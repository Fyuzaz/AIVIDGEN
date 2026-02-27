import os
import subprocess
import logging
import shutil

logger = logging.getLogger("Processor")

# =============================================
# Subtitle Style Presets (ASS format)
# =============================================
# ASS Color format: &HAABBGGRR (hex, alpha-blue-green-red)
# BorderStyle: 1=outline+shadow, 3=opaque box
SUBTITLE_STYLES = {
    "classico": {
        "label": "Clássico",
        "fontname": "Arial",
        "fontsize_ratio": 0.048,
        "primary": "&H00FFFFFF",     # White
        "outline_color": "&H00000000", # Black
        "back_color": "&H80000000",
        "bold": -1,
        "border_style": 1,
        "outline": 3,
        "shadow": 1,
        "alignment": 2,  # Bottom center
        "uppercase": True,
        "fade": "\\fad(150,100)",
    },
    "neon": {
        "label": "Neon",
        "fontname": "Arial",
        "fontsize_ratio": 0.05,
        "primary": "&H00FFFF00",     # Cyan (BGR)
        "outline_color": "&H00FF0000", # Blue glow
        "back_color": "&H00000000",
        "bold": -1,
        "border_style": 1,
        "outline": 4,
        "shadow": 2,
        "alignment": 2,
        "uppercase": True,
        "fade": "\\fad(100,100)",
    },
    "caixa": {
        "label": "Caixa",
        "fontname": "Arial",
        "fontsize_ratio": 0.042,
        "primary": "&H00FFFFFF",     # White
        "outline_color": "&H00000000",
        "back_color": "&HC0000000",  # Semi-transparent black box
        "bold": -1,
        "border_style": 3,          # Opaque box
        "outline": 2,
        "shadow": 0,
        "alignment": 2,
        "uppercase": False,
        "fade": "",
    },
    "impacto": {
        "label": "Impacto",
        "fontname": "Impact",
        "fontsize_ratio": 0.065,
        "primary": "&H0000FFFF",     # Yellow (BGR)
        "outline_color": "&H00000000",
        "back_color": "&H80000000",
        "bold": -1,
        "border_style": 1,
        "outline": 4,
        "shadow": 2,
        "alignment": 2,
        "uppercase": True,
        "fade": "\\fad(80,80)",
    },
    "minimalista": {
        "label": "Minimalista",
        "fontname": "Arial",
        "fontsize_ratio": 0.035,
        "primary": "&H00FFFFFF",
        "outline_color": "&H00000000",
        "back_color": "&H00000000",
        "bold": 0,
        "border_style": 1,
        "outline": 1,
        "shadow": 0,
        "alignment": 2,
        "uppercase": False,
        "fade": "\\fad(200,150)",
    },
}


class VideoEditor:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_ass_subtitle(self, segments: list, video_width: int, video_height: int,
                               style_name: str = "classico") -> str:
        """Generates ASS subtitle file with the specified style preset."""
        ass_path = os.path.join(self.output_dir, f"subs_{os.getpid()}.ass")
        style = SUBTITLE_STYLES.get(style_name, SUBTITLE_STYLES["classico"])

        font_size = max(24, int(video_height * style["fontsize_ratio"]))
        margin_bottom = int(video_height * 0.12)

        ass_content = f"""[Script Info]
Title: AI Shorts Subtitles
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style['fontname']},{font_size},{style['primary']},&H000000FF,{style['outline_color']},{style['back_color']},{style['bold']},0,0,0,100,100,0,0,{style['border_style']},{style['outline']},{style['shadow']},{style['alignment']},40,40,{margin_bottom},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        # Trim overlapping segments
        for i in range(len(segments) - 1):
            if segments[i]["end"] > segments[i + 1]["start"]:
                segments[i]["end"] = segments[i + 1]["start"]

        for seg in segments:
            text = seg["text"].strip()
            if not text:
                continue

            start = self._seconds_to_ass_time(seg["start"])
            end = self._seconds_to_ass_time(seg["end"])

            text = text.replace("\\", "\\\\")
            text = text.replace("{", "\\{").replace("}", "\\}")

            if style.get("uppercase"):
                text = text.upper()

            fade = style.get("fade", "")
            prefix = f"{{{fade}}}" if fade else ""
            ass_content += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{prefix}{text}\n"

        with open(ass_path, "w", encoding="utf-8-sig") as f:
            f.write(ass_content)

        logger.info(f"Generated ASS subtitle ({style_name}): {len(segments)} entries")
        return ass_path

    @staticmethod
    def _seconds_to_ass_time(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    def get_video_dimensions(self, video_path: str) -> tuple:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0:s=x",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        w, h = result.stdout.strip().split("x")
        return int(w), int(h)

    def render_short(self, input_path: str, job_id: str, index: int,
                     segments: list = None,
                     crop_x: float = None, crop_y: float = None,
                     sub_style: str = "classico",
                     overlay_path: str = None,
                     overlay_ratio: float = 0.4) -> str:
        """
        Renders a short with crop, subtitles, and optional overlay video.
        overlay_path: path to secondary video (split-screen bottom)
        overlay_ratio: how much of the frame the overlay occupies (0-1, default 0.4)
        """
        output_path = os.path.join(self.output_dir, f"{job_id}_short_{index}.mp4")

        try:
            src_w, src_h = self.get_video_dimensions(input_path)
            out_w, out_h = 608, 1080

            if overlay_path and os.path.exists(overlay_path):
                return self._render_with_overlay(
                    input_path, output_path, src_w, src_h, out_w, out_h,
                    crop_x, crop_y, segments, sub_style,
                    overlay_path, overlay_ratio, index
                )
            else:
                return self._render_standard(
                    input_path, output_path, src_w, src_h, out_w, out_h,
                    crop_x, crop_y, segments, sub_style, index
                )

        except Exception as e:
            logger.error(f"Failed to render short {index}: {e}", exc_info=True)
            return ""

    def _calc_crop(self, src_w, src_h, crop_x, crop_y):
        """Calculate 9:16 crop dimensions and position."""
        target_ratio = 9 / 16
        if src_w / src_h > target_ratio:
            crop_h = src_h
            crop_w = int(src_h * target_ratio) // 2 * 2
        else:
            crop_w = src_w
            crop_h = int(src_w / target_ratio) // 2 * 2

        if crop_x is not None and crop_y is not None:
            cx, cy = int(crop_x * src_w), int(crop_y * src_h)
            x = max(0, min(cx - crop_w // 2, src_w - crop_w))
            y = max(0, min(cy - crop_h // 2, src_h - crop_h))
        else:
            x = (src_w - crop_w) // 2
            y = (src_h - crop_h) // 2

        return crop_w, crop_h, x, y

    def _render_standard(self, input_path, output_path, src_w, src_h, out_w, out_h,
                          crop_x, crop_y, segments, sub_style, index):
        """Standard render: crop → scale → subtitles."""
        crop_w, crop_h, x, y = self._calc_crop(src_w, src_h, crop_x, crop_y)

        filters = [
            f"crop={crop_w}:{crop_h}:{x}:{y}",
            f"scale={out_w}:{out_h}:flags=lanczos"
        ]

        ass_path = None
        if segments and sub_style != "none":
            ass_path = self.generate_ass_subtitle(segments, out_w, out_h, sub_style)
            escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
            filters.append(f"ass='{escaped_ass}'")

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", ",".join(filters),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
            output_path
        ]

        logger.info(f"Rendering short {index} (style={sub_style})...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

        if result.returncode != 0:
            logger.error(f"FFmpeg failed: {result.stderr[-500:]}")
            return self._fallback_render(input_path, output_path, crop_w, crop_h, x, y, out_w, out_h)

        if ass_path and os.path.exists(ass_path):
            os.remove(ass_path)

        logger.info(f"Short {index} rendered: {output_path}")
        return output_path

    def _render_with_overlay(self, input_path, output_path, src_w, src_h, out_w, out_h,
                              crop_x, crop_y, segments, sub_style,
                              overlay_path, overlay_ratio, index):
        """
        Split-screen render:
        - Top portion: main video (cropped to fill width)
        - Bottom portion: overlay video (looped, cropped to fill width)
        - Subtitles on top of the composite
        """
        crop_w, crop_h, x, y = self._calc_crop(src_w, src_h, crop_x, crop_y)

        # Calculate split heights
        main_h = int(out_h * (1 - overlay_ratio)) // 2 * 2
        overlay_h = out_h - main_h

        # Build filter_complex for split-screen
        # [0] = main video, [1] = overlay video
        filter_parts = [
            # Process main video: crop → scale to fill top portion
            f"[0:v]crop={crop_w}:{crop_h}:{x}:{y},scale={out_w}:{main_h}:flags=lanczos[main]",
            # Process overlay: scale to fill bottom portion, loop if shorter
            f"[1:v]scale={out_w}:{overlay_h}:flags=lanczos,setsar=1[overlay]",
            # Stack vertically
            f"[main][overlay]vstack=inputs=2[stacked]",
        ]

        # Add subtitles to the stacked result
        ass_path = None
        if segments and sub_style != "none":
            ass_path = self.generate_ass_subtitle(segments, out_w, out_h, sub_style)
            escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")
            filter_parts.append(f"[stacked]ass='{escaped_ass}'[out]")
            output_label = "[out]"
        else:
            output_label = "[stacked]"

        filter_complex = ";".join(filter_parts)

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-stream_loop", "-1",  # Loop overlay video
            "-i", overlay_path,
            "-filter_complex", filter_complex,
            "-map", output_label,
            "-map", "0:a?",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
            output_path
        ]

        logger.info(f"Rendering short {index} with overlay (style={sub_style}, ratio={overlay_ratio})...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            logger.error(f"Overlay render failed: {result.stderr[-500:]}")
            # Fallback to standard render
            logger.info("Falling back to standard render...")
            return self._render_standard(
                input_path, output_path, src_w, src_h, out_w, out_h,
                crop_x, crop_y, segments, sub_style, index
            )

        if ass_path and os.path.exists(ass_path):
            os.remove(ass_path)

        logger.info(f"Short {index} rendered with overlay: {output_path}")
        return output_path

    def export_elements(self, input_path: str, job_id: str, index: int,
                         segments: list = None,
                         crop_x: float = None, crop_y: float = None,
                         sub_style: str = "classico",
                         overlay_path: str = None,
                         overlay_ratio: float = 0.4) -> dict:
        """
        Export separated elements for external editing tools.
        Returns dict with paths to: raw_video, ass_subtitle, srt_subtitle, overlay_clip, elements_dir
        """
        elements_dir = os.path.join(self.output_dir, f"{job_id}_elements_{index}")
        os.makedirs(elements_dir, exist_ok=True)

        elements = {"elements_dir": elements_dir}

        try:
            src_w, src_h = self.get_video_dimensions(input_path)
            out_w, out_h = 608, 1080
            crop_w, crop_h, x, y = self._calc_crop(src_w, src_h, crop_x, crop_y)

            # 1. Raw video (crop + scale, NO subtitles)
            raw_video_path = os.path.join(elements_dir, "video_raw.mp4")
            cmd = [
                "ffmpeg", "-y",
                "-i", input_path,
                "-vf", f"crop={crop_w}:{crop_h}:{x}:{y},scale={out_w}:{out_h}:flags=lanczos",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
                raw_video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0:
                elements["raw_video"] = raw_video_path
                logger.info(f"Exported raw video: {raw_video_path}")
            else:
                logger.error(f"Failed to export raw video: {result.stderr[-300:]}")

            # 2. Subtitle files (ASS + SRT)
            if segments and sub_style != "none":
                ass_path = self.generate_ass_subtitle(segments, out_w, out_h, sub_style)
                ass_dest = os.path.join(elements_dir, "subtitles.ass")
                shutil.copy2(ass_path, ass_dest)
                elements["ass_subtitle"] = ass_dest

                # Convert to SRT
                srt_dest = os.path.join(elements_dir, "subtitles.srt")
                self._ass_to_srt(segments, srt_dest, sub_style)
                elements["srt_subtitle"] = srt_dest

                # Clean temp ASS
                if os.path.exists(ass_path):
                    os.remove(ass_path)

                logger.info(f"Exported subtitles: ASS + SRT")

            # 3. Overlay clip (if used)
            if overlay_path and os.path.exists(overlay_path):
                overlay_h = out_h - (int(out_h * (1 - overlay_ratio)) // 2 * 2)
                overlay_dest = os.path.join(elements_dir, "overlay.mp4")
                cmd = [
                    "ffmpeg", "-y",
                    "-i", overlay_path,
                    "-vf", f"scale={out_w}:{overlay_h}:flags=lanczos,setsar=1",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                    "-c:a", "aac", "-b:a", "128k",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-t", "60",  # Limit to 60s
                    overlay_dest
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    elements["overlay_clip"] = overlay_dest
                    logger.info(f"Exported overlay clip: {overlay_dest}")

            # 4. README
            readme_path = os.path.join(elements_dir, "README.txt")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("=== AI Shorts Generator — Pacote de Edição ===\n\n")
                f.write("Este pacote contém os elementos separados do seu short\n")
                f.write("para edição em ferramentas externas.\n\n")
                f.write("Arquivos incluídos:\n")
                f.write("  - video_raw.mp4    → Vídeo croppado 9:16 SEM legendas\n")
                if "ass_subtitle" in elements:
                    f.write("  - subtitles.ass    → Legendas (formato ASS, estilizado)\n")
                    f.write("  - subtitles.srt    → Legendas (formato SRT, universal)\n")
                if "overlay_clip" in elements:
                    f.write("  - overlay.mp4      → Vídeo overlay (parte inferior)\n")
                f.write("\nComo usar:\n")
                f.write("  1. Importe video_raw.mp4 no seu editor\n")
                f.write("  2. Importe subtitles.srt ou subtitles.ass como legenda\n")
                f.write("  3. Se tiver overlay, adicione overlay.mp4 na camada inferior\n")
                f.write(f"\nResolução: {out_w}x{out_h} (9:16)\n")
            elements["readme"] = readme_path

            logger.info(f"Export package ready: {elements_dir}")
            return elements

        except Exception as e:
            logger.error(f"Failed to export elements for short {index}: {e}", exc_info=True)
            return elements

    def _ass_to_srt(self, segments: list, srt_path: str, style_name: str = "classico"):
        """Convert subtitle segments to SRT format."""
        style = SUBTITLE_STYLES.get(style_name, SUBTITLE_STYLES["classico"])
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                text = seg["text"].strip()
                if not text:
                    continue
                if style.get("uppercase"):
                    text = text.upper()
                start = self._seconds_to_srt_time(seg["start"])
                end = self._seconds_to_srt_time(seg["end"])
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        logger.info(f"Generated SRT subtitle: {len(segments)} entries")

    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def _fallback_render(self, input_path, output_path,
                          crop_w, crop_h, x, y, out_w, out_h):
        """Fallback: crop + scale without subtitles."""
        fallback_path = output_path.replace(".mp4", "_nosub.mp4")
        logger.warning("Fallback render (no subtitles)")

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"crop={crop_w}:{crop_h}:{x}:{y},scale={out_w}:{out_h}:flags=lanczos",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
            fallback_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=120)
            return fallback_path
        except Exception as e:
            logger.error(f"Fallback render failed: {e}")
            return ""

