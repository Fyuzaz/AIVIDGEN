import yt_dlp
import os
import uuid
import subprocess
import logging
import shutil

logger = logging.getLogger("Processor")


class Downloader:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def extract_info(self, url: str) -> dict:
        """Extracts video metadata WITHOUT downloading. Typically < 3s."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        logger.info(f"Extracted info: {info.get('title', '?')} ({info.get('duration', 0)}s)")
        return info

    def get_youtube_captions(self, info: dict, lang: str = "pt") -> list | None:
        """
        Extracts YouTube captions from metadata.
        Priority: manual subs > auto captions. Tries pt → en → pt-BR → es → any.
        """
        all_subs = {**info.get("automatic_captions", {}), **info.get("subtitles", {})}

        for try_lang in [lang, "en", "pt-BR", "es"]:
            if try_lang in all_subs:
                return self._parse_captions(all_subs[try_lang], try_lang)

        # Fallback: any available language
        if all_subs:
            first_lang = next(iter(all_subs))
            return self._parse_captions(all_subs[first_lang], first_lang)

        return None

    def _parse_captions(self, formats: list, lang: str) -> list | None:
        """Tries json3 first, then vtt."""
        for fmt in formats:
            if fmt.get("ext") == "json3":
                return self._download_and_parse_json3(fmt["url"], lang)
        for fmt in formats:
            if fmt.get("ext") == "vtt":
                return self._download_and_parse_vtt(fmt["url"], lang)
        return None

    def _download_and_parse_json3(self, url: str, lang: str) -> list | None:
        """Downloads and parses YouTube's json3 caption format."""
        import urllib.request
        import json

        try:
            logger.info(f"Downloading captions (json3, lang={lang})...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            segments = []
            for event in data.get("events", []):
                segs = event.get("segs")
                if not segs:
                    continue

                start_ms = event.get("tStartMs", 0)
                duration_ms = event.get("dDurationMs", 0)
                text = "".join(s.get("utf8", "") for s in segs).strip().replace("\n", " ")

                if text:
                    segments.append({
                        "start": start_ms / 1000.0,
                        "end": (start_ms + duration_ms) / 1000.0,
                        "text": text
                    })

            logger.info(f"Parsed {len(segments)} caption segments")
            return segments or None

        except Exception as e:
            logger.warning(f"Failed to parse json3 captions: {e}")
            return None

    def _download_and_parse_vtt(self, url: str, lang: str) -> list | None:
        """Downloads and parses VTT captions (fallback)."""
        import urllib.request
        import re

        try:
            logger.info(f"Downloading captions (vtt, lang={lang})...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                vtt_text = resp.read().decode("utf-8")

            segments = []
            pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n(.+?)(?=\n\n|\Z)'
            for start_str, end_str, text in re.findall(pattern, vtt_text, re.DOTALL):
                start = self._vtt_time_to_seconds(start_str)
                end = self._vtt_time_to_seconds(end_str)
                clean_text = re.sub(r'<[^>]+>', '', text).strip().replace("\n", " ")
                if clean_text:
                    segments.append({"start": start, "end": end, "text": clean_text})

            logger.info(f"Parsed {len(segments)} VTT segments")
            return segments or None

        except Exception as e:
            logger.warning(f"Failed to parse VTT captions: {e}")
            return None

    @staticmethod
    def _vtt_time_to_seconds(time_str: str) -> float:
        h, m, s = time_str.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    def download_segment(self, url: str, start: float, end: float, segment_id: str = None) -> str:
        """
        Downloads a specific segment using yt-dlp --download-sections.
        Falls back to full download + FFmpeg extraction if needed.
        """
        if not segment_id:
            segment_id = uuid.uuid4().hex[:8]

        output_path = os.path.join(self.download_dir, f"seg_{segment_id}.mp4")

        # Add small padding for smooth cuts
        padded_start = max(0, start - 1.0)
        padded_end = end + 1.0

        # Method 1: yt-dlp section download (fast, server-side range)
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'download_ranges': yt_dlp.utils.download_range_func(None, [(padded_start, padded_end)]),
                # NOTE: force_keyframes_at_cuts removed — causes slow re-encode
                'retries': 5,
                'fragment_retries': 5,
                'socket_timeout': 30,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Resolve filename mismatch
            if not os.path.exists(output_path):
                self._resolve_filename(output_path)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                logger.info(f"Segment downloaded: {padded_start:.1f}s-{padded_end:.1f}s")
                return output_path

        except Exception as e:
            logger.warning(f"Section download failed: {e}. Falling back.")

        # Method 2: Full download + FFmpeg extract
        return self._fallback_segment_extract(url, padded_start, padded_end, output_path)

    def _fallback_segment_extract(self, url: str, start: float, end: float, output_path: str) -> str:
        """Fallback: downloads full video, extracts segment with FFmpeg (codec copy = instant)."""
        full_path = os.path.join(self.download_dir, f"full_{uuid.uuid4().hex[:8]}.mp4")

        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
            'outtmpl': full_path,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'retries': 5,
            'socket_timeout': 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(full_path):
            self._resolve_filename(full_path)

        # Extract segment with FFmpeg (codec copy = instant)
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start), "-to", str(end),
            "-i", full_path,
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)

        # Cleanup full video
        if os.path.exists(full_path):
            os.remove(full_path)

        logger.info(f"Segment extracted via fallback: {start:.1f}s-{end:.1f}s")
        return output_path

    def download_audio_only(self, url: str, segment_id: str = None) -> str:
        """Downloads only audio (for Whisper fallback)."""
        if not segment_id:
            segment_id = uuid.uuid4().hex[:8]

        output_path = os.path.join(self.download_dir, f"audio_{segment_id}.m4a")

        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'retries': 5,
            'socket_timeout': 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(output_path):
            self._resolve_filename(output_path, [".m4a", ".webm", ".ogg", ".mp3"])

        logger.info(f"Audio downloaded: {output_path}")
        return output_path

    @staticmethod
    def _resolve_filename(expected_path: str, extensions: list = None):
        """Resolves yt-dlp filename mismatches (centralized helper)."""
        if extensions is None:
            extensions = [".mp4", ".mkv", ".webm"]
        base = os.path.splitext(expected_path)[0]
        for ext in extensions:
            candidate = base + ext
            if os.path.exists(candidate) and candidate != expected_path:
                shutil.move(candidate, expected_path)
                return
