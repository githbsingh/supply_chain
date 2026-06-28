import os
from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. Set it in .env for local development or in Streamlit Secrets for deployment."
        )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0,
)