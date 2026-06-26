def impact_agent(state):

    score = state[
        "risk"
    ][
        "risk_score"
    ]

    impact = (
        "Production may stop "
        "within 24 hours"
    )

    if score < 50:

        impact = (
            "Minor production impact"
        )

    state["impact"] = {
        "impact": impact
    }

    return state