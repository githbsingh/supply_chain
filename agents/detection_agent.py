def detection_agent(state):

    event = state["event"]
    
    delay_days = event.get(
        "delay_days",
        0
    )

    if delay_days > 5:

        state["disruption"] = {
            "issue": "Supplier Delay"
        }

    else:

        state["disruption"] = {
            "issue": "No Risk"
        }

    return state