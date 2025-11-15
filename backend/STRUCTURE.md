# Backend Code Structure

## Project Organization

```
backend/
├── main.py                    # FastAPI application entry point
├── services/                  # Services module
│   ├── __init__.py           # Module initialization
│   ├── whisper_service.py    # Whisper AI transcription service
│   └── mcp_server.py         # MCP Server for order processing
├── data/                      # Data directory
│   └── orders.xlsx           # Excel file with orders
├── create_sample_excel.py    # Script to generate sample data
├── requirements.txt          # Python dependencies
└── README.md                  # Setup instructions
```

## Services

### 1. WhisperService (`services/whisper_service.py`)
**Purpose:** Handle audio/video transcription using OpenAI Whisper

**Key Methods:**
- `__init__(model_name)`: Initialize Whisper model
- `transcribe_file(file_path)`: Transcribe from file path
- `transcribe_audio_content(audio_content, file_extension)`: Transcribe from bytes

**Usage:**
```python
from services.whisper_service import WhisperService

whisper = WhisperService(model_name="base")
result = whisper.transcribe_file("audio.wav")
text = result.get("text")
```

### 2. MCPServer (`services/mcp_server.py`)
**Purpose:** Process transcripts, extract data, lookup orders, generate responses

**Key Methods:**
- `__init__(excel_path, openai_api_key)`: Initialize with Excel file path
- `extract_from_text(transcript)`: Extract mobile, order ID, name, topic, intent
- `lookup_order(mobile_number, order_id)`: Search Excel for order
- `generate_response(extracted, order_status, status_found)`: Create response text
- `process(transcript)`: Complete processing pipeline

**Usage:**
```python
from services.mcp_server import MCPServer

mcp = MCPServer(excel_path="data/orders.xlsx")
result = mcp.process("Hello, I want to check my order AMZ12345")
```

## Main Application (`main.py`)

**Endpoints:**
- `POST /process-audio`: Main endpoint for audio processing
- `POST /analyze`: Legacy endpoint (redirects to /process-audio)
- `GET /audio/{filename}`: Serve TTS audio files

**Flow:**
1. Receive audio file
2. Save to temporary file
3. WhisperService → Transcribe to text
4. MCPServer → Extract, lookup, generate response
5. OpenAI TTS → Generate audio
6. Return JSON response

## Benefits of This Structure

✅ **Separation of Concerns**: Each service has a single responsibility
✅ **Modularity**: Services can be tested and used independently
✅ **Maintainability**: Easy to update or replace individual services
✅ **Reusability**: Services can be imported in other projects
✅ **Clean Code**: Main file focuses on API routing, not business logic

