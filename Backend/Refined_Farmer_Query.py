from langchain.prompts import ChatPromptTemplate
from utils import llm

def get_farming_query(query: str, history: list):
    """
    query: str - the farmer's latest question
    history: list[dict] - [{"role": "user"/"assistant", "content": "..."}]
    llm: initialized LLM (e.g. ChatOpenAI or Bedrock LLM)
    """
    if(history is None):
        return query
    # Convert history into a readable conversation
    history_text = "\n".join(
        [f"{h['role'].capitalize()}: {h['content']}" for h in history]
    )
    
    prompt = ChatPromptTemplate.from_template("""
    You are a farming assistant. A farmer is asking questions. 
    Use the conversation history to understand context and rewrite the latest question as a complete, standalone query.

    Conversation so far:
    {history}

    Farmer's latest question:
    {query}

    Rewritten standalone query:
    """)
    
    chain = prompt | llm
    response = chain.invoke({"history": history_text, "query": query})
    
    return response.content.strip()
