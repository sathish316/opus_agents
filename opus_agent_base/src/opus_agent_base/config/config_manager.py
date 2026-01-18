from pathlib import Path
import yaml
from typing import Dict, Any, List, Type, TypeVar
import logging

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
from opus_agent_base.config.nested_config_manager import NestedConfigManager
from opus_agent_base.common.logging_config import console_log


logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration for the Opus TODO Agent."""

    # Configuration file path
    CONFIG_DIR = Path.home() / ".opusai"
    CONFIG_FILE = CONFIG_DIR / "opus-config.yml"

    def __init__(self, config_dir: str = None, config_file: str = None):
        if config_dir is None or config_file is None:
            self.config_dir = ConfigManager.CONFIG_DIR
            self.config_file = ConfigManager.CONFIG_FILE
        else:
            self.config_dir = Path(config_dir)
            self.config_file = self.config_dir / config_file
        self.nested_config_manager = NestedConfigManager()
        self.cached_config = None
        self._ensure_config_dir()
        self._ensure_config_file()

    def _ensure_config_dir(self):
        """Ensure config directory exists."""
        self.config_dir.mkdir(exist_ok=True)

    def _ensure_config_file(self):
        """Ensure config file exists."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        # cache config file
        if self.cached_config is not None:
            return self.cached_config

        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f)
                return config if config is not None else {}
        except (yaml.YAMLError, IOError) as e:
            logger.warning(f"Failed to load config: {e}")
            return {}

    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
            self.cached_config = None
            return True
        except IOError as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting.

        Supports dot notation for nested values (e.g., 'todoist.api_key').
        """
        config = self.load_config()
        keys = key.split(".")
        return self.nested_config_manager.get_nested_value(config, keys, default)

    def set_setting(self, key: str, value: Any) -> bool:
        """Set a configuration setting.

        Supports dot notation for nested values (e.g., 'todoist.api_key').
        Creates intermediate dictionaries as needed.
        """
        config = self.load_config()
        keys = key.split(".")
        self.nested_config_manager.set_nested_value(config, keys, value)
        return self.save_config(config)

    def delete_setting(self, key: str) -> bool:
        """Delete a configuration setting.

        Supports dot notation for nested values (e.g., 'todoist.api_key').
        """
        config = self.load_config()
        keys = key.split(".")
        if self.nested_config_manager.delete_nested_key(config, keys):
            return self.save_config(config)
        return False

    def get_all_settings_flat(self) -> Dict[str, Any]:
        """Get all configuration settings as a flattened dictionary with dot notation keys."""
        config = self.load_config()
        return self.nested_config_manager.get_flattened_values(config)

    def get_setting_as_model(self, key: str, model_class: Type[T], default: T = None) -> T:
        """Get a configuration setting as a Pydantic BaseModel.

        Args:
            key: Dot-notation path to the config section (e.g., 'mcp_config.redis')
            model_class: The Pydantic BaseModel class to instantiate
            default: Default value if key not found (if None, returns model with defaults)

        Returns:
            Instance of model_class populated with config values
        """
        config_dict = self.get_setting(key, None)

        if config_dict is None:
            if default is not None:
                return default
            return model_class()

        if not isinstance(config_dict, dict):
            if default is not None:
                return default
            return model_class()

        return model_class(**config_dict)
