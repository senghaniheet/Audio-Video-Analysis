# Generate Test Audio Files

## Quick Setup

### Step 1: Set OpenAI API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_openai_api_key_here"

# Windows CMD  
set OPENAI_API_KEY=your_openai_api_key_here

# macOS/Linux
export OPENAI_API_KEY=your_openai_api_key_here
```

### Step 2: Run the Script
```bash
cd backend
python create_test_audio.py
```

This will create two files in `backend/test_audio/`:
- `test_audio_1_matching_order.mp3`
- `test_audio_2_not_matching.mp3`

## Alternative: Manual Recording

If you don't have OpenAI API access, you can record the audio manually:

### Audio File 1: test_audio_1_matching_order.mp3
**Text to speak:**
```
Hello, my name is Rahul Sharma. My mobile number is nine eight seven six five four three two one zero.
My order ID is A M Z one two three four five. I want to know the status of my Amazon order.
Please check and tell me when it will be delivered.
```

### Audio File 2: test_audio_2_not_matching.mp3
**Text to speak:**
```
Hi, this is Priya speaking. My mobile number is nine nine zero zero one one two two three three.
My order ID is X Y Z nine nine nine nine. Please tell me the status of my order.
I need an update urgently.
```

**Recording Tools:**
- Windows: Voice Recorder app
- Online: https://online-voice-recorder.com/
- Phone: Use your phone's voice recorder

Save files as MP3 or WAV format in `backend/test_audio/` folder.

## File Details

### File 1: Matching Order
- **Customer:** Rahul Sharma
- **Mobile:** 9876543210
- **Order ID:** AMZ12345
- **Expected:** Order FOUND ✅

### File 2: Not Matching
- **Customer:** Priya
- **Mobile:** 9900112233
- **Order ID:** XYZ9999
- **Expected:** Order NOT FOUND ❌

## Testing

1. Ensure Excel has Rahul's order:
   ```bash
   python create_sample_excel.py
   ```

2. Start backend:
   ```bash
   python main.py
   ```

3. Upload audio files via frontend at http://localhost:4200

