# Backend Setup Instructions

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set OpenAI API Key:**
   - Option 1: Set environment variable:
     ```bash
     # Windows PowerShell
     $env:OPENAI_API_KEY="your_api_key_here"
     
     # Windows CMD
     set OPENAI_API_KEY=your_api_key_here
     
     # macOS/Linux
     export OPENAI_API_KEY=your_api_key_here
     ```
   
   - Option 2: Install python-dotenv and create `.env` file:
     ```bash
     pip install python-dotenv
     ```
     Then create `.env` file with:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
     And update `main.py` to load it:
     ```python
     from dotenv import load_dotenv
     load_dotenv()
     ```

3. **Run the server:**
```bash
python main.py
```

The server will start on `http://localhost:8000`

## Notes

- First run will download the Whisper model (~150MB for base model)
- Make sure you have sufficient OpenAI API credits
- The server supports CORS for Angular frontend on port 4200

