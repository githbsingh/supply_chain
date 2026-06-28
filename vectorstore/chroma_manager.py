import os

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#from langchain_ollama import OllamaEmbeddings


class ChromaManager:

    def __init__(self):

        self.embeddings = (
            GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-2-preview",
                google_api_key=os.getenv("GOOGLE_API_KEY")#os.environ["GOOGLE_API_KEY"]
            )
        )
        print(
            len(
                self.embeddings.embed_query(
                    "test"
                )
            )
        )

    def create_vector_store(
        self,
        chunks
    ):

        db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="chroma_db"
        )

        return db

    # def load_vector_store(self):

    #     return Chroma(
    #         persist_directory="chroma_db",
    #         embedding_function=self.embeddings
    #     )