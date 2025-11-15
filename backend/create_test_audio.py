"""
Script to create test audio files for Order Status AI system
Generates two audio files using Murf TTS API
"""
import os
from murf import Murf
import requests

# Initialize Murf client
client = Murf(
    api_key=os.getenv("MURF_API_KEY", "ap2_1e0bb4d0-233f-472b-88d0-68cd063e8c18")
)

def create_audio_file(text: str, filename: str, voice_id: str = "en-US-terrell"):
    """
    Create audio file from text using Murf TTS
    
    Args:
        text: Text to convert to speech
        filename: Output filename
        voice_id: Murf voice ID (e.g., "en-US-terrell", "en-US-male-1", etc.)
    """
    try:
        print(f"Generating audio: {filename}...")
        
        # Generate speech using Murf
        res = client.text_to_speech.generate(
            text=text,
            voice_id=voice_id,
        )
        
        # Get audio file URL from response
        audio_url = res.audio_file
        
        if not audio_url:
            print(f"[ERROR] No audio file URL returned for {filename}")
            return None
        
        # Download the audio file
        print(f"Downloading audio from: {audio_url}")
        audio_response = requests.get(audio_url)
        audio_response.raise_for_status()
        
        # Create test_audio directory if it doesn't exist
        os.makedirs("test_audio", exist_ok=True)
        
        # Save audio file
        file_path = os.path.join("test_audio", filename)
        with open(file_path, 'wb') as audio_file:
            audio_file.write(audio_response.content)
        
        print(f"[OK] Created: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"[ERROR] Error creating {filename}: {str(e)}")
        return None

def main():
    """Generate test audio files"""
    
    print("=" * 60)
    print("Creating Test Audio Files for Order Status AI System")
    print("=" * 60)
    
    # Audio File 1: Matching Order Data
    audio1_text = """Hello, my name is Rahul Sharma. My mobile number is nine eight seven six five four three two one zero.
My order ID is A M Z one two three four five. I want to know the status of my Amazon order.
Please check and tell me when it will be delivered."""
    
    audio1_file = create_audio_file(
        text=audio1_text,
        filename="test_audio_1_matching_order.wav",
        voice_id="en-US-terrell"
    )
    
    print()
    
    # Audio File 2: Not Matching Order Data
    audio2_text = """Hi, this is Priya speaking. My mobile number is nine nine zero zero one one two two three three.
My order ID is X Y Z nine nine nine nine. Please tell me the status of my order.
I need an update urgently."""
    
    audio2_file = create_audio_file(
        text=audio2_text,
        filename="test_audio_2_not_matching.wav",
        voice_id="en-US-terrell"  # Using same voice, or you can use another valid Murf voice ID
    )
    
    print()
    print("=" * 60)
    print("Audio Files Created Successfully!")
    print("=" * 60)
    print(f"Location: test_audio/")
    print()
    print("Audio File 1: test_audio_1_matching_order.wav")
    print("  - Customer: Rahul Sharma")
    print("  - Mobile: 9876543210")
    print("  - Order ID: AMZ12345")
    print("  - Expected: Order FOUND in Excel")
    print()
    print("Audio File 2: test_audio_2_not_matching.wav")
    print("  - Customer: Priya")
    print("  - Mobile: 9900112233")
    print("  - Order ID: XYZ9999")
    print("  - Expected: Order NOT FOUND message")
    print()
    print("Tip: Make sure Excel file has Rahul Sharma's order record!")
    print("   Run: python create_sample_excel.py")

if __name__ == "__main__":
    main()

