from typing import TypedDict


class SupplyChainState(TypedDict):

    event: dict

    disruption: dict

    risk: dict

    retrieved_docs: str

    impact: dict

    recommendations: list

    final_alert: dict

    trace: list