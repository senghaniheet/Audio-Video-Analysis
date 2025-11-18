from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI
import uvicorn
import tempfile
import os
import uuid
from services.whisper_service import WhisperService
import sys

# Add mcp-order-status/server to path to import MCP server
# mcp_server_path = os.path.join(os.path.dirname(__file__), '..', 'mcp-order-status', 'server')
# sys.path.insert(0, mcp_server_path)
##from order_mcp_server import handle_mcp_request
from services.gemini_server import extract_details, format_service_boy_response

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
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

# MCP Server is now in mcp-order-status/server - will be called via handle_mcp_request


@app.get("/")
async def root():
    return {"message": "AI-Based Amazon Order Status Voice Assistant API"}


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

        # Step 3: Process through Gemini Server (extract details and format)
        print("Processing through Gemini Server...")
        # Commented out MCP server code
        # mcp_result = process_text(transcription)
        
        # Call Gemini server's extract_details method
        extracted_data = extract_details(transcription)
        human_readable_text = format_service_boy_response(extracted_data, transcription)
        
        # Create result structure similar to MCP server response
        mcp_result = {
            "transcript": transcription,
            "mobile_number": extracted_data.get("mobile_number"),
            "order_id": extracted_data.get("order_id"),
            "customer_name": extracted_data.get("name"),
            "topic": "",
            "intent": "",
            "status_found": extracted_data.get("status_found", False),
            "order_status": {
                "status": extracted_data.get("order_status", ""),
                "delivery_date": extracted_data.get("delivery_date", ""),
                "last_update": extracted_data.get("last_update", "")
            },
            "response_text": human_readable_text,
            "response_voice_text": human_readable_text
        }
        
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

