"""Configuration management module for LanguageMentor."""

import json
import os
from typing import Any, Dict, Optional
from pathlib import Path

from utils.logger import LOG


class ConfigManager:
    """
    Configuration manager for loading and accessing application settings.

    This class handles loading configuration from a JSON file and provides
    convenient access to configuration values with validation.
    Environment variables take precedence over config file values.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ConfigManager.

        Args:
            config_path: Path to the configuration file. If not provided,
                        defaults to 'config.json' in the project root.
        """
        if config_path is None:
            # Default to config.json in project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config.json"

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from the JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
            LOG.info(f"Configuration loaded from: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_model_provider(self) -> str:
        """
        Get the configured model provider name.

        Returns:
            Model provider name (e.g., "ollama", "siliconflow")
        """
        provider = self.get("model_provider", "ollama")
        if not provider:
            raise ValueError("model_provider is not configured")
        return provider

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """
        Get configuration for a specific provider.

        Args:
            provider: Provider name (e.g., "ollama", "siliconflow")

        Returns:
            Provider configuration dictionary
        """
        config = self.get(provider)
        if config is None:
            raise ValueError(f"Configuration for provider '{provider}' not found")
        return config

    def get_ollama_config(self) -> Dict[str, Any]:
        """
        Get Ollama configuration.

        Returns:
            Ollama configuration dictionary with keys: model, max_tokens, temperature
        """
        config = self.get_provider_config("ollama")
        required_keys = ["model"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Required key '{key}' not found in ollama config")
        return config

    def get_siliconflow_config(self) -> Dict[str, Any]:
        """
        Get SiliconFlow configuration.

        API key is first read from OPENAI_API_KEY environment variable.
        If not found, falls back to config file value.

        Returns:
            SiliconFlow configuration dictionary with keys: api_key, model, max_tokens, temperature
        """
        config = self.get_provider_config("siliconflow")
        required_keys = ["model"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Required key '{key}' not found in siliconflow config")

        # Try to get API key from environment variable first, then fall back to config
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            LOG.info("Using API key from OPENAI_API_KEY environment variable")
            config["api_key"] = api_key
        elif "api_key" not in config:
            raise ValueError("SiliconFlow api_key not found in environment (OPENAI_API_KEY) or config file")

        return config

    @property
    def config(self) -> Dict[str, Any]:
        """Get the full configuration dictionary."""
        return self._config.copy()
