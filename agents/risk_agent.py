from utils.logger import logger
def risk_agent(state):

    event = state["event"]

    delay_days = event.get(
        "delay_days",
        0
    )
    logger.info(f"risk_agent started")
    logger.info(f"delay_days: {delay_days}")

    inventory_days = event.get(
        "inventory_days",
        10
    )
    logger.info(f"inventory_days: {inventory_days}")
    score = 0

    score += delay_days * 10

    if inventory_days < 2:

        score += 30
    logger.info(f"risk_score: {score}")
    if score > 100:
        score = 100

    severity = "Low"

    if score > 90:
        severity = "Critical"

    elif score > 70:
        severity = "High"

    elif score > 40:
        severity = "Medium"

    state["risk"] = {
        "risk_score": score,
        "severity": severity
    }

    trace = state.get(
    "trace",
    []
    )
    
    trace.append(
        f"⚠️ Risk Agent: Risk Score={state['risk']['risk_score']}"
    )
    
    # return {
    #     "risk_assessment": state["risk"],
    #     "trace": trace
    # }

    return state