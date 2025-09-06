from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Agent import agent 
from process_media import process_media
import startup
import os

app = FastAPI(title="Annadata Agent API")
production_frontend_url = os.environ.get("FRONTEND_URL")
origins = [
    "http://localhost:3000",
    "http://localhost:8000", # If your other API is on 8000
    "http://127.0.0.1:3000",
]
if production_frontend_url:
    origins.append(production_frontend_url)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows the specified origins
    allow_credentials=True,         # Allows cookies, authorization headers, etc.
    allow_methods=["*"],            # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],            # Allows all headers
)
# Request body schema
class QueryRequest(BaseModel):
    query: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    history: Optional[List[dict]] = None

@app.get("/")
def root():
    return {"message": "AnnaData Agent API is running!"}

@app.post("/agent")
def run_agent(request: QueryRequest):
    try:
        result = agent(
            query=request.query,
            latitude=request.latitude,
            longitude=request.longitude,
            history=request.history,
        )
        print(f"Agent function returned: {result}")
        return {"answer": result}
    except Exception as e:
        print(f"Error in agent function: {e}")
        return {"error": str(e)}
    
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat/describe")
async def chat_describe(
    audio: Optional[UploadFile | str] = File(None, description="Optional audio file (.mp3)"),
    image: Optional[UploadFile | str] = File(None, description="Optional image file (.jpg)")
):
    audio_bytes, image_bytes = None, None

    if audio is not None and audio != "":
        audio_bytes = await audio.read()
    if image is not None and image != "":
        image_bytes = await image.read()

    if not audio_bytes and not image_bytes:
        return JSONResponse(content={"error": "No file provided"}, status_code=400)

    if audio_bytes and image_bytes:
        prompt_text = "First transcribe the audio into English, then describe the crop details from the image. Output format: Audio: , Crop Name: , Crop Type: , Crop Stage: , Pests/Diseases: ."
    elif audio_bytes:
        prompt_text = "Transcribe this audio into English."
    elif image_bytes:
        prompt_text = "Provide the crop name, crop type, crop stage, and any visible pests or diseases in one line. Output format: Crop Name: , Crop Type: , Crop Stage: , Pests/Diseases: ."
    else:
        prompt_text = ""

    output = await process_media(
        audio_bytes=audio_bytes,
        image_bytes=image_bytes,
        extra_prompt=prompt_text,
    )
    return JSONResponse(content={"Result": output.strip()})

