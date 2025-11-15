# Setup OpenAI API Key

## To Generate Test Audio Files

You need to set your OpenAI API key before running the script.

### Step 1: Get Your API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Create a new API key
4. Copy the key

### Step 2: Set the API Key

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

**macOS/Linux:**
```bash
export OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Run the Script
```bash
cd backend
py create_test_audio.py
```

### Alternative: Set in Script
You can also edit `create_test_audio.py` and replace:
```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))
```
with:
```python
client = OpenAI(api_key="sk-your-actual-api-key-here")
```

## Note
The API key is needed to generate TTS audio files. If you don't have an API key, you can:
1. Record the audio manually using the text provided in `GENERATE_TEST_AUDIO.md`
2. Use online TTS tools like https://elevenlabs.io/ or https://ttsmaker.com/

