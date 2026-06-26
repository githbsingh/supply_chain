from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import (
    SupplyChainState
)

from agents.detection_agent import (
    detection_agent
)

from agents.risk_agent import (
    risk_agent
)

from agents.retrieval_agent import (
    retrieval_agent
)

from agents.impact_agent import (
    impact_agent
)

from agents.recommendation_agent import (
    recommendation_agent
)

from agents.alert_agent import (
    alert_agent
)


workflow = StateGraph(
    SupplyChainState
)

workflow.add_node(
    "detect",
    detection_agent
)

workflow.add_node(
    "risk",
    risk_agent
)

workflow.add_node(
    "retrieve",
    retrieval_agent
)

workflow.add_node(
    "impact",
    impact_agent
)

workflow.add_node(
    "recommend",
    recommendation_agent
)

workflow.add_node(
    "alert",
    alert_agent
)

workflow.set_entry_point(
    "detect"
)

workflow.add_edge(
    "detect",
    "risk"
)

workflow.add_edge(
    "risk",
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "impact"
)

workflow.add_edge(
    "impact",
    "recommend"
)

workflow.add_edge(
    "recommend",
    "alert"
)

workflow.add_edge(
    "alert",
    END
)

graph = workflow.compile()