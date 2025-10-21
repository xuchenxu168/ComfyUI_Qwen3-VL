"""
Load Video Node for ComfyUI
Allows loading video files similar to LoadImage node
"""

import os
from pathlib import Path
from typing import Tuple, List


class LoadVideo:
    """Load video file and return video path"""
    
    def __init__(self):
        self.video_dir = os.path.join(os.path.dirname(__file__), "videos")
        os.makedirs(self.video_dir, exist_ok=True)
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define input types"""
        video_dir = os.path.join(os.path.dirname(__file__), "videos")
        os.makedirs(video_dir, exist_ok=True)
        
        # Get list of video files
        video_files = []
        if os.path.exists(video_dir):
            for file in os.listdir(video_dir):
                if file.lower().endswith(('.mp4', '.mov', '.webm', '.avi', '.mkv', '.flv', '.wmv')):
                    video_files.append(file)
        
        if not video_files:
            video_files = ["No videos found"]
        
        return {
            "required": {
                "video": (sorted(video_files), {"default": video_files[0] if video_files else ""}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "load_video"
    CATEGORY = "Qwen3-VL"
    
    def load_video(self, video: str) -> Tuple[str]:
        """Load video and return path"""
        video_dir = os.path.join(os.path.dirname(__file__), "videos")
        video_path = os.path.join(video_dir, video)
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print(f"[LoadVideo] Loaded: {video}")
        print(f"[LoadVideo] Path: {video_path}")
        print(f"[LoadVideo] Size: {os.path.getsize(video_path) / 1024 / 1024:.2f}MB")
        
        return (video_path,)


class LoadVideoURL:
    """Load video from URL"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define input types"""
        return {
            "required": {
                "url": ("STRING", {
                    "default": "https://example.com/video.mp4",
                    "multiline": False
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "load_video_url"
    CATEGORY = "Qwen3-VL"
    
    def load_video_url(self, url: str) -> Tuple[str]:
        """Load video from URL"""
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL: {url}")
        
        print(f"[LoadVideoURL] URL: {url}")
        
        return (url,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "LoadVideo": LoadVideo,
    "LoadVideoURL": LoadVideoURL,
}

# Display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadVideo": "Load Video",
    "LoadVideoURL": "Load Video (URL)",
}

