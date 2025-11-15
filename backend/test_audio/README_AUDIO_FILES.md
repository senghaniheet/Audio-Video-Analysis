# Test Audio Files

## Location
`backend/test_audio/`

## Files Required

### 1. test_audio_1_matching_order.wav
**Content:**
- Customer Name: Rahul Sharma
- Mobile Number: 9876543210
- Order ID: AMZ12345
- **Expected:** Order FOUND in Excel

**Text to speak:**
```
Hello, my name is Rahul Sharma. My mobile number is nine eight seven six five four three two one zero.
My order ID is A M Z one two three four five. I want to know the status of my Amazon order.
Please check and tell me when it will be delivered.
```

### 2. test_audio_2_not_matching.wav
**Content:**
- Customer Name: Priya
- Mobile Number: 9900112233
- Order ID: XYZ9999
- **Expected:** Order NOT FOUND message

**Text to speak:**
```
Hi, this is Priya speaking. My mobile number is nine nine zero zero one one two two three three.
My order ID is X Y Z nine nine nine nine. Please tell me the status of my order.
I need an update urgently.
```

## How to Generate

**Option 1: Using Script (Requires OpenAI API Key)**
```bash
cd backend
$env:OPENAI_API_KEY="your_api_key_here"
py create_test_audio.py
```

**Option 2: Manual Recording**
1. Use Windows Voice Recorder or online TTS tools
2. Record the text above for each file
3. Save as WAV format in this folder

**Option 3: Online TTS Tools**
- https://elevenlabs.io/
- https://ttsmaker.com/
- https://www.naturalreaders.com/

## Note
The placeholder files will be replaced when you run the script with a valid OpenAI API key.

