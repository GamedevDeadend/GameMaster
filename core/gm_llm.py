import os

from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7, max_tokens=1024, api_key=api_key)

