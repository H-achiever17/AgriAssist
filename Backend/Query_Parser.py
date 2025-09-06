from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from utils import llm 

def extract_farm_info(farmer_input: str):
    response_schemas = [
        ResponseSchema(
        name="location",
        description="Location of the farm (village, district, state, etc.)"),
        ResponseSchema(name="state", description="State where the farm is located. Use the location information to locate the indian state"),
        ResponseSchema(name="crop_type", description="Type of crop being grown"),
        ResponseSchema(name="answer", description="If the query is not related to agriculture, ptovide a short answer to the query in the query language."),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
    You are an Farming assistant that extracts structured agricultural data from farmer queries. Always translate the laguage of the query into English.

    Farmer's Input:
    {farmer_input}

    {format_instructions}

    Make sure:
    - "location" is just the location.
    - "state" is the state name, not the full address.
    - "crop_type" is only the crop name.
    - "answer" is a short answer to the query if it is not related to agriculture.
    If information is missing, put "unknown".
    """,
        input_variables=["farmer_input"],
        partial_variables={"format_instructions": format_instructions},
    )
    try:
        _input = prompt.format_prompt(farmer_input=farmer_input)
        output = llm(_input.to_messages()).content
        print(f"LLM output: {output}")
        if not output:
            return {
                "location": "unknown",
                "state": "unknown",
                "crop_type": "unknown",
                "answer": "unknown"
            }
        parsed = output_parser.parse(output)
        return parsed
    
    except Exception as e:
        return {
            "query": "unknown",
            "location": "unknown",
            "crop_type": "unknown",
            "error": str(e)
        }
