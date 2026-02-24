from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from processor import VideoProcessor

app = FastAPI(title="AI Shorts Generator")

# Storage for jobs (In-memory for now)
jobs = {}

# Create downloads and outputs directories if they don't exist
os.makedirs("downloads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

class VideoRequest(BaseModel):
    url: str
    api_key: Optional[str] = None

class JobStatus(BaseModel):
    job_id: str
    status: str
    shorts: List[dict] = []
    error: Optional[str] = None

# Create a single processor instance with global model loading
processor_instance = VideoProcessor()

@app.post("/process", response_model=JobStatus)
async def process_video(request: VideoRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "shorts": [], "error": None}
    
    # Update processor API key if changed (simple way for this exercise)
    if request.api_key:
        processor_instance.analyzer.api_key = request.api_key
    
    background_tasks.add_task(run_processing, job_id, request.url)
    
    return {"job_id": job_id, "status": "processing"}

@app.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, **jobs[job_id]}

def run_processing(job_id: str, url: str):
    try:
        result = processor_instance.process_url(url)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["shorts"] = result["shorts"]
    except Exception as e:
        import logging
        logger = logging.getLogger("API")
        logger.error(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
