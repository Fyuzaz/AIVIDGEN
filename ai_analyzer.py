from pydantic import BaseModel
from typing import List, Optional
import json

class Highlight(BaseModel):
    start_time: float
    end_time: float
    reason: str
    transcript_text: str

class VideoAnalysis(BaseModel):
    highlights: List[Highlight]

class AIAnalyzer:
    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini"):
        self.api_key = api_key
        self.provider = provider

    def analyze_transcript(self, transcript_data: dict) -> VideoAnalysis:
        """
        Analyzes the transcript to find highlights.
        Currently uses a simple logic or mock if no API key is provided.
        """
        # In a real scenario, we would send the transcript with timestamps to an LLM.
        # Here's how the prompt would look:
        # "Identify the most engaging segments of this video for a Short. 
        # Return a JSON list of objects with start_time, end_time, and reason."

        if not self.api_key:
            print("Warning: No AI API key provided. Using mock analysis.")
            return self._mock_analysis(transcript_data)
        
        # Implementation for Gemini/OpenAI would go here
        return self._mock_analysis(transcript_data)

    def _mock_analysis(self, transcript_data: dict) -> VideoAnalysis:
        # Just pick the first 30 seconds as a highlight for now
        segments = transcript_data.get("segments", [])
        if not segments:
            return VideoAnalysis(highlights=[])

        # Simple logic: take the first 30 seconds
        highlight_text = ""
        end_time = 0
        for seg in segments:
            if seg["end"] <= 30:
                highlight_text += seg["text"] + " "
                end_time = seg["end"]
            else:
                break
        
        return VideoAnalysis(highlights=[
            Highlight(
                start_time=0.0,
                end_time=end_time or 30.0,
                reason="First 30 seconds of the video (Auto-generated highlight)",
                transcript_text=highlight_text.strip()
            )
        ])

if __name__ == "__main__":
    # Quick test
    # analyzer = AIAnalyzer()
    # mock_data = {"segments": [{"start": 0, "end": 10, "text": "Hello world"}, {"start": 10, "end": 20, "text": "This is a test"}]}
    # print(analyzer.analyze_transcript(mock_data))
    pass
