def detection_agent(state):

    event = state["event"]
    
    risk_type = event.get(
        "risk_type",
        0
    )
    print("risk_type:", risk_type)

    if risk_type == 'CRITICAL_DELAY':

        state["disruption"] = {
            "issue": "Supplier Delay"
        }
    elif risk_type == 'OUT_OF_STOCK_RISK':

        state["disruption"] = {
            "issue": "Material Out of Stock"
        }
    elif risk_type == 'DELAYED_SHIPMENT':

        state["disruption"] = {
            "issue": "Delayed Shipment"
        }

    else:
        state["disruption"] = {
            "issue": "No Risk"
        }

    return state