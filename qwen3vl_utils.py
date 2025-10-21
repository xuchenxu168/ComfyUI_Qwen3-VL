"""
Utility nodes for Qwen3-VL integration
Provides helper nodes for image/video loading and text processing
"""

import os
import torch
import folder_paths
from pathlib import Path
from typing import Optional, Tuple, List
import cv2
import numpy as np
from PIL import Image


class LoadImageForQwen3VL:
    """Load image from file path for Qwen3-VL processing"""
    
    @classmethod
    def INPUT_TYPES(cls):
        image_dir = folder_paths.get_input_directory()
        files = []
        for f in os.listdir(image_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                files.append(f)
        
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "load_image"
    CATEGORY = "Qwen3-VL/loaders"

    def load_image(self, image):
        image_path = os.path.join(folder_paths.get_input_directory(), image)
        img = Image.open(image_path).convert("RGB")
        img_array = np.array(img).astype(np.float32) / 255.0
        return (torch.from_numpy(img_array).unsqueeze(0),)


class LoadVideoForQwen3VL:
    """Load video from file path for Qwen3-VL processing"""
    
    @classmethod
    def INPUT_TYPES(cls):
        video_dir = folder_paths.get_input_directory()
        files = []
        for f in os.listdir(video_dir):
            if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')):
                files.append(f)
        
        return {
            "required": {
                "video": (sorted(files), {"video_upload": True}),
                "fps": ("INT", {"default": 2, "min": 1, "max": 30, "step": 1}),
                "max_frames": ("INT", {"default": 128, "min": 1, "max": 1024, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("VIDEO",)
    RETURN_NAMES = ("video",)
    FUNCTION = "load_video"
    CATEGORY = "Qwen3-VL/loaders"

    def load_video(self, video: str, fps: int, max_frames: int):
        video_path = os.path.join(folder_paths.get_input_directory(), video)
        
        cap = cv2.VideoCapture(video_path)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_skip = max(1, int(video_fps / fps))
        
        frames = []
        frame_count = 0
        
        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_skip == 0:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_tensor = torch.from_numpy(frame_rgb).float() / 255.0
                frames.append(frame_tensor)
            
            frame_count += 1
        
        cap.release()
        
        if frames:
            video_tensor = torch.stack(frames)
            return (video_tensor,)
        else:
            raise ValueError(f"No frames loaded from video: {video_path}")


class CombineImagesForQwen3VL:
    """Combine multiple images into a batch for multi-image queries"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE",),
            },
            "optional": {
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "image_5": ("IMAGE",),
                "resize_mode": (["keep_original", "resize_to_first", "resize_to_max"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("combined_images",)
    FUNCTION = "combine"
    CATEGORY = "Qwen3-VL/utils"

    def combine(self, image_1, image_2=None, image_3=None, image_4=None, image_5=None, resize_mode="keep_original"):
        images = [image_1]

        for img in [image_2, image_3, image_4, image_5]:
            if img is not None:
                images.append(img)

        # If all images have the same size, just concatenate
        if len(images) == 1:
            return (images[0],)

        # Check if all images have the same dimensions
        first_shape = images[0].shape[1:3]  # Get H, W
        all_same_size = all(img.shape[1:3] == first_shape for img in images)

        if all_same_size:
            # All images have the same size, just concatenate
            combined = torch.cat(images, dim=0)
        else:
            # Images have different sizes, need to resize
            if resize_mode == "keep_original":
                # Keep original sizes - this will fail, so we need to resize
                resize_mode = "resize_to_first"

            if resize_mode == "resize_to_first":
                # Resize all images to match the first image
                target_h, target_w = images[0].shape[1:3]

                resized_images = [images[0]]
                for i, img in enumerate(images[1:], 1):
                    if img.shape[1:3] != (target_h, target_w):
                        # Use torch.nn.functional.interpolate for resizing
                        import torch.nn.functional as F
                        # Reshape to (B, C, H, W) for interpolation
                        img_reshaped = img.permute(0, 3, 1, 2)  # (B, H, W, C) -> (B, C, H, W)
                        img_resized = F.interpolate(img_reshaped, size=(target_h, target_w), mode='bilinear', align_corners=False)
                        img_resized = img_resized.permute(0, 2, 3, 1)  # (B, C, H, W) -> (B, H, W, C)
                        resized_images.append(img_resized)
                    else:
                        resized_images.append(img)

                combined = torch.cat(resized_images, dim=0)

            elif resize_mode == "resize_to_max":
                # Resize all images to the maximum dimensions
                max_h = max(img.shape[1] for img in images)
                max_w = max(img.shape[2] for img in images)

                resized_images = []
                for i, img in enumerate(images):
                    if img.shape[1:3] != (max_h, max_w):
                        # Use torch.nn.functional.interpolate for resizing
                        import torch.nn.functional as F
                        # Reshape to (B, C, H, W) for interpolation
                        img_reshaped = img.permute(0, 3, 1, 2)  # (B, H, W, C) -> (B, C, H, W)
                        img_resized = F.interpolate(img_reshaped, size=(max_h, max_w), mode='bilinear', align_corners=False)
                        img_resized = img_resized.permute(0, 2, 3, 1)  # (B, C, H, W) -> (B, H, W, C)
                        resized_images.append(img_resized)
                    else:
                        resized_images.append(img)

                combined = torch.cat(resized_images, dim=0)

        return (combined,)


class TextPromptForQwen3VL:
    """Create and manage text prompts for Qwen3-VL"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "default": "Describe this image in detail.",
                    "multiline": True
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "default": "You are a helpful assistant expert in analyzing images and videos.",
                    "multiline": True
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("user_prompt", "system_prompt")
    FUNCTION = "create_prompt"
    CATEGORY = "Qwen3-VL/utils"

    def create_prompt(self, prompt, system_prompt=""):
        if not system_prompt:
            system_prompt = "You are a helpful assistant expert in analyzing images and videos."
        return (prompt, system_prompt)


class Qwen3VLResponseFormatter:
    """Format Qwen3-VL response for ComfyUI Display nodes"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "response": ("STRING",),
            },
            "optional": {
                "title": ("STRING", {"default": "Qwen3-VL Response"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_response",)
    FUNCTION = "format_response"
    CATEGORY = "Qwen3-VL/utils"

    def format_response(self, response, title="Qwen3-VL Response"):
        """Format response with title for better display"""
        formatted = f"{title}\n{'='*80}\n{response}"
        return (formatted,)


NODE_CLASS_MAPPINGS = {
    "LoadImageForQwen3VL": LoadImageForQwen3VL,
    "LoadVideoForQwen3VL": LoadVideoForQwen3VL,
    "CombineImagesForQwen3VL": CombineImagesForQwen3VL,
    "TextPromptForQwen3VL": TextPromptForQwen3VL,
    "Qwen3VLResponseFormatter": Qwen3VLResponseFormatter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageForQwen3VL": "Load Image for Qwen3-VL",
    "LoadVideoForQwen3VL": "Load Video for Qwen3-VL",
    "CombineImagesForQwen3VL": "Combine Images for Qwen3-VL",
    "TextPromptForQwen3VL": "Text Prompt for Qwen3-VL",
    "Qwen3VLResponseFormatter": "Qwen3-VL Response Formatter",
}

