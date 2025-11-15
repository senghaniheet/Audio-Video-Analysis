# Backend Setup with MCP Server

## Quick Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Create sample Excel file:**
```bash
python create_sample_excel.py
```

This creates `data/orders.xlsx` with 50 sample orders.

3. **Set OpenAI API Key:**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_api_key_here"

# Windows CMD
set OPENAI_API_KEY=your_api_key_here

# macOS/Linux
export OPENAI_API_KEY=your_api_key_here
```

4. **Run backend:**
```bash
python main.py
```

## Project Structure

```
backend/
├── main.py                 # FastAPI server
├── mcp_server.py          # MCP Server with Excel lookup
├── create_sample_excel.py # Script to generate sample data
├── data/
│   └── orders.xlsx        # Excel file with orders (created by script)
└── requirements.txt       # Dependencies
```

## API Endpoints

### POST `/process-audio`
Main endpoint for audio processing.

**Flow:**
1. Audio → Whisper (Transcription)
2. Transcript → MCP Server (Extraction + Excel Lookup)
3. Response Generation + TTS

**Response:**
```json
{
  "transcript": "...",
  "mobile_number": "9876543210",
  "order_id": "AMZ12345",
  "customer_name": "John Doe",
  "topic": "Order Status",
  "intent": "check_status",
  "status_found": true,
  "order_status": {
    "status": "Shipped",
    "delivery_date": "2025-11-15",
    "last_update": "2025-11-14 10:30:00"
  },
  "response_text": "...",
  "response_voice_text": "...",
  "audio_url": "/audio/abc123.mp3"
}
```

## Excel File Format

The Excel file (`data/orders.xlsx`) should have these columns:
- MobileNumber
- OrderID
- CustomerName
- OrderStatus
- DeliveryDate
- LastUpdate

## MCP Server Features

- **Text Extraction**: Uses GPT-4o to extract mobile number, order ID, customer name, topic, intent
- **Excel Lookup**: Searches orders by mobile number or order ID
- **Response Generation**: Creates appropriate responses based on lookup results
- **Error Handling**: Handles missing data gracefully

