from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI
import uvicorn
import tempfile
import os
import uuid
from datetime import datetime, timedelta
from services.whisper_service import WhisperService
from services.mcp_server import MCPServer

app = FastAPI()

# CORS middleware to allow Angular frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Whisper Service
whisper_service = WhisperService(model_name="base")  # Using 'base' for faster startup

# Initialize OpenAI client (set your API key as environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

# Initialize MCP Server
mcp_server = MCPServer(
    excel_path="data/orders.xlsx",
    openai_api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
)


@app.get("/")
async def root():
    return {"message": "AI-Based Amazon Order Status Voice Assistant API"}


async def get_order_status(order_id: str = None, mobile_number: str = None):
    """
    Mock order status API. Replace this with actual API call.
    In production, this would call the real Amazon Order Status API.
    """
    # Mock data for demonstration
    if order_id:
        # Simulate API call delay
        import asyncio
        await asyncio.sleep(0.5)
        
        # Mock order status based on order ID
        statuses = {
            "AMZ": {"status": "Shipped", "delivery_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), "courier": "BlueDart"},
            "ORD": {"status": "Out for Delivery", "delivery_date": datetime.now().strftime("%Y-%m-%d"), "courier": "Amazon Logistics"},
            "DEL": {"status": "Delivered", "delivery_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "courier": "BlueDart"},
        }
        
        # Get status based on prefix
        prefix = order_id[:3] if len(order_id) >= 3 else "AMZ"
        return statuses.get(prefix, {
            "status": "Processing",
            "delivery_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "courier": "Amazon Logistics"
        })
    
    if mobile_number:
        # Mock lookup by mobile number
        import asyncio
        await asyncio.sleep(0.5)
        return {
            "status": "Shipped",
            "delivery_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "courier": "BlueDart"
        }
    
    return {
        "status": "Not Found",
        "delivery_date": None,
        "courier": None
    }


@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """
    Main endpoint: Audio -> Whisper -> MCP Server -> Response
    """
    temp_path = None
    audio_filename = None
    
    try:
        # Step 1: Save uploaded file
        file_extension = os.path.splitext(file.filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name

        # Step 2: Transcription using Whisper Service
        print(f"Transcribing audio/video file: {temp_path}")
        result = whisper_service.transcribe_file(temp_path)
        transcription = result.get("text", "")
        
        if not transcription.strip():
            return {
                "error": "No speech detected in the audio file",
                "transcript": ""
            }

        # Step 3: Process through MCP Server
        print("Processing through MCP Server...")
        mcp_result = mcp_server.process(transcription)
        
        # Step 4: Generate TTS Audio if response available
        voice_text = mcp_result.get("response_voice_text", "")
        audio_url = None
        
        if voice_text:
            try:
                print("Generating TTS audio...")
                tts_response = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=voice_text
                )
                
                audio_filename = f"{uuid.uuid4().hex}.mp3"
                audio_path = os.path.join(tempfile.gettempdir(), audio_filename)
                
                with open(audio_path, 'wb') as audio_file:
                    audio_file.write(tts_response.content)
                
                audio_url = f"/audio/{audio_filename}"
            except Exception as e:
                print(f"TTS generation failed: {str(e)}")
                audio_url = None

        # Add audio_url to result
        mcp_result["audio_url"] = audio_url
        
        return mcp_result

    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": f"Error processing audio: {str(e)}",
            "transcript": "",
            "mobile_number": None,
            "order_id": None,
            "customer_name": None,
            "topic": "",
            "intent": "",
            "status_found": False,
            "order_status": {
                "status": "",
                "delivery_date": "",
                "last_update": ""
            },
            "response_text": "",
            "response_voice_text": "",
            "audio_url": None
        }
    
    finally:
        # Clean up temporary files
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"Error deleting temp file: {str(e)}")


# Keep /analyze endpoint for backward compatibility
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Legacy endpoint - redirects to /process-audio"""
    return await process_audio(file)


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated TTS audio files"""
    # In production, implement proper file storage and retrieval
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "Audio file not found"}


# Keep old endpoint for backward compatibility
@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    """Legacy endpoint - redirects to /analyze"""
    return await analyze(file)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

