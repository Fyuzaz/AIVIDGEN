import yt_dlp
import os
import uuid

class Downloader:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_video(self, url: str) -> str:
        """
        Downloads a video from a URL and returns the path to the downloaded file.
        """
        job_id = str(uuid.uuid4())
        output_template = os.path.join(self.download_dir, f"{job_id}.%(ext)s")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Ensure we return the merged filename if applicable
            return filename

if __name__ == "__main__":
    # Quick test
    dl = Downloader()
    # test_url = "https://www.youtube.com/shorts/..." # Need a real link to test
    # print(dl.download_video(test_url))
