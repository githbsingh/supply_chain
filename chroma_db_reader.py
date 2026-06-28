import os

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from utils.logger import logger

logger.info("Initializing Chroma DB")

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=os.getenv("GOOGLE_API_KEY")#os.environ["GOOGLE_API_KEY"]
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