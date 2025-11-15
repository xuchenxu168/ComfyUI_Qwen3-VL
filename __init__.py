"""
ComfyUI Qwen3-VL Integration
Enhanced local implementation of Qwen3-VL for ComfyUI
Supports direct image and video inputs without intermediate conversion
"""

__version__ = "2.0.0"

import os
from .qwen3vl_processor import NODE_CLASS_MAPPINGS as PROCESSOR_MAPPINGS
from .qwen3vl_processor import NODE_DISPLAY_NAME_MAPPINGS as PROCESSOR_DISPLAY_NAMES
from .qwen3vl_utils import NODE_CLASS_MAPPINGS as UTILS_MAPPINGS
from .qwen3vl_utils import NODE_DISPLAY_NAME_MAPPINGS as UTILS_DISPLAY_NAMES
from .qwen3vl_api_node import NODE_CLASS_MAPPINGS as API_MAPPINGS
from .qwen3vl_api_node import NODE_DISPLAY_NAME_MAPPINGS as API_DISPLAY_NAMES
from .qwen3vl_api_advanced import NODE_CLASS_MAPPINGS as API_ADVANCED_MAPPINGS
from .qwen3vl_api_advanced import NODE_DISPLAY_NAME_MAPPINGS as API_ADVANCED_DISPLAY_NAMES

# Combine all node mappings
NODE_CLASS_MAPPINGS = {
    **PROCESSOR_MAPPINGS,
    **UTILS_MAPPINGS,
    **API_MAPPINGS,
    **API_ADVANCED_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **PROCESSOR_DISPLAY_NAMES,
    **UTILS_DISPLAY_NAMES,
    **API_DISPLAY_NAMES,
    **API_ADVANCED_DISPLAY_NAMES,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "__version__"]

