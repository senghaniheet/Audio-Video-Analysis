# Test Audio Files Guide

## Overview

This guide explains how to create and use test audio files for the Order Status AI system.

## Creating Test Audio Files

### Method 1: Using the Script (Recommended)

1. **Set OpenAI API Key:**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_api_key_here"

# Windows CMD
set OPENAI_API_KEY=your_api_key_here

# macOS/Linux
export OPENAI_API_KEY=your_api_key_here
```

2. **Run the script:**
```bash
cd backend
python create_test_audio.py
```

This will create two audio files in `test_audio/` folder:
- `test_audio_1_matching_order.wav` - Should find order in Excel
- `test_audio_2_not_matching.wav` - Should return NOT FOUND

### Method 2: Manual Recording

You can also record your own audio files using:
- Windows Voice Recorder
- Online TTS tools
- Your phone's voice recorder

Just make sure the audio contains the required information.

## Test Audio File 1: Matching Order

**File:** `test_audio_1_matching_order.wav`

**Content:**
- Customer Name: Rahul Sharma
- Mobile Number: 9876543210
- Order ID: AMZ12345

**Expected Result:**
- ✅ Order FOUND in Excel
- ✅ Status: Shipped
- ✅ Delivery date returned
- ✅ Response with order details

**Text:**
```
Hello, my name is Rahul Sharma. My mobile number is nine eight seven six five four three two one zero.
My order ID is A M Z one two three four five. I want to know the status of my Amazon order.
Please check and tell me when it will be delivered.
```

## Test Audio File 2: Not Matching Order

**File:** `test_audio_2_not_matching.wav`

**Content:**
- Customer Name: Priya
- Mobile Number: 9900112233
- Order ID: XYZ9999

**Expected Result:**
- ❌ Order NOT FOUND in Excel
- ❌ Status: Not Found
- ✅ Default "not found" message returned

**Text:**
```
Hi, this is Priya speaking. My mobile number is nine nine zero zero one one two two three three.
My order ID is X Y Z nine nine nine nine. Please tell me the status of my order.
I need an update urgently.
```

## Testing the System

1. **Ensure Excel file has test data:**
```bash
python create_sample_excel.py
```
This creates Excel with Rahul Sharma's order (AMZ12345).

2. **Start the backend:**
```bash
python main.py
```

3. **Test via Frontend:**
   - Open http://localhost:4200
   - Upload `test_audio_1_matching_order.wav`
   - Click "Check Order Status"
   - Verify: Order found, status shown

4. **Test Audio File 2:**
   - Upload `test_audio_2_not_matching.wav`
   - Verify: "Not Found" message displayed

## File Locations

```
backend/
├── test_audio/                    # Test audio files folder
│   ├── test_audio_1_matching_order.wav
│   └── test_audio_2_not_matching.wav
├── create_test_audio.py          # Script to generate audio files
└── data/
    └── orders.xlsx               # Excel with test orders
```

## Troubleshooting

**Issue: Audio files not created**
- Check OpenAI API key is set
- Verify you have API credits
- Check internet connection

**Issue: Order not found (Audio 1)**
- Run `create_sample_excel.py` to ensure Excel has the test record
- Check Excel file path in `mcp_server.py`

**Issue: Poor transcription quality**
- Use clear audio (no background noise)
- Speak slowly and clearly
- Use WAV or MP3 format

## Notes

- Audio files are ~20 seconds each
- Generated using OpenAI TTS API
- Can be replaced with your own recordings
- Supported formats: WAV, MP3, MP4, M4A

