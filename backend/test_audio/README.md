# Test Audio Files

This folder contains sample audio files for testing the Order Status AI system.

## Files

### 1. test_audio_1_matching_order.mp3
- **Customer Name:** Rahul Sharma
- **Mobile Number:** 9876543210
- **Order ID:** AMZ12345
- **Expected Result:** Order FOUND in Excel

### 2. test_audio_2_not_matching.mp3
- **Customer Name:** Priya
- **Mobile Number:** 9900112233
- **Order ID:** XYZ9999
- **Expected Result:** Order NOT FOUND message

## How to Generate These Files

Run the script:
```bash
cd backend
python create_test_audio.py
```

This will create both audio files in the `test_audio/` folder.

## Usage

1. Upload these files through the Angular frontend
2. Test the order lookup functionality
3. Verify the system correctly identifies matching and non-matching orders

