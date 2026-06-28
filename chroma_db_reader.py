import os
from turtle import st
from dotenv import load_dotenv
load_dotenv()
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from utils.logger import logger

logger.info("Initializing Chroma DB")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. Set it in .env for local development or in Streamlit Secrets for deployment."
        )
db = Chroma(
    persist_directory="chroma_db",
    embedding_function=GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=api_key#os.environ["GOOGLE_API_KEY"]
    )
)

collection = db._collection

data = collection.get()

#print(f"Total Documents: {len(data['ids'])}")

# for i in range(len(data["ids"])):
    # print("=" * 80)
    # print("ID:", data["ids"][i])
    # print("Metadata:", data["metadatas"][i])
    # print("Document:", data["documents"][i][:500])

#data = collection.get()

for meta in data["metadatas"]:
    logger.info(meta)