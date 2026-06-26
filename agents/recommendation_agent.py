from models.llm import llm
import textwrap


def recommendation_agent(state):

    prompt = textwrap.dedent(f"""You are a Supply Chain Risk Analyst.

        Your job is to strictly follow the SOP rules provided in the context.

        =====================
        SOP CONTEXT
        =====================

        {state['retrieved_docs']}

        =====================
        CURRENT EVENT
        =====================

        Supplier: {state['event'].get('supplier')}
        Material: {state['event'].get('material')}
        Delay Days: {state['event'].get('delay_days')}
        Inventory Days Remaining: {state['event'].get('inventory_days')}

        =====================
        RISK ASSESSMENT
        =====================

        Risk Score: {state['risk']['risk_score']}
        Severity: {state['risk']['severity']}

        Impact: {state['impact']}

        =====================
        INSTRUCTIONS
        =====================

        1. Read the SOP context carefully.

        2. Identify:
           - Severity Classification rules
           - Risk Assessment Methodology
           - Delay Escalation Protocol
           - Targeted Response Actions

        3. Determine which SOP rules apply to this event.

        4. Use ONLY recommendations and actions defined in the SOP.

        5. If the SOP does not explicitly provide an action,
           derive a reasonable action based on the SOP.

        6. Explain WHY each recommendation was selected.

        7. Return valid JSON only.

        Output Format:

        {{
            "applied_rules": [
                "...",
                "..."
            ],
            "recommendations": [
                {{
                    "action": "...",
                    "reason": "..."
                }}
            ]
        }}
        """)
    print("=" * 50)
    print("PROMPT SENT TO LLM")
    print("=" * 50)
    print(prompt)
    print("=" * 50)
    try:
        response = llm.invoke(prompt)

        print("SUCCESS")
        #print(response.content)

        state["recommendations"] = response.content

    except Exception as e:
        print("LLM ERROR:", str(e))

        state["recommendations"] = f"LLM Failed: {str(e)}"
        response = None

    trace = state.get("trace", [])
    trace.append(
        f"🤖 Recommendation Agent: Generated recommendations for {state.get('event', {}).get('material')}"
    )
    state["trace"] = trace

    if response is not None and hasattr(response, "content"):
        state["recommendations"] = response.content
        #print("LLM Response:", response.content)

    return state