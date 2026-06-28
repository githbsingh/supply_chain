from turtle import st

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.logger import logger

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. Set it in .env for local development or in Streamlit Secrets for deployment."
        )
def retrieve_context(query):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=api_key#os.environ["GOOGLE_API_KEY"]
    )

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    logger.info(f"Query: {query}")

    docs = db.similarity_search(
    "severity",
    k=1,
    filter={
        "section":
            "3. SEVERITY CLASSIFICATION"
    }
)

    logger.info(f"Retrieved {len(docs)} chunks")
    logger.info(f"Retrieved chunks: {docs}")

    # return "\n".join(
    #     [
    #         doc.page_content
    #         for doc in docs
    #     ]
    # )
    return docs