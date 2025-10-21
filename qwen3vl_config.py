"""
Configuration Manager for Qwen3-VL
Handles loading and managing configuration from JSON file
"""

import os
import json
from typing import Any, Dict, List, Optional
from pathlib import Path


class Qwen3VLConfig:
    """Configuration manager for Qwen3-VL API"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(Qwen3VLConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration"""
        if self._config is None:
            self.load_config()
    
    @staticmethod
    def get_config_path() -> str:
        """Get path to config file"""
        config_dir = os.path.dirname(__file__)
        config_path = os.path.join(config_dir, "Qwen3-VL-config.json")
        return config_path
    
    def load_config(self) -> None:
        """Load configuration from JSON file"""
        config_path = self.get_config_path()
        
        if not os.path.exists(config_path):
            print(f"[Qwen3VL Config] ⚠️ Config file not found: {config_path}")
            print(f"[Qwen3VL Config] Using default configuration")
            self._config = self._get_default_config()
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            print(f"[Qwen3VL Config] ✓ Config loaded from: {config_path}")
        except json.JSONDecodeError as e:
            print(f"[Qwen3VL Config] ⚠️ Invalid JSON in config file: {e}")
            print(f"[Qwen3VL Config] Using default configuration")
            self._config = self._get_default_config()
        except Exception as e:
            print(f"[Qwen3VL Config] ⚠️ Error loading config: {e}")
            print(f"[Qwen3VL Config] Using default configuration")
            self._config = self._get_default_config()
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        self._config = None
        self.load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def get_provider(self) -> str:
        """Get current API provider"""
        return self.get('api.provider', 'dashscope')

    def get_available_providers(self) -> List[str]:
        """Get list of available API providers"""
        providers = self.get('api.providers', {})
        return list(providers.keys()) if isinstance(providers, dict) else ['dashscope']

    def get_provider_info(self, provider: str = None) -> Dict[str, str]:
        """Get provider configuration"""
        if provider is None:
            provider = self.get_provider()

        providers = self.get('api.providers', {})
        if isinstance(providers, dict) and provider in providers:
            return providers[provider]

        # Fallback to dashscope
        return providers.get('dashscope', {
            'name': '通义万像API',
            'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
            'api_key': ''
        })

    def get_api_key(self, provider: str = None) -> str:
        """Get API key from config or environment"""
        provider_info = self.get_provider_info(provider)
        api_key = provider_info.get('api_key', '')

        # Fall back to environment variable
        if not api_key:
            api_key = os.getenv('DASHSCOPE_API_KEY', '')

        return api_key

    def get_base_url(self, provider: str = None) -> str:
        """Get API base URL"""
        provider_info = self.get_provider_info(provider)
        return provider_info.get('base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    
    def get_default_model(self) -> str:
        """Get default model name"""
        return self.get('models.default', 'qwen3-vl-235b-a22b-instruct')
    
    def get_available_models(self) -> List[str]:
        """Get list of available model display names"""
        models = self.get('models.available', [])
        return [m.get('display_name', m['name']) for m in models if isinstance(m, dict)]

    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model"""
        models = self.get('models.available', [])
        for model in models:
            if isinstance(model, dict) and model.get('name') == model_name:
                return model
        return None
    
    def get_default_temperature(self) -> float:
        """Get default temperature"""
        return self.get('generation.default_temperature', 0.7)
    
    def get_default_top_p(self) -> float:
        """Get default top_p"""
        return self.get('generation.default_top_p', 0.8)
    
    def get_default_top_k(self) -> int:
        """Get default top_k"""
        return self.get('generation.default_top_k', 20)
    
    def get_default_max_tokens(self) -> int:
        """Get default max_tokens"""
        return self.get('generation.default_max_tokens', 1024)
    
    def get_default_repetition_penalty(self) -> float:
        """Get default repetition_penalty"""
        return self.get('generation.default_repetition_penalty', 1.0)
    
    def get_image_max_size_mb(self) -> int:
        """Get maximum image size in MB"""
        return self.get('media.image.max_size_mb', 9)
    
    def get_image_compression_quality(self) -> int:
        """Get initial image compression quality"""
        return self.get('media.image.compression_quality', 95)
    
    def get_image_min_compression_quality(self) -> int:
        """Get minimum image compression quality"""
        return self.get('media.image.min_compression_quality', 10)
    
    def get_video_max_size_mb(self) -> int:
        """Get maximum video size in MB"""
        return self.get('media.video.max_size_mb', 9)
    
    def get_timeout(self) -> int:
        """Get API timeout in seconds"""
        return self.get('api.timeout', 30)
    
    def get_max_retries(self) -> int:
        """Get maximum number of retries"""
        return self.get('api.max_retries', 3)
    
    def get_proxy(self) -> Optional[str]:
        """Get proxy URL if configured"""
        return self.get('api.proxy', None)
    
    def is_streaming_enabled(self) -> bool:
        """Check if streaming is enabled"""
        return self.get('features.enable_streaming', True)
    
    def is_thinking_enabled(self) -> bool:
        """Check if thinking mode is enabled"""
        return self.get('features.enable_thinking', True)
    
    def is_image_compression_enabled(self) -> bool:
        """Check if image compression is enabled"""
        return self.get('features.enable_image_compression', True)
    
    def get_log_level(self) -> str:
        """Get logging level"""
        return self.get('logging.level', 'INFO')
    
    def is_debug_enabled(self) -> bool:
        """Check if debug logging is enabled"""
        return self.get('logging.enable_debug', False)
    
    def should_log_api_calls(self) -> bool:
        """Check if API calls should be logged"""
        return self.get('logging.log_api_calls', True)
    
    def should_log_payloads(self) -> bool:
        """Check if payloads should be logged"""
        return self.get('logging.log_payloads', False)
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "api": {
                "provider": "dashscope",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                "api_key": "",
                "timeout": 30,
                "max_retries": 3,
                "proxy": None
            },
            "models": {
                "default": "qwen3-vl-235b-a22b-instruct",
                "available": [
                    {
                        "name": "qwen3-vl-235b-a22b-instruct",
                        "display_name": "Qwen3-VL 235B (Instruct)",
                        "max_tokens": 8192
                    },
                    {
                        "name": "qwen3-vl-235b-a22b-thinking",
                        "display_name": "Qwen3-VL 235B (Thinking)",
                        "max_tokens": 8192
                    },
                    {
                        "name": "qwen-vl-max",
                        "display_name": "Qwen-VL Max",
                        "max_tokens": 4096
                    },
                    {
                        "name": "qwen-vl-plus",
                        "display_name": "Qwen-VL Plus",
                        "max_tokens": 4096
                    }
                ]
            },
            "generation": {
                "default_temperature": 0.7,
                "default_top_p": 0.8,
                "default_top_k": 20,
                "default_max_tokens": 1024,
                "default_repetition_penalty": 1.0
            },
            "media": {
                "image": {
                    "max_size_mb": 9,
                    "compression_quality": 95,
                    "min_compression_quality": 10
                },
                "video": {
                    "max_size_mb": 9
                }
            },
            "logging": {
                "level": "INFO",
                "enable_debug": False,
                "log_api_calls": True,
                "log_payloads": False
            },
            "features": {
                "enable_streaming": True,
                "enable_thinking": True,
                "enable_image_compression": True,
                "enable_video_compression": False
            }
        }


# Global config instance
_config = None


def get_config() -> Qwen3VLConfig:
    """Get global config instance"""
    global _config
    if _config is None:
        _config = Qwen3VLConfig()
    return _config

