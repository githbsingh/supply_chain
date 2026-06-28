import streamlit as st
import os
import streamlit as st
import json
from graph.workflow import (
    graph
)
from kafka_utils.consumer import get_latest_risk


risk_event = get_latest_risk()
print("risk_event:", risk_event)

if risk_event:

    result = graph.invoke(
        {
            "event": risk_event,
            "trace": []
        }
    )

    # ------------------------
    # Event Details
    # ------------------------
    event = result["event"]

    st.title("🚨 Supply Chain Control Tower")

    st.subheader("📦 Supply Chain Event")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Supplier", event["supplier"])
        st.metric("Material", event["material"])

    with col2:
        st.metric("Risk Type", event["risk_type"])
        st.metric("Risk Score", event["risk_score"])

    # ------------------------
    # Alert Summary
    # ------------------------

    alert = result["final_alert"]

    st.subheader("⚠️ Alert Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Severity", alert["severity"])

    with col2:
        st.metric("Risk Score", alert["risk_score"])

    with col3:
        st.metric("Alert ID", alert["alert_id"][:8])

    st.error(f"**Issue:** {alert['issue']}")
    st.info(f"**Impact:** {alert['impact']}")

    # ------------------------
    # Recommendations
    # ------------------------

    rec_json = json.loads(alert["recommendations"])

    st.subheader("📋 Applied Rules")

    for rule in rec_json["applied_rules"]:
        st.info(rule)

    st.subheader("✅ Recommended Actions")

    for i, rec in enumerate(rec_json["recommendations"], start=1):

        with st.container(border=True):

            st.markdown(f"### Recommendation {i}")

            st.write(f"**Action:** {rec['action']}")

            st.write(f"**Reason:** {rec['reason']}")