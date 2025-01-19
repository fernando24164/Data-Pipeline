import json
import logging
from pathlib import Path
from typing import Any, Dict


class Config:
    def __init__(self, config_file: str = "config.json") -> None:
        """
        Initialize the Config class with path resolution capabilities.

        Args:
            config_file (str): Name of the configuration file
            base_path (str, optional): Base directory path. If None, uses the current directory
        """
        self.base_path = Path(__file__).parent
        self.config_file = self._resolve_config_path(config_file)
        self.config_data = self.load_config()

    def _resolve_config_path(self, config_file: str) -> Path:
        """
        Resolve the absolute path of the configuration file.

        Args:
            config_file (str): The configuration file name or relative path

        Returns:
            Path: Absolute path to the configuration file
        """
        path = Path(config_file)
        return (
            path
            if path.is_absolute()
            else (Path(self.base_path) / config_file).resolve()
        )

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the specified file with proper path handling.

        Returns:
            dict: Configuration data or empty dict if loading fails
        """
        try:
            with self.config_file.open(mode="r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Config file not found: {self.config_file}")
            logging.info(f"Working directory: {Path.cwd()}")
            logging.info(f"Base path: {self.base_path}")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in config file: {self.config_file}")
            return {}
        except Exception as e:
            logging.error(f"Unexpected error loading config: {str(e)}")
            return {}

    def reload_config(self) -> None:
        self.config_data = self.load_config(self.config_file)

    def get_site_info(self) -> Dict[str, Any]:
        return self.config_data
