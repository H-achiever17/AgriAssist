import os
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def get_llm():
    """Return the global LLM instance."""
    return llm

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

def get_client():
    """
    Returns the GenAI client instance.
    """
    return client