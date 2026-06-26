import uuid


def alert_agent(state):

    state["final_alert"] = {

        "alert_id":
            str(uuid.uuid4())[:8],

        "severity":
            state["risk"]["severity"],

        "risk_score":
            state["risk"]["risk_score"],

        "issue":
            state["disruption"]["issue"],

        "impact":
            state["impact"]["impact"],

        "recommendations":
            state["recommendations"]
    }

    return state