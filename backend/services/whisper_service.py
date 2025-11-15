"""
Whisper Service for Audio/Video Transcription
Handles speech-to-text conversion using OpenAI Whisper
"""
import whisper
import tempfile
import os
from typing import Dict, Optional

class WhisperService:
    """Service for transcribing audio/video files using Whisper"""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_name: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)
        print(f"Whisper model loaded successfully")
    
    def transcribe_file(self, file_path: str) -> Dict[str, any]:
        """
        Transcribe audio/video file
        
        Args:
            file_path: Path to audio/video file
            
        Returns:
            dict with transcription result containing 'text' key
        """
        try:
            print(f"Transcribing file: {file_path}")
            result = self.model.transcribe(file_path)
            return result
        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            raise
    
    def transcribe_audio_content(self, audio_content: bytes, file_extension: str = ".wav") -> str:
        """
        Transcribe audio content from bytes
        
        Args:
            audio_content: Audio file content as bytes
            file_extension: File extension for temporary file
            
        Returns:
            Transcribed text
        """
        temp_path = None
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp:
                temp.write(audio_content)
                temp_path = temp.name
            
            # Transcribe
            result = self.transcribe_file(temp_path)
            return result.get("text", "")
        
        finally:
            # Clean up temporary file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    print(f"Error deleting temp file: {str(e)}")

