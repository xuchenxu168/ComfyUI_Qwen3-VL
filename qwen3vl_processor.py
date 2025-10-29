"""
Qwen3-VL Processor Node - Main inference node for Qwen3-VL models
Supports direct image and video inputs without intermediate conversion
"""

import os
import torch
import folder_paths
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import base64
import io
from transformers import (
    Qwen3VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
)
import comfy.model_management
from qwen_vl_utils import process_vision_info


class Qwen3VLProcessor:
    """
    Enhanced Qwen3-VL processor node with improved architecture
    Supports text, images, and videos directly
    """

    # Model ID mapping: model_name -> HuggingFace repo_id
    MODEL_REPO_MAP = {
        "Qwen3-VL-4B-Instruct": "Qwen/Qwen3-VL-4B-Instruct",
        "Qwen3-VL-4B-Thinking": "Qwen/Qwen3-VL-4B-Thinking",
        "Qwen3-VL-8B-Instruct": "Qwen/Qwen3-VL-8B-Instruct",
        "Qwen3-VL-8B-Thinking": "Qwen/Qwen3-VL-8B-Thinking",
        "Qwen3-VL-4B-Instruct-FP8": "Qwen/Qwen3-VL-4B-Instruct-FP8",
        "Qwen3-VL-4B-Thinking-FP8": "Qwen/Qwen3-VL-4B-Thinking-FP8",
        "Qwen3-VL-8B-Instruct-FP8": "Qwen/Qwen3-VL-8B-Instruct-FP8",
        "Qwen3-VL-8B-Thinking-FP8": "Qwen/Qwen3-VL-8B-Thinking-FP8",
        "Huihui-Qwen3-VL-8B-Instruct-abliterated": "huihui-ai/Huihui-Qwen3-VL-8B-Instruct-abliterated",
    }

    def __init__(self):
        self.model_checkpoint = None
        self.processor = None
        self.model = None
        self.device = comfy.model_management.get_torch_device()
        self.bf16_support = (
            torch.cuda.is_available()
            and torch.cuda.get_device_capability(self.device)[0] >= 8
        )
        self.current_model_name = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_prompt": ("STRING", {
                    "default": "Describe this image.",
                    "multiline": True
                }),
                "model_name": (
                    [
                        "Qwen3-VL-4B-Instruct",
                        "Qwen3-VL-4B-Thinking",
                        "Qwen3-VL-8B-Instruct",
                        "Qwen3-VL-8B-Thinking",
                        "Qwen3-VL-4B-Instruct-FP8",
                        "Qwen3-VL-4B-Thinking-FP8",
                        "Qwen3-VL-8B-Instruct-FP8",
                        "Qwen3-VL-8B-Thinking-FP8",
                        "Huihui-Qwen3-VL-8B-Instruct-abliterated",
                    ],
                    {"default": "Qwen3-VL-4B-Instruct"}
                ),
                "temperature": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}
                ),
                "top_p": (
                    "FLOAT",
                    {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.05}
                ),
                "max_new_tokens": (
                    "INT",
                    {"default": 2048, "min": 128, "max": 256000, "step": 128}
                ),
                "min_pixels": (
                    "INT",
                    {
                        "default": 256 * 32 * 32,
                        "min": 4 * 32 * 32,
                        "max": 16384 * 32 * 32,
                        "step": 32 * 32,
                    }
                ),
                "max_pixels": (
                    "INT",
                    {
                        "default": 768 * 32 * 32,  # Reduced from 1280 to avoid OOM
                        "min": 4 * 32 * 32,
                        "max": 16384 * 32 * 32,
                        "step": 32 * 32,
                    }
                ),
                "quantization": (
                    ["none", "4bit", "8bit"],
                    {"default": "none"}
                ),
                "attention_type": (
                    ["eager", "sdpa", "flash_attention_2"],
                    {"default": "eager"}
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 0xffffffffffffffff}
                ),
                "max_image_dimension": (
                    "INT",
                    {"default": 2048, "min": 512, "max": 8192, "step": 256}
                ),
            },
            "optional": {
                "image": ("IMAGE",),
                "video": ("VIDEO",),
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "process"
    CATEGORY = "Qwen3-VL"
    OUTPUT_NODE = True

    def _download_model_with_progress(self, model_id: str, local_dir: str):
        """Download model with progress display"""
        from huggingface_hub import snapshot_download
        from tqdm.auto import tqdm

        print(f"\n{'='*70}")
        print(f"[Qwen3-VL] 📥 开始下载模型: {model_id}")
        print(f"[Qwen3-VL] 📂 保存路径: {local_dir}")
        print(f"[Qwen3-VL] ⏳ 请耐心等待，下载可能需要几分钟到几十分钟...")
        print(f"[Qwen3-VL] 💡 下载进度将在下方显示")
        print(f"{'='*70}\n")

        try:
            # snapshot_download 会自动显示每个文件的下载进度条
            snapshot_download(
                repo_id=model_id,
                local_dir=local_dir,
                local_dir_use_symlinks=False,
                resume_download=True,
                tqdm_class=tqdm,  # 使用 tqdm 显示进度
            )
            print(f"\n{'='*70}")
            print(f"[Qwen3-VL] ✅ 模型下载完成: {model_id}")
            print(f"{'='*70}\n")
        except Exception as e:
            print(f"\n{'='*70}")
            print(f"[Qwen3-VL] ❌ 模型下载失败: {e}")
            print(f"[Qwen3-VL] 💡 解决方法:")
            print(f"[Qwen3-VL]    1. 检查网络连接")
            print(f"[Qwen3-VL]    2. 使用镜像站: export HF_ENDPOINT=https://hf-mirror.com")
            print(f"[Qwen3-VL]    3. 使用代理: export HTTP_PROXY=http://127.0.0.1:7890")
            print(f"[Qwen3-VL]    4. 手动下载模型到: {local_dir}")
            print(f"{'='*70}\n")
            raise

    def _load_model(self, model_name: str, quantization: str, attention_type: str):
        """Load model and processor with specified configuration"""
        if self.current_model_name == model_name and self.model is not None:
            return

        # Get HuggingFace repo ID from mapping, fallback to Qwen/{model_name}
        model_id = self.MODEL_REPO_MAP.get(model_name, f"Qwen/{model_name}")

        # Use model_name as local directory name
        self.model_checkpoint = os.path.join(
            folder_paths.models_dir, "qwen3vl", model_name
        )

        # Download model if not exists
        if not os.path.exists(self.model_checkpoint):
            self._download_model_with_progress(model_id, self.model_checkpoint)

        # Load processor
        self.processor = AutoProcessor.from_pretrained(self.model_checkpoint)

        # Configure quantization
        quantization_config = None
        if quantization == "4bit":
            quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        elif quantization == "8bit":
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        # Load model
        self.model = Qwen3VLForConditionalGeneration.from_pretrained(
            self.model_checkpoint,
            dtype=torch.bfloat16 if self.bf16_support else torch.float16,
            device_map="auto",
            attn_implementation=attention_type,
            quantization_config=quantization_config,
        )
        
        self.current_model_name = model_name

    def _prepare_messages(self, text_prompt: str, image_data: Optional[List[str]] = None,
                         video_data: Optional[str] = None) -> List[Dict[str, Any]]:
        """Prepare messages for the model

        Args:
            text_prompt: The text prompt
            image_data: List of base64-encoded image strings (data:image/png;base64,...)
            video_data: Local file path to video (qwen_vl_utils requires file paths for video processing)
        """
        content = []

        if image_data:
            for img_b64 in image_data:
                # Use base64-encoded images directly
                content.append({"type": "image", "image": img_b64})

        if video_data:
            # Use local file path for video (qwen_vl_utils requires file paths)
            content.append({"type": "video", "video": video_data})

        content.append({"type": "text", "text": text_prompt})

        return [{"role": "user", "content": content}]

    def process(
        self,
        text_prompt: str,
        model_name: str,
        temperature: float,
        top_p: float,
        max_new_tokens: int,
        min_pixels: int,
        max_pixels: int,
        quantization: str,
        attention_type: str,
        seed: int,
        max_image_dimension: int,
        image: Optional[torch.Tensor] = None,
        video: Optional[torch.Tensor] = None,
        keep_model_loaded: bool = False,
    ) -> Tuple[str]:
        """Process input and generate response"""

        if seed != -1:
            torch.manual_seed(seed)

        # Load model
        self._load_model(model_name, quantization, attention_type)

        # Prepare image/video data (base64 encoded)
        image_data = None
        video_data = None

        if image is not None:
            from torchvision.transforms import ToPILImage
            import torch.nn.functional as F
            image_data = []
            if image.dim() == 3:
                image = image.unsqueeze(0)

            for idx, img in enumerate(image):
                # Limit image size to avoid OOM
                # Qwen3-VL can handle up to max_pixels, but we'll be conservative
                h, w = img.shape[0], img.shape[1]

                if h > max_image_dimension or w > max_image_dimension:
                    # Calculate scaling factor
                    scale = min(max_image_dimension / h, max_image_dimension / w)
                    new_h, new_w = int(h * scale), int(w * scale)

                    # Resize using interpolation
                    img_reshaped = img.permute(2, 0, 1).unsqueeze(0)  # (H, W, C) -> (1, C, H, W)
                    img_resized = F.interpolate(img_reshaped, size=(new_h, new_w), mode='bilinear', align_corners=False)
                    img = img_resized.squeeze(0).permute(1, 2, 0)  # (1, C, H, W) -> (H, W, C)

                # Convert tensor to PIL image
                # ComfyUI IMAGE format is (B, H, W, C) with values in [0, 1]
                pil_image = ToPILImage()(img.permute(2, 0, 1))

                # Convert PIL image to base64
                img_buffer = io.BytesIO()
                pil_image.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                img_b64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                image_data.append(f"data:image/png;base64,{img_b64}")
        
        if video is not None:
            import cv2
            import numpy as np

            video_data = None
            video_path = None

            # Handle different video input types
            # Check if it's a VideoFromFile object from comfy_api
            if type(video).__name__ == 'VideoFromFile':
                # It's a VideoFromFile object, use get_stream_source() method
                try:
                    # VideoFromFile has a get_stream_source() method that returns the file path or BytesIO
                    stream_source = video.get_stream_source()
                    if isinstance(stream_source, str):
                        # It's a file path, use it directly
                        video_path = stream_source
                    else:
                        # It's a BytesIO object, save to temporary file
                        temp_dir = Path(folder_paths.temp_directory)
                        temp_dir.mkdir(parents=True, exist_ok=True)
                        temp_video_path = temp_dir / f"qwen3vl_video_{seed}.mp4"
                        with open(temp_video_path, 'wb') as f:
                            f.write(stream_source.getvalue())
                        video_path = str(temp_video_path)
                except Exception as e:
                    video_data = None
            elif hasattr(video, 'dim'):
                # It's a tensor, convert to video file
                if video.dim() == 4:  # (T, H, W, C)
                    frames = (video * 255).byte().cpu().numpy()
                    h, w = frames.shape[1], frames.shape[2]

                    # Use temporary file for video encoding (cv2.VideoWriter requires file path)
                    temp_dir = Path(folder_paths.temp_directory)
                    temp_dir.mkdir(parents=True, exist_ok=True)
                    temp_video_path = temp_dir / f"qwen3vl_video_{seed}.mp4"

                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(str(temp_video_path), fourcc, 2.0, (w, h))

                    for frame in frames:
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        out.write(frame_bgr)
                    out.release()

                    video_path = str(temp_video_path)
            else:
                # Try to use as file path
                try:
                    video_path = str(video)
                except Exception as e:
                    video_data = None

            # Use local file path for video (qwen_vl_utils requires file paths for video processing)
            if video_path:
                video_data = video_path
        
        # Prepare messages
        messages = self._prepare_messages(text_prompt, image_data, video_data)

        with torch.no_grad():
            # Apply chat template
            text = self.processor.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            # Process vision info
            image_inputs, video_inputs, video_kwargs = process_vision_info(
                messages,
                return_video_kwargs=True
            )

            # Fix video_kwargs if fps is a sequence
            if video_kwargs and 'fps' in video_kwargs:
                fps_value = video_kwargs['fps']
                # If fps is a sequence, take the first element
                if isinstance(fps_value, (list, tuple)):
                    video_kwargs['fps'] = fps_value[0] if fps_value else 24

            # Prepare inputs
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
                **video_kwargs
            )
            inputs = inputs.to(self.device)

            # Generate
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            
            generated_ids_trimmed = [
                out_ids[len(in_ids):]
                for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            
            result = self.processor.batch_decode(
                generated_ids_trimmed,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )

        # Cleanup
        if not keep_model_loaded:
            del self.processor
            del self.model
            self.processor = None
            self.model = None
            self.current_model_name = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

        return (result[0] if result else "",)


NODE_CLASS_MAPPINGS = {
    "Qwen3VLProcessor": Qwen3VLProcessor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen3VLProcessor": "Qwen3-VL Processor",
}

