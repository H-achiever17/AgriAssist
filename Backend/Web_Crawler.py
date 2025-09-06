import os
import boto3

KNOWLEDGE_BASE_ID =  os.getenv("KNOWLEDGE_BASE_ID")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def query_kb(question):
    """Retrieve info from KB and generate an LLM answer."""
    response = client.retrieve_and_generate(
        input={
            "text": question
        },
        retrieveAndGenerateConfiguration = {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": "arn:aws:bedrock:ap-south-1::foundation-model/meta.llama3-70b-instruct-v1:0",
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {
                        "numberOfResults": 8
                    }
                },
                "generationConfiguration": {
                    "inferenceConfig": {
                        "textInferenceConfig": {
                            "temperature": 0.2,
                            "topP": 0.9,
                            "maxTokens": 1024
                        }
                    }
                },
                "orchestrationConfiguration": {
                    "inferenceConfig": {
                        "textInferenceConfig": {
                            "temperature": 0.2,
                            "topP": 0.9,
                            "maxTokens": 512
                        }
                    }
                }
            }
        }
    )
    return response