import whisper
import os
import logging

logger = logging.getLogger("Processor")


class Transcriber:
    _model_instance = None
    _current_model_name = None

    def __init__(self, model_name="base"):
        self.model_name = model_name

    def load_model(self):
        if Transcriber._model_instance is None or Transcriber._current_model_name != self.model_name:
            logger.info(f"Loading Whisper model: {self.model_name}...")
            Transcriber._model_instance = whisper.load_model(self.model_name)
            Transcriber._current_model_name = self.model_name
        return Transcriber._model_instance

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribes an audio/video file using Whisper.
        Returns dict with 'text' and 'segments' keys.
        Only used as fallback when YouTube captions are unavailable.
        """
        model = self.load_model()
        logger.info(f"Transcribing with Whisper: {audio_path}")
        result = model.transcribe(audio_path, verbose=False, fp16=False)
        logger.info(f"Whisper transcription complete: {len(result.get('segments', []))} segments")
        return result

    @staticmethod
    def youtube_captions_to_transcript_format(caption_segments: list) -> dict:
        """
        Converts YouTube caption segments to Whisper-compatible format.
        Input:  [{"start": 0.0, "end": 3.5, "text": "Hello"}, ...]
        Output: {"text": "Hello ...", "segments": [{"start": 0.0, "end": 3.5, "text": "Hello"}, ...]}
        """
        full_text = " ".join(seg["text"] for seg in caption_segments)
        return {
            "text": full_text,
            "segments": caption_segments
        }


if __name__ == "__main__":
    pass
