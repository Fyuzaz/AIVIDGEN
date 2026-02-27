from downloader import Downloader
from transcriber import Transcriber
from ai_analyzer import AIAnalyzer
from editor import VideoEditor
import os
import logging

# Configure logging
class ConnectionResetFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return not ("WinError 10054" in msg or "ConnectionResetError" in msg or "BrokenPipeError" in msg)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Processor")
logger.addFilter(ConnectionResetFilter())
logging.getLogger("uvicorn.error").addFilter(ConnectionResetFilter())
logging.getLogger("asyncio").addFilter(ConnectionResetFilter())


class VideoProcessor:
    def __init__(self, api_key: str = None):
        self.downloader = Downloader()
        self.transcriber = Transcriber()
        self.analyzer = AIAnalyzer(api_key=api_key)
        self.editor = VideoEditor()

    def process_url(self, url: str, crop_x: float = None, crop_y: float = None,
                    sub_style: str = "classico", overlay_path: str = None):
        """
        AI pipeline: extract metadata → get transcript → analyze → render.
        """
        logger.info(f"=== Starting AI pipeline for: {url} ===")

        info = self.downloader.extract_info(url)
        logger.info(f"Video: '{info.get('title', '?')}' ({info.get('duration', 0)}s)")

        transcript_data = self._get_transcript(url, info)
        logger.info(f"Transcript ready: {len(transcript_data.get('segments', []))} segments")

        heatmap = info.get("heatmap")
        analysis = self.analyzer.analyze_transcript(transcript_data, heatmap=heatmap)
        logger.info(f"Found {len(analysis.highlights)} highlights")

        # Build segment list from AI analysis
        segments = [{
            "start": h.start_time,
            "end": h.end_time,
            "reason": h.reason,
        } for h in analysis.highlights]

        return self._render_segments(url, segments, transcript_data, crop_x, crop_y, sub_style, overlay_path)

    def process_manual_segments(self, url: str, segments: list,
                                 crop_x: float = None, crop_y: float = None,
                                 cached_info: dict = None, cached_captions: list = None,
                                 sub_style: str = "classico", overlay_path: str = None):
        """
        Manual pipeline: user-selected segments, no AI.
        Accepts cached_info and cached_captions to skip redundant API calls.
        """
        logger.info(f"=== Starting MANUAL pipeline for: {url} ({len(segments)} segments) ===")

        # Use cached data if available, otherwise fetch
        if cached_captions:
            transcript_data = Transcriber.youtube_captions_to_transcript_format(cached_captions)
            logger.info("Using cached captions (skipped extract_info)")
        else:
            info = cached_info or self.downloader.extract_info(url)
            transcript_data = self._get_transcript(url, info)
            logger.info(f"Transcript: {len(transcript_data.get('segments', []))} segments")

        # Add reason to segments
        render_segments = [{
            "start": s["start"],
            "end": s["end"],
            "reason": f"Manual: {s['start']:.0f}s - {s['end']:.0f}s",
        } for s in segments]

        return self._render_segments(url, render_segments, transcript_data, crop_x, crop_y, sub_style, overlay_path)

    def _render_segments(self, url: str, segments: list, transcript_data: dict,
                          crop_x: float = None, crop_y: float = None,
                          sub_style: str = "classico", overlay_path: str = None):
        """
        Unified render loop: downloads each segment and renders with FFmpeg.
        segments: list of {start, end, reason}
        """
        all_caption_segments = transcript_data.get("segments", [])
        shorts = []
        cleanup_files = []

        for i, seg in enumerate(segments):
            start, end = seg["start"], seg["end"]
            logger.info(f"[{i}] Downloading {start:.1f}s - {end:.1f}s...")

            segment_id = f"{i}_{int(start)}"
            try:
                segment_path = self.downloader.download_segment(
                    url, start, end, segment_id=segment_id
                )
            except Exception as e:
                logger.error(f"Failed to download segment {i}: {e}")
                continue

            cleanup_files.append(segment_path)

            # Extract subtitle segments relative to this clip
            sub_segments = self._extract_relative_segments(all_caption_segments, start, end)

            # Render
            job_id = os.path.basename(segment_path).split('.')[0]
            logger.info(f"[{i}] Rendering short (style={sub_style})...")

            short_path = self.editor.render_short(
                segment_path, job_id, i,
                segments=sub_segments,
                crop_x=crop_x, crop_y=crop_y,
                sub_style=sub_style,
                overlay_path=overlay_path
            )

            if short_path:
                # Export separated elements for external editing
                elements = self.editor.export_elements(
                    segment_path, job_id, i,
                    segments=sub_segments,
                    crop_x=crop_x, crop_y=crop_y,
                    sub_style=sub_style,
                    overlay_path=overlay_path
                )
                shorts.append({
                    "path": short_path,
                    "reason": seg.get("reason", ""),
                    "transcript": "",
                    "elements_dir": elements.get("elements_dir", "")
                })

        # Cleanup downloaded segments
        for f in cleanup_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass

        logger.info(f"=== Pipeline complete! {len(shorts)} shorts generated ===")
        return {"shorts": shorts}

    def _get_transcript(self, url: str, info: dict) -> dict:
        """YouTube captions (instant) → Whisper fallback (slower)."""
        yt_segments = self.downloader.get_youtube_captions(info)
        if yt_segments:
            logger.info("Using YouTube captions (no Whisper needed).")
            return Transcriber.youtube_captions_to_transcript_format(yt_segments)

        logger.info("No captions. Downloading audio for Whisper...")
        audio_path = None
        try:
            audio_path = self.downloader.download_audio_only(url)
            return self.transcriber.transcribe(audio_path)
        finally:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)

    @staticmethod
    def _extract_relative_segments(all_segments: list, start: float, end: float) -> list:
        """
        Extract and normalize subtitle segments to clip-relative timestamps.
        Accounts for the 1s padding added by download_segment.
        """
        padding = 1.0
        result = []

        for seg in all_segments:
            if seg["start"] < end and seg["end"] > start:
                s_rel = max(0, seg["start"] - start + padding)
                e_rel = seg["end"] - start + padding
                clip_duration = (end - start) + 2 * padding
                e_rel = min(clip_duration, e_rel)

                if e_rel > s_rel:
                    result.append({
                        "start": s_rel,
                        "end": e_rel,
                        "text": seg["text"].strip()
                    })

        return result
