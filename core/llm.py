from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=1024, api_key=api_key)

