from downloader import Downloader
from transcriber import Transcriber
from ai_analyzer import AIAnalyzer
from editor import VideoEditor
import os
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Processor")

class VideoProcessor:
    def __init__(self, api_key: str = None):
        self.downloader = Downloader()
        self.transcriber = Transcriber()
        self.analyzer = AIAnalyzer(api_key=api_key)
        self.editor = VideoEditor()

    def process_url(self, url: str):
        """
        Full pipeline: Download -> Transcribe -> Analyze -> Edit
        """
        logger.info(f"Starting process for URL: {url}")
        
        # 1. Download
        video_path = self.downloader.download_video(url)
        job_id = os.path.basename(video_path).split('.')[0]
        
        try:
            # 2. Transcribe
            logger.info(f"[{job_id}] Starting transcription...")
            transcript_data = self.transcriber.transcribe(video_path)
            
            # 3. Analyze
            logger.info(f"[{job_id}] Analyzing transcript...")
            analysis = self.analyzer.analyze_transcript(transcript_data)
            
            # 4. Edit
            shorts = []
            logger.info(f"[{job_id}] Generating {len(analysis.highlights)} shorts...")
            for i, highlight in enumerate(analysis.highlights):
                short_path = self.editor.process_highlight(video_path, highlight, job_id, i)
                shorts.append({
                    "path": short_path,
                    "reason": highlight.reason,
                    "transcript": highlight.transcript_text
                })
            
            logger.info(f"[{job_id}] Process completed successfully.")
            return {
                "job_id": job_id,
                "shorts": shorts
            }
        
        except Exception as e:
            logger.error(f"[{job_id}] Error in pipeline: {e}", exc_info=True)
            raise
            
        finally:
            # Cleanup source video to save space
            if os.path.exists(video_path):
                logger.info(f"[{job_id}] Cleaning up source video: {video_path}")
                os.remove(video_path)

if __name__ == "__main__":
    pass
