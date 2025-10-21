"""
Qwen3-VL API Node - Call Qwen3-VL models via DashScope API
Supports images, videos, and text inputs
"""

import os
import json
import base64
import requests
import io
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse
import mimetypes
import numpy as np
import urllib3
from .qwen3vl_config import get_config

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Qwen3VLAPINode:
    """
    Qwen3-VL API Node for ComfyUI
    Calls Qwen3-VL models through DashScope API
    """
    
    def __init__(self):
        self.config = get_config()
        self.api_key = self.config.get_api_key()
        self.base_url = self.config.get_base_url()
        self.model_name = self.config.get_default_model()

    @classmethod
    def INPUT_TYPES(cls):
        config = get_config()
        available_models = config.get_available_models()
        available_providers = config.get_available_providers()

        return {
            "required": {
                "text_prompt": ("STRING", {
                    "default": "Describe this image.",
                    "multiline": True
                }),
                "provider": (available_providers, {
                    "default": config.get_provider()
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "model_name": (available_models, {
                    "default": available_models[0] if available_models else "Qwen3-VL 235B (Instruct)"
                }),
                "max_tokens": ("INT", {
                    "default": config.get_default_max_tokens(),
                    "min": 1,
                    "max": 8192,
                    "step": 1
                }),
                "temperature": ("FLOAT", {
                    "default": config.get_default_temperature(),
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "top_p": ("FLOAT", {
                    "default": config.get_default_top_p(),
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
            },
            "optional": {
                "image": ("IMAGE",),
                "video": ("VIDEO",),
                "stream": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text_output", "raw_response")
    FUNCTION = "process"
    CATEGORY = "Qwen3-VL"
    
    def process(
        self,
        text_prompt: str,
        provider: str,
        api_key: str,
        model_name: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        image: Optional[Any] = None,
        video: Optional[str] = None,
        stream: bool = False,
    ) -> Tuple[str, str]:
        """
        Process request through Qwen3-VL API

        Args:
            text_prompt: Text prompt for the model
            provider: API provider (dashscope or t8)
            api_key: API key for the provider
            model_name: Model name to use
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            top_p: Top-p for generation
            image: Optional image tensor
            video: Optional video path or URL
            stream: Whether to use streaming

        Returns:
            Tuple of (text_output, raw_response)
        """
        # Get provider info
        provider_info = self.config.get_provider_info(provider)
        base_url = provider_info.get('base_url', '')
        provider_name = provider_info.get('name', provider)

        # Clean model name - remove tags like [Comfly-T8]
        import re
        clean_model_name = re.sub(r'\[.*?\]', '', model_name).strip()

        # Use provided model name, or default
        if not clean_model_name or clean_model_name == "":
            clean_model_name = self.config.get_default_model()

        model_name = clean_model_name

        # Use provided API key, or config file, or environment variable
        if not api_key:
            api_key = self.config.get_api_key(provider)

        if not api_key:
            api_key = os.getenv("DASHSCOPE_API_KEY", "")

        if not api_key:
            raise ValueError(f"API key not provided for {provider_name}. Set it in Qwen3-VL-config.json, DASHSCOPE_API_KEY environment variable, or provide api_key parameter.")
        
        # Build message content
        content = []
        
        # Add image if provided
        if image is not None:
            image_url = self._process_image(image)
            content.append({
                "type": "image_url",
                "image_url": {"url": image_url}
            })
        
        # Add video if provided
        if video is not None:
            # Handle VIDEO type from LoadVideo node (dict with 'video_name' key)
            if isinstance(video, dict) and 'video_name' in video:
                video_path = video['video_name']
            # Handle string type (backward compatibility)
            elif isinstance(video, str) and video.strip():
                video_path = video
            else:
                video_path = None

            if video_path:
                video_url = self._process_video(video_path)
                # Only add video if it's a valid URL or Base64 data
                if video_url and (video_url.startswith(('http://', 'https://', 'data:'))):
                    content.append({
                        "type": "video_url",
                        "video_url": {"url": video_url}
                    })
                else:
                    print(f"[Qwen3VL API] ⚠️ Video URL invalid, skipping")
        
        # Add text prompt
        content.append({
            "type": "text",
            "text": text_prompt
        })
        
        # Build request
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]



        # Call API
        response_text, raw_response = self._call_api(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            provider=provider
        )

        return (response_text, raw_response)
    
    def _process_image(self, image_tensor) -> str:
        """Convert image tensor to URL or base64 with size limit"""
        import torch
        from PIL import Image as PILImage

        # Handle different tensor shapes
        if image_tensor.dim() == 4:
            # (B, H, W, C) format
            image_tensor = image_tensor[0]

        # Ensure tensor is in (H, W, C) format
        if image_tensor.dim() == 3:
            # Check if it's (C, H, W) or (H, W, C)
            if image_tensor.shape[0] in [1, 3, 4]:  # Likely (C, H, W)
                image_tensor = image_tensor.permute(1, 2, 0)

        # Convert to numpy and scale to 0-255
        image_np = image_tensor.cpu().numpy()
        if image_np.dtype == np.float32 or image_np.dtype == np.float64:
            image_np = (image_np * 255).astype(np.uint8)

        # Create PIL image
        pil_image = PILImage.fromarray(image_np.astype(np.uint8))

        # Resize if image is too large (max 2048 on longest side)
        max_size = 2048
        width, height = pil_image.size
        if width > max_size or height > max_size:
            # Calculate new size maintaining aspect ratio
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))

            pil_image = pil_image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

        # Convert to PNG and encode to base64
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_b64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return f"data:image/png;base64,{img_b64}"
    
    def _process_video(self, video_input: str) -> str:
        """Process video input - return URL or base64"""
        # If it's a URL, return as-is
        if video_input.startswith(('http://', 'https://')):
            return video_input

        # If it's a local file path, convert to base64
        if os.path.exists(video_input):
            file_size = os.path.getsize(video_input)
            file_size_mb = file_size / 1024 / 1024

            # API has a 20MB limit for base64 strings
            # Base64 encoding increases size by ~33%, so limit original file to ~15MB
            max_size_bytes = 15 * 1024 * 1024
            if file_size > max_size_bytes:
                print(f"[Qwen3VL API] ⚠️ Video file too large: {file_size_mb:.2f}MB")
                print(f"[Qwen3VL API] ⚠️ Maximum supported size: 15MB (API base64 limit)")
                print(f"[Qwen3VL API] ⚠️ Please use a smaller video or upload to a URL")
                return None

            # Encode to Base64
            with open(video_input, 'rb') as f:
                video_data = f.read()
            video_b64 = base64.b64encode(video_data).decode('utf-8')
            print(f"[Qwen3VL API] ✓ Video encoded: {file_size_mb:.2f}MB → {len(video_b64) / 1024 / 1024:.2f}MB base64")
            return f"data:video/mp4;base64,{video_b64}"

        # File doesn't exist
        print(f"[Qwen3VL API] ⚠️ Video file not found: {video_input}")
        return video_input
    
    def _call_api(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        messages: List[Dict[str, Any]],
        max_tokens: int,
        temperature: float,
        top_p: float,
        stream: bool = False,
        provider: str = "dashscope"
    ) -> Tuple[str, str]:
        """Call API through specified provider"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ComfyUI-Qwen3VL/1.0"
        }

        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }

        url = f"{base_url}/chat/completions"

        try:
            if stream:
                return self._call_api_stream(url, headers, payload)
            else:
                return self._call_api_normal(url, headers, payload, provider)

        except requests.exceptions.HTTPError as e:
            error_msg = f"API HTTP Error: {e.response.status_code} - {e.response.text}"
            print(f"[Qwen3VL API] {error_msg}")
            return (error_msg, json.dumps({"error": str(e)}, ensure_ascii=False))
        except requests.exceptions.RequestException as e:
            error_msg = f"API Error: {str(e)}"
            print(f"[Qwen3VL API] {error_msg}")
            return (error_msg, json.dumps({"error": str(e)}, ensure_ascii=False))

    def _call_api_normal(self, url: str, headers: Dict, payload: Dict, provider: str = "dashscope") -> Tuple[str, str]:
        """Normal API call (non-streaming) with retry logic"""
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=600,
                    stream=True
                )

                if response.status_code != 200:
                    error_text = response.text
                    print(f"[Qwen3VL API] Error {response.status_code}: {error_text}")
                    return (f"API Error {response.status_code}: {error_text}",
                            json.dumps({"error": error_text}, ensure_ascii=False))

                # 读取完整响应
                response_text = response.text
                result = json.loads(response_text)

                # Extract text from response
                if "choices" in result and len(result["choices"]) > 0:
                    text_output = result["choices"][0]["message"]["content"]
                else:
                    text_output = "No response from model"

                raw_response = json.dumps(result, ensure_ascii=False, indent=2)

                return (text_output, raw_response)

            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                error_msg = f"Connection error: {str(e)}"
                print(f"[Qwen3VL API] ⚠️ {error_msg}")

                if attempt < max_retries - 1:
                    print(f"[Qwen3VL API] Retrying in {retry_delay}s...")
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return (error_msg, json.dumps({"error": error_msg}, ensure_ascii=False))

            except requests.exceptions.Timeout:
                error_msg = "API request timeout (600 seconds)"
                print(f"[Qwen3VL API] ⚠️ {error_msg}")
                return (error_msg, json.dumps({"error": error_msg}, ensure_ascii=False))
            except Exception as e:
                error_msg = f"Error processing response: {type(e).__name__}: {str(e)}"
                print(f"[Qwen3VL API] ⚠️ {error_msg}")
                import traceback
                traceback.print_exc()
                return (error_msg, json.dumps({"error": str(e)}, ensure_ascii=False))

    def _call_api_stream(self, url: str, headers: Dict, payload: Dict) -> Tuple[str, str]:
        """Streaming API call"""
        text_output = ""
        raw_responses = []

        response = requests.post(url, json=payload, headers=headers, timeout=300, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        raw_responses.append(data)

                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                text_output += delta["content"]
                    except json.JSONDecodeError:
                        pass

        raw_response = json.dumps(raw_responses, ensure_ascii=False, indent=2)
        return (text_output, raw_response)


# Node class mapping
NODE_CLASS_MAPPINGS = {
    "Qwen3VLAPINode": Qwen3VLAPINode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen3VLAPINode": "Qwen3-VL API",
}

