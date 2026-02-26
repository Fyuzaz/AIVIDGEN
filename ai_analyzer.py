from pydantic import BaseModel
from typing import List, Optional
import json
import logging

logger = logging.getLogger("Processor")

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

    def analyze_transcript(self, transcript_data: dict, heatmap: Optional[List[dict]] = None) -> VideoAnalysis:
        """
        Analyzes the transcript and optional heatmap to find highlights.
        """
        if heatmap:
            logger.info("Heatmap data found. Using peak detection.")
            return self._analyze_with_heatmap(transcript_data, heatmap)
        
        logger.info("No heatmap data available. Using transcript-based logic.")
        return self._analyze_with_transcript_logic(transcript_data)

    def _analyze_with_heatmap(self, transcript_data: dict, heatmap: List[dict]) -> VideoAnalysis:
        """
        Uses YouTube heatmap data to find local peaks of engagement.
        """
        # 1. Find local peaks
        peaks = []
        for i in range(1, len(heatmap) - 1):
            if heatmap[i]['value'] > heatmap[i-1]['value'] and heatmap[i]['value'] > heatmap[i+1]['value']:
                peaks.append(heatmap[i])
        
        # If no local peaks found, use sorted values
        if not peaks:
            peaks = sorted(heatmap, key=lambda x: x['value'], reverse=True)
        else:
            peaks = sorted(peaks, key=lambda x: x['value'], reverse=True)
            
        highlights = []
        used_ranges = []
        
        # 2. Select top 3 non-overlapping peaks
        for peak in peaks:
            if len(highlights) >= 3:
                break
                
            peak_time = peak['start_time']
            
            # Distance check (ensure moments are distinct)
            if any(abs(peak_time - start) < 60 for start, end in used_ranges):
                continue
            
            # Window: 10s before, 15-20s after (classic Short length)
            h_start = max(0, peak_time - 10)
            h_end = peak_time + 20
            
            text = self._get_transcript_window(transcript_data, h_start, h_end)
            
            highlights.append(Highlight(
                start_time=h_start,
                end_time=h_end,
                reason=f"Engagement peak (Score: {peak['value']:.2f})",
                transcript_text=text
            ))
            used_ranges.append((h_start, h_end))
            
        return VideoAnalysis(highlights=highlights)

    def _analyze_with_transcript_logic(self, transcript_data: dict) -> VideoAnalysis:
        """
        Fallback logic: Score segments by high-energy keywords/laughter.
        """
        segments = transcript_data.get("segments", [])
        if not segments:
            return VideoAnalysis(highlights=[])

        duration = segments[-1]["end"]
        
        # Keyword scoring
        keywords = ["wow", "amazing", "incredible", "laughter", "look", "best", "unbelievable"]
        scores = []
        
        # Group segments into 30s chunks and score them
        for start_t in range(0, int(duration), 30):
            end_t = start_t + 30
            text = self._get_transcript_window(transcript_data, start_t, end_t)
            score = sum(1 for kw in keywords if kw in text.lower())
            scores.append({"start": start_t, "end": end_t, "score": score, "text": text})
            
        # Select target segments (Intro + top scored chunks)
        sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        
        final_highlights = []
        # Always take the intro (first 30s)
        final_highlights.append(Highlight(
            start_time=0.0,
            end_time=min(30.0, duration),
            reason="Opening moment",
            transcript_text=self._get_transcript_window(transcript_data, 0, 30)
        ))
        
        # Take up to 2 other high-score chunks
        for item in sorted_scores:
            if len(final_highlights) >= 3:
                break
            if item["start"] >= 30: # Don't duplicate intro
                final_highlights.append(Highlight(
                    start_time=float(item["start"]),
                    end_time=float(item["end"]),
                    reason="Engagement spike by audio analysis",
                    transcript_text=item["text"]
                ))

        return VideoAnalysis(highlights=final_highlights)

    def _get_transcript_window(self, transcript_data: dict, start: float, end: float) -> str:
        segments = transcript_data.get("segments", [])
        text_parts = [
            seg["text"].strip() 
            for seg in segments 
            if seg["start"] < end and seg["end"] > start
        ]
        return " ".join(text_parts)

if __name__ == "__main__":
    pass
