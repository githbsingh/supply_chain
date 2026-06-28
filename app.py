import os
import json
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from graph.workflow import graph
from kafka_utils.consumer import get_latest_risk
import time
from dotenv import load_dotenv
load_dotenv()

# ----------------------------------------------------
# Streamlit Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Control Tower",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI Supply Chain Control Tower")


# ----------------------------------------------------
# Sidebar : Knowledge Base Management
# ----------------------------------------------------

st.sidebar.header("📚 Knowledge Base")

KB_PATH = Path("chroma_db")

kb_exists = KB_PATH.exists() and any(KB_PATH.iterdir())

uploaded_files = st.sidebar.file_uploader(
    "Upload SOP Documents",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs("knowledge_base", exist_ok=True)

    for file in uploaded_files:

        with open(
            os.path.join("knowledge_base", file.name),
            "wb"
        ) as f:

            f.write(file.getbuffer())

    st.sidebar.success(
        f"{len(uploaded_files)} document(s) uploaded."
    )

if st.sidebar.button("Build / Refresh Knowledge Base"):

    with st.spinner("Building Knowledge Base..."):
        # Clear cached resources
        st.cache_resource.clear()

        from ingestion.ingest import main

        main()

    st.sidebar.success("Knowledge Base created successfully.")

    st.rerun()


# ----------------------------------------------------
# Stop if KB not available
# ----------------------------------------------------

if not kb_exists:

    st.warning(
        """
        Knowledge Base not found.

        Upload SOP PDFs from the sidebar and click
        **Build / Refresh Knowledge Base**.
        """
    )

    st.stop()


# ----------------------------------------------------
# Live Streaming
# ----------------------------------------------------

st.sidebar.success("✅ Knowledge Base Loaded")

st.sidebar.markdown("---")

refresh = st.sidebar.slider(
    "Refresh Interval (seconds)",
    2,
    300,
    5
)
#Refresh the app every 60 seconds
st_autorefresh(
    interval=300 * 1000,
    key="refresh"
)


# ----------------------------------------------------
# Consume Latest Risk Event
# ----------------------------------------------------

risk_event = get_latest_risk()

if risk_event is None:

    st.info("Waiting for Kafka events...")

    st.stop()


# ----------------------------------------------------
# Invoke LangGraph
# ----------------------------------------------------

start_time = time.perf_counter()
with st.spinner("Running AI Agents..."):

    result = graph.invoke(
        {
            "event": risk_event,
            "trace": []
        }
    )

end_time = time.perf_counter()

st.sidebar.metric(
    "End-to-End Latency",
    f"{end_time - start_time:.2f} sec"
)
event = result["event"]

alert = result["final_alert"]


# ----------------------------------------------------
# Event Summary
# ----------------------------------------------------

st.subheader("📦 Live Risk Event")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Supplier", event["supplier"])
c2.metric("Material", event["material"])
c3.metric("Risk Type", event["risk_type"])
c4.metric("Risk Score", event["risk_score"])


# ----------------------------------------------------
# Alert Summary
# ----------------------------------------------------

st.subheader("🚨 Alert")

a1, a2, a3 = st.columns(3)

a1.metric(
    "Severity",
    alert["severity"]
)

a2.metric(
    "Risk Score",
    alert["risk_score"]
)

a3.metric(
    "Alert ID",
    alert["alert_id"][:8]
)

st.error(f"**Issue:** {alert['issue']}")

st.info(f"**Impact:** {alert['impact']}")


# ----------------------------------------------------
# Recommendations
# ----------------------------------------------------

st.subheader("✅ Recommendations")

try:

    recommendations = alert.get("recommendations", "")

    # Handle both string and dict responses
    if isinstance(recommendations, str):

        # Remove markdown code fences if present
        recommendations = recommendations.strip()

        if recommendations.startswith("```json"):
            recommendations = recommendations.replace("```json", "", 1)

        if recommendations.endswith("```"):
            recommendations = recommendations[:-3]

        recommendations = recommendations.strip()

        # Extract only JSON object
        start = recommendations.find("{")
        end = recommendations.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No valid JSON found in recommendations.")

        recommendations = json.loads(
            recommendations[start:end]
        )

    # recommendations is now a Python dict

    st.markdown("### 📋 Applied Rules")

    for rule in recommendations.get("applied_rules", []):
        st.info(rule)

    st.markdown("### ✅ Suggested Actions")

    for i, rec in enumerate(
        recommendations.get("recommendations", []),
        start=1
    ):

        with st.container(border=True):

            st.markdown(f"### Recommendation {i}")

            st.success(f"**Action:** {rec.get('action', 'N/A')}")

            st.write(f"**Reason:** {rec.get('reason', 'N/A')}")

except Exception as e:

    st.error("Unable to parse recommendations.")

    st.code(str(e))

    st.code(alert.get("recommendations", ""))


# ----------------------------------------------------
# Agent Execution Trace
# ----------------------------------------------------

if result.get("trace"):

    st.subheader("🤖 Agent Execution")

    for step in result["trace"]:

        st.success(step)


# ----------------------------------------------------
# Retrieved SOP Chunks
# ----------------------------------------------------

docs = result.get("retrieved_docs", [])

if docs:

    with st.expander("📄 Retrieved SOP Context"):

        for i, doc in enumerate(docs, start=1):

            st.markdown(f"### Document {i}")

            if hasattr(doc, "metadata"):

                st.write(
                    f"**Source:** {doc.metadata.get('source','Unknown')}"
                )

                st.write(
                    f"**Section:** {doc.metadata.get('section','')}"
                )

            st.write(doc.page_content[:1000])

            st.divider()