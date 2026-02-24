from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os

class VideoEditor:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def process_highlight(self, video_path: str, highlight, job_id: str, index: int) -> str:
        """
        Crops video to 9:16 and extracts the highlight segment.
        """
        output_path = os.path.join(self.output_dir, f"{job_id}_short_{index}.mp4")
        
        with VideoFileClip(video_path) as clip:
            # Extract segment with safety check on duration
            start = max(0, highlight.start_time)
            end = min(clip.duration, highlight.end_time)
            subclip = clip.subclipped(start, end)
            
            # Intelligent 9:16 Crop
            w, h = subclip.size
            target_ratio = 9/16
            
            if w/h > target_ratio:
                # Landscape -> Crop sides
                new_w = h * target_ratio
                subclip = subclip.cropped(x_center=w/2, width=new_w)
            else:
                # Portrait -> Crop top/bottom if needed
                new_h = w / target_ratio
                subclip = subclip.cropped(y_center=h/2, height=new_h)
            
            # Encode at standard 1080p, moderate bitrate for speed
            final_clip = subclip.resized(height=1080)
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                fps=24,
                logger=None # Suppress moviepy stdout
            )
            
        return output_path

if __name__ == "__main__":
    # Quick test
    pass
