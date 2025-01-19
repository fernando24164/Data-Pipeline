from pathlib import Path

from src.config.config import Config


class TestConfig:
    def test_init_default_config_file(self):
        config = Config()
        expected_base_path = Path.cwd() / "src" / "config"
        expected_config_file = expected_base_path / "config.json"

        assert Path(config.base_path) == expected_base_path
        assert Path(config.config_file) == expected_config_file.resolve()

    def test_load_nonexistent_config_file(self, mocker):
        mock_logger = mocker.patch("logging.error")
        config = Config("nonexistent.json")
        expected_path = Path(config.base_path) / "nonexistent.json"

        assert config.config_data == {}
        mock_logger.assert_called_once_with(
            f"Config file not found: {expected_path.resolve()}"
        )
