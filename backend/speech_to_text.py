"""
Speech-to-text module using OpenAI Whisper
Handles audio transcription
"""
import whisper
import os
from typing import Optional
import tempfile

class SpeechToText:
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model
        Available sizes: tiny, base, small, medium, large
        base is good for hackathon speed/accuracy balance
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        print("Whisper model loaded successfully")
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file (wav, mp3, m4a, etc.)
            language: Optional language code (e.g., 'en', 'es')
        
        Returns:
            dict with 'text', 'language', 'segments' keys
        """
        try:
            # Transcribe
            options = {"language": language} if language else {}
            result = self.model.transcribe(audio_path, **options)
            
            return {
                "text": result["text"],
                "language": result.get("language", "unknown"),
                "segments": result.get("segments", [])
            }
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            raise
    
    def transcribe_from_bytes(self, audio_bytes: bytes, format: str = "wav") -> dict:
        """
        Transcribe audio from bytes (for API uploads)
        
        Args:
            audio_bytes: Audio file as bytes
            format: Audio format extension (wav, mp3, etc.)
        
        Returns:
            dict with transcription results
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            result = self.transcribe_audio(tmp_path)
            return result
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

# Global instance
stt = SpeechToText()
