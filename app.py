import streamlit as st
import os
import streamlit as st
import json
from graph.workflow import (
    graph
)
#from kafka_utils.consumer import get_latest_risk

# risk_event = get_latest_risk()

# risk_event = get_latest_risk()

# if risk_event:

#     result = graph.invoke(
#         {
#             "event": risk_event,
#             "trace": []
#         }
#     )

st.title(
    "Supply Chain Control Tower"
)

st.subheader("Supply Chain Event")

supplier = st.text_input(
    "Supplier",
    "CircuitParts"
)

material = st.text_input(
    "Material",
    "Microchips"
)

delay_days = st.number_input(
    "Delay Days",
    min_value=0,
    value=7
)

inventory_days = st.number_input(
    "Inventory Coverage (Days)",
    min_value=0,
    value=1
)

event = {
    "supplier": supplier,
    "material": material,
    "delay_days": delay_days,
    "inventory_days": inventory_days
}

uploaded_files = st.sidebar.file_uploader(
    "Upload SOP Documents",


    
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs(
        "knowledge_base",
        exist_ok=True
    )

    for file in uploaded_files:

        file_path = os.path.join(
            "knowledge_base",
            file.name
        )

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(
                file.getbuffer()
            )

    st.sidebar.success(
        f"{len(uploaded_files)} PDFs uploaded"
    )

if st.sidebar.button(
    "Build Knowledge Base"
):
    from ingestion.ingest import main

    main()

    st.sidebar.success(
        "Knowledge Base Created"
    )
if st.button(
    "Analyze"
):

    result = graph.invoke(
        {
            "event": event,
            "trace": []
        }
    )

    st.subheader(
        "🔄 Agent Execution Trace"
    )

    # for step in result["trace"]:
    #     #st.write(step)
    #     print("step:", step)
    #     trace_container = st.empty()

    #     trace_text = ""

    alert = result["final_alert"]
    st.subheader(
        "🚨 Supply Chain Alert"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Severity",
            alert["severity"]
        )
    with col2:
        st.metric(
            "Risk Score",
            alert["risk_score"]
        )
    with col3:
        st.metric(
            "Alert ID",
            alert["alert_id"][:8]
        )
    # ------------------------------
    # Issue
    # ------------------------------
    st.error(
        f"⚠️ Issue: {alert['issue']}"
    )
    # ------------------------------
    # Impact
    # ------------------------------
    st.info(
        f"📊 Impact: {alert['impact']}"
    )
    # ------------------------------
    # Recommendations
    # ------------------------------
    st.subheader(
        "✅ Recommended Actions"
    )
    recommendations = alert["recommendations"]
    try:
        rec_json = json.loads(recommendations)
        st.subheader("📋 Applied Rules")
        for rule in rec_json["applied_rules"]:
            st.info(rule)
        st.subheader("✅ Recommendations")

        for i, rec in enumerate(rec_json["recommendations"], start=1):
            with st.expander(f"Recommendation {i}"):
                st.markdown(f"**Action:** {rec['action']}")
                st.markdown(f"**Reason:** {rec['reason']}")
    except Exception:
        st.code(recommendations)