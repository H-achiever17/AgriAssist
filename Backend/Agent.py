from langchain.schema import HumanMessage
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from utils import llm
from Address_Convertor import get_location
from Mandi_Price_Tool import get_state_data
from Query_Parser import extract_farm_info
from weather_tool import weather_openmeteo
from Soil_Tool import soil_tool
from Refined_Farmer_Query import get_farming_query
from typing import List, Optional
from Web_Crawler import query_kb
import json
import re

def extract_markdown_content(text: str) -> str:
    pattern = r"```markdown\n([\s\S]*?)\n```"
    
    match = re.search(pattern, text)
    
    if match:
        return match.group(1).strip()
    else:
        return text


def get_open_ended_answer(query: str, history: List[dict]) -> str:
    """
    query: str - the farmer's latest question
    history: list[dict] - [{"role": "user"/"assistant", "content": "..."}]
    """
    print("QUERY:", query)
    print("HISTORY:", history)
    if history is None:
        history_text = ""
    else:
        history_text = "\n".join(
            [f"{h['role'].capitalize()}: {h['content']}" for h in history]
        )
    
    prompt = f"""
    **Role and Goal:**
    You are a highly knowledgeable agronomist and expert agricultural advisor, specializing in Indian farming conditions. Your goal is to provide a detailed, scientifically valid, and practical answer to the farmer's question, using the provided conversation history for context.

    **Critical Instructions:**
    1.  **Language:** You MUST respond in the exact same language as the "Farmer's latest question". Do not translate or switch languages.
    2.  **Content:** The advice must be accurate, practical for Indian conditions, and directly address the farmer's latest query. Keep the answer concise, ideally under 250 words.

    ---

    **Conversation Context:**

    **Conversation so far:**
    {history_text}

    **Farmer's latest question:**
    {query}

    ---

    **Assistant's Expert Agronomic Advice:**
    """
    
    response = llm([HumanMessage(content=prompt)])
    return response.content.strip()

def get_farming_advice(location, state, crop, soil, weather, mandi_price, kb_answer, farmer_query):
    """
    location: dict with keys 'village', 'district', 'state', 'lat', 'lon'
    crop: str, crop name
    soil: dict with keys like 'texture', 'ph', 'organic_carbon'
    weather: dict with keys like 'temperature', 'rainfall', 'humidity', 'forecast'
    farmer_query: str, the question farmer is asking
    """

    prompt = f"""
    You are an expert agronomist and agricultural advisor. 
    Answer the farmer's question using the provided data. 
    Always respond in the farmer's query language: 
    Farmer's Query: {farmer_query}.

    Constraints:
    - Keep the response under 200 words.
    - Be concise, practical, and farmer-friendly.
    - Always reference the relevant data points (soil values, weather, mandi prices, etc.) in your answer.
    - Do not invent facts beyond the given data.
    - Format response clearly into sections.

    Context:
    - 
    - Location: {location}
    - State: {state}
    - Crop: {crop}
    - Soil: {soil}
    - Weather: {weather}
    - Mandi Price: {mandi_price}
    - Knowledge Base Answer: {kb_answer}
    - Farmer's Question: {farmer_query}
    """

    response = llm([HumanMessage(content=prompt)])
    return response.content


def kb_router(query: str) -> bool:
    """
    Uses LLM to decide whether the query requires knowledge base lookup.
    Returns True if query is about cold storage or farming schemes, else False.
    """
    response_schemas = [
        ResponseSchema(
            name="query",
            description='Return "YES" if the query is about storage or government schemes, otherwise "NO".'
        )
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = f"""
    You are a query classifier for an agricultural assistant.

    Farmer's query: "{query}"

    Task:
    Classify the query:
    - If it's about "storage or cold storage" OR "government schemes" (subsidies, support schemes, loan schemes, insurance, etc.), return YES.
    - Otherwise, return NO.

    {format_instructions}
    """

    response = llm([HumanMessage(content=prompt)])
    
    try:
        parsed = output_parser.parse(response.content)
        return parsed["query"].strip().upper() == "YES"
    except Exception as e:
        print("Router Parsing Error:", e, response.content)
        return False

def agent(
    query: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    history: Optional[List] = []
) -> str:
    query_final = get_farming_query(query, history)
    print(f"Final query after refinement: {query_final}")
    structured_input = extract_farm_info(query_final)

    crop = structured_input.get("crop_type", "unknown")
    state = structured_input.get("state", "unknown")
    location = structured_input.get("location", "unknown")
    answer = structured_input.get("answer", "unknown")

    print(f"Extracted Crop: {crop}, State: {state}, Location: {location}, answer: {answer}")

    if answer != "unknown" and crop == "unknown" and state == "unknown" and location == "unknown":
        return answer


    lat, lon = latitude, longitude
    if location != "unknown":
        lat, lon = get_location(location)
    
    print(f"Coordinates from location: lat={lat}, lon={lon}")

    if lat == "unknown" or lat is None or lon == "unknown" or lon is None:
        final_res = extract_markdown_content(get_open_ended_answer(query_final, history))
        print(final_res)
        return final_res
    
    is_kb_required = kb_router(query_final)
    print(f"Is knowledge base required? {is_kb_required}")
    if is_kb_required:
        result = json.dumps(query_kb(query_final), indent=4)
        answer_from_kb = json.loads(result)['output']['text']
        return answer_from_kb
    else:
        answer_from_kb = ""

    soil = soil_tool(lat, lon)
    weather = weather_openmeteo(lat, lon)
    mandi_price = get_state_data(state)

    print(lat, lon, soil, weather)

    final_response = extract_markdown_content(get_farming_advice(location, state, crop, soil, weather, mandi_price, answer_from_kb, query))
    print(f"Final response: {final_response}")
    return final_response
    