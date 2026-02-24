import whisper
import os

class Transcriber:
    _model_instance = None
    _current_model_name = None

    def __init__(self, model_name="base"):
        self.model_name = model_name

    def load_model(self):
        if Transcriber._model_instance is None or Transcriber._current_model_name != self.model_name:
            print(f"Loading Whisper model: {self.model_name}...")
            Transcriber._model_instance = whisper.load_model(self.model_name)
            Transcriber._current_model_name = self.model_name
        return Transcriber._model_instance

    def transcribe(self, audio_path: str):
        """
        Transcribes the audio file and returns the transcript with segments.
        """
        model = self.load_model()
        print(f"Transcribing {audio_path}...")
        result = model.transcribe(audio_path, verbose=False)
        return result

if __name__ == "__main__":
    # Quick test
    # t = Transcriber()
    # result = t.transcribe("path/to/audio/or/video.mp4")
    # print(result["text"])
    pass
