from retrieval.retriever import retrieve_context
from utils.logger import logger


def retrieval_agent(state):

    logger.info(
        "Retrieval Agent Started"
    )

    # query = str(
    #     state["event"]
    # )
    query = f"Get SEVERITY CLASSIFICATION and RISK ASSESSMENT methodology from the knowledge base in json format" 
    logger.info(f"query: {query}")
    docs = retrieve_context(
        query
    )

    state["retrieved_docs"] = docs

    logger.info(
        f"Retrieved {len(docs)} characters from knowledge base"
    )
    logger.info(docs)

    return state