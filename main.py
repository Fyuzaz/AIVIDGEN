from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
import logging
from processor import VideoProcessor
from downloader import Downloader

logger = logging.getLogger("API")

app = FastAPI(title="AI Shorts Generator")

# In-memory storage
jobs = {}
info_cache = {}  # URL → {info, captions, video_url} — avoids redundant API calls

# Ensure directories exist
for d in ("downloads", "outputs", "static", "logs", "overlays"):
    os.makedirs(d, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
app.mount("/overlays", StaticFiles(directory="overlays"), name="overlays")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# --- Models ---

class PreviewRequest(BaseModel):
    url: str

class VideoRequest(BaseModel):
    url: str
    api_key: Optional[str] = None
    crop_x: Optional[float] = None
    crop_y: Optional[float] = None
    sub_style: Optional[str] = "classico"
    overlay_video: Optional[str] = None

class SegmentInput(BaseModel):
    start: float
    end: float

class ManualProcessRequest(BaseModel):
    url: str
    segments: List[SegmentInput]
    crop_x: Optional[float] = None
    crop_y: Optional[float] = None
    sub_style: Optional[str] = "classico"
    overlay_video: Optional[str] = None

class JobStatus(BaseModel):
    job_id: str
    status: str
    shorts: List[dict] = []
    error: Optional[str] = None

# Singleton processor
processor_instance = VideoProcessor()

# --- Helpers ---

def _get_or_extract_info(url: str):
    """Returns cached info or extracts fresh. Avoids duplicate YouTube calls."""
    if url in info_cache and "info" in info_cache[url]:
        logger.info("Using cached video info")
        return info_cache[url]["info"]
    downloader = Downloader()
    info = downloader.extract_info(url)
    info_cache.setdefault(url, {})["info"] = info
    return info

def _run_job(job_id: str, func, *args, **kwargs):
    """Generic job runner — eliminates try/except duplication."""
    try:
        result = func(*args, **kwargs)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["shorts"] = result["shorts"]
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

def _resolve_overlay(overlay_name: str | None) -> str | None:
    """Resolves overlay video name to file path."""
    if not overlay_name or overlay_name == "none":
        return None
    path = os.path.join("overlays", overlay_name)
    if os.path.exists(path):
        return path
    return None

# --- Endpoints ---

@app.post("/load")
async def load_video(request: PreviewRequest):
    """Downloads the full video for the browser player + caches info."""
    try:
        info = _get_or_extract_info(request.url)
        downloader = Downloader()

        title = info.get("title", "Unknown")
        duration = info.get("duration", 0)
        width = info.get("width", 1920)
        height = info.get("height", 1080)

        # Download video for playback (720p for speed)
        video_id = uuid.uuid4().hex[:8]
        output_path = os.path.join("downloads", f"player_{video_id}.mp4")

        import yt_dlp
        ydl_opts = {
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'retries': 5,
            'socket_timeout': 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])

        # Resolve potential filename mismatch from yt-dlp
        if not os.path.exists(output_path):
            output_path = _find_output_file(output_path) or output_path

        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Falha ao baixar o vídeo")

        # Cache captions for later use in /process-manual
        captions = downloader.get_youtube_captions(info) or []
        info_cache.setdefault(request.url, {})["captions"] = captions

        logger.info(f"Video loaded: {title} ({duration}s)")

        return {
            "video_url": f"/downloads/player_{video_id}.mp4",
            "title": title,
            "duration": duration,
            "width": width,
            "height": height,
            "captions": captions
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Load video failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/preview")
async def preview_video(request: PreviewRequest):
    """Extracts a thumbnail for crop selection."""
    try:
        info = _get_or_extract_info(request.url)

        # Find best thumbnail
        thumbnails = info.get("thumbnails", [])
        thumb_url = None
        if thumbnails:
            best = sorted(thumbnails, key=lambda t: t.get("width", 0) or 0, reverse=True)
            thumb_url = best[0].get("url")
        thumb_url = thumb_url or info.get("thumbnail")

        if not thumb_url:
            raise HTTPException(status_code=400, detail="Thumbnail não encontrada")

        import urllib.request
        preview_filename = f"preview_{uuid.uuid4().hex[:8]}.jpg"
        preview_path = os.path.join("outputs", preview_filename)

        req = urllib.request.Request(thumb_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(preview_path, "wb") as f:
                f.write(resp.read())

        return {
            "preview_url": f"/outputs/{preview_filename}",
            "video_width": info.get("width", 1920),
            "video_height": info.get("height", 1080),
            "title": info.get("title", "Unknown"),
            "duration": info.get("duration", 0)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Preview failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process", response_model=JobStatus)
async def process_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """AI-powered: analyze transcript and auto-select best moments."""
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "shorts": [], "error": None}

    if request.api_key:
        processor_instance.analyzer.api_key = request.api_key

    overlay_path = _resolve_overlay(request.overlay_video)

    background_tasks.add_task(
        _run_job, job_id, processor_instance.process_url,
        request.url, request.crop_x, request.crop_y,
        sub_style=request.sub_style or "classico",
        overlay_path=overlay_path
    )
    return {"job_id": job_id, "status": "processing"}


@app.post("/process-manual", response_model=JobStatus)
async def process_manual(request: ManualProcessRequest, background_tasks: BackgroundTasks):
    """Manual: process user-selected segments only."""
    if not request.segments:
        raise HTTPException(status_code=400, detail="Nenhum segmento selecionado")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "shorts": [], "error": None}

    segments = [{"start": s.start, "end": s.end} for s in request.segments]
    cached = info_cache.get(request.url, {})
    overlay_path = _resolve_overlay(request.overlay_video)

    background_tasks.add_task(
        _run_job, job_id, processor_instance.process_manual_segments,
        request.url, segments,
        crop_x=request.crop_x, crop_y=request.crop_y,
        cached_info=cached.get("info"),
        cached_captions=cached.get("captions"),
        sub_style=request.sub_style or "classico",
        overlay_path=overlay_path
    )
    return {"job_id": job_id, "status": "processing"}


@app.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, **jobs[job_id]}


@app.get("/subtitle-styles")
async def get_subtitle_styles():
    """Returns available subtitle style presets."""
    from editor import SUBTITLE_STYLES
    styles = {k: {"label": v["label"]} for k, v in SUBTITLE_STYLES.items()}
    styles["none"] = {"label": "Sem Legenda"}
    return {"styles": styles}


@app.get("/overlay-list")
async def list_overlays():
    """Lists available overlay videos in the overlays/ directory."""
    overlay_dir = "overlays"
    videos = []
    if os.path.exists(overlay_dir):
        for f in os.listdir(overlay_dir):
            if f.lower().endswith((".mp4", ".webm", ".mkv", ".avi")):
                videos.append({
                    "name": f,
                    "label": os.path.splitext(f)[0].replace("_", " ").replace("-", " ").title(),
                    "url": f"/overlays/{f}",
                })
    return {"overlays": videos}


# Overlay upload
from fastapi import UploadFile, File

@app.post("/upload-overlay-file")
async def upload_overlay_file(file: UploadFile = File(...)):
    """Upload a custom overlay video file."""
    allowed_exts = {".mp4", ".webm", ".mkv", ".avi"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Formato não suportado: {ext}")

    safe_name = f"custom_{uuid.uuid4().hex[:6]}{ext}"
    save_path = os.path.join("overlays", safe_name)

    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    logger.info(f"Overlay uploaded: {safe_name} ({len(content)} bytes)")
    return {"name": safe_name, "label": "Custom Upload", "url": f"/overlays/{safe_name}"}


@app.get("/export-package/{job_id}/{index}")
async def export_package(job_id: str, index: int):
    """Downloads a ZIP with separated elements for external editing."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job não encontrado")

    job = jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job ainda não foi concluído")

    shorts = job.get("shorts", [])
    if index < 0 or index >= len(shorts):
        raise HTTPException(status_code=404, detail="Short não encontrado")

    short = shorts[index]
    elements_dir = short.get("elements_dir", "")

    if not elements_dir or not os.path.isdir(elements_dir):
        raise HTTPException(status_code=404, detail="Pacote de elementos não encontrado")

    import zipfile
    import io

    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(elements_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, elements_dir)
                zf.write(file_path, arcname)

    zip_buffer.seek(0)
    zip_filename = f"short_{index}_editing_package.zip"

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{zip_filename}"'}
    )


@app.get("/trending")
async def get_trending(q: str = "podcast em alta"):
    """Searches YouTube for trending podcast videos using yt-dlp."""
    try:
        import yt_dlp

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': 'in_playlist',
            'playlistend': 20,
        }

        search_url = f"ytsearch20:{q}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(search_url, download=False)

        videos = []
        for entry in results.get("entries", []):
            if not entry:
                continue

            # Format duration
            dur = int(entry.get("duration") or 0)
            if dur > 3600:
                dur_str = f"{dur // 3600}h{(dur % 3600) // 60:02d}m"
            elif dur > 0:
                dur_str = f"{dur // 60}:{dur % 60:02d}"
            else:
                dur_str = ""

            # Format view count
            views = entry.get("view_count") or 0
            if views >= 1_000_000:
                views_str = f"{views / 1_000_000:.1f}M"
            elif views >= 1_000:
                views_str = f"{views / 1_000:.0f}K"
            elif views > 0:
                views_str = str(views)
            else:
                views_str = ""

            videos.append({
                "id": entry.get("id", ""),
                "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                "title": entry.get("title", "Sem título"),
                "channel": entry.get("channel") or entry.get("uploader") or "",
                "thumbnail": entry.get("thumbnails", [{}])[-1].get("url") if entry.get("thumbnails") else f"https://i.ytimg.com/vi/{entry.get('id', '')}/hqdefault.jpg",
                "duration": dur_str,
                "duration_seconds": dur,
                "views": views_str,
            })

        logger.info(f"Trending search '{q}': {len(videos)} results")
        return {"videos": videos, "query": q}

    except Exception as e:
        logger.error(f"Trending search failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def _find_output_file(expected_path: str) -> str | None:
    """Resolves yt-dlp filename mismatches (it may change the extension)."""
    base = os.path.splitext(expected_path)[0]
    for ext in (".mp4", ".mkv", ".webm"):
        candidate = base + ext
        if os.path.exists(candidate):
            if candidate != expected_path:
                import shutil
                shutil.move(candidate, expected_path)
            return expected_path
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
