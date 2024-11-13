import tomllib
from typing import List
from appdirs import user_config_dir
from pathlib import Path
import yaml
from dataclasses import dataclass


@dataclass(frozen=True)
class Models:
    model_name: str
    max_tokens: int


DEFAULT_CONFIG = {
    'interface': 'huggingface',
    # 'max_tokens': 32760,
    'temperature': 1,
}

GROQ_MODELS: List[Models] = [
    Models(
        model_name="llama-3.2-90b-text-preview",
        max_tokens=8000
    )
    # Models(
    #     model_name="llama-3.1-8b-instruct",
    #     max_tokens=8000
    # )
]


HUGGING_FACE_MODELS: List[Models] = [
    Models(
        model_name="Qwen/Qwen2.5-72B-Instruct",
        max_tokens=32760
    ),
    # HuggingFaceModel(model_name='Qwen/Qwen2.5-1.5B-Instruct', max_tokens=32760),
    # HuggingFaceModel(model_name='microsoft/Phi-3.5-mini-instruct', max_tokens=32760),
    # HuggingFaceModel(model_name='meta-llama/Meta-Llama-3-8B-Instruct', max_tokens=32760),
]


class ConfigManager:
    def __init__(
        self,
        app_name: str,
        app_author: str = None,
        config_filename: str = "config.yaml"
    ):
        self.config_dir = Path(user_config_dir(app_name, app_author))
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # eg: /home/username/.config/gai/config.yaml
        self.config_path = self.config_dir / config_filename
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            self.create_default_config()

        with self.config_path.open('r') as f:
            return yaml.safe_load(f)

    def create_default_config(self):
        default_config = DEFAULT_CONFIG.copy()

        with self.config_path.open('w') as f:
            yaml.dump(default_config, f)
        print(f"Created default config at {self.config_path}")

    def save_config(self):
        with self.config_path.open('w') as f:
            yaml.dump(self.config, f)
        print(f"Saved config to {self.config_path}")

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def get_config(self, key, default=None):
        return self.config.get(key, default)


def get_app_name():
    try:
        with open('pyproject.toml', 'rb') as f:
            pyproject = tomllib.load(f)
        return pyproject['project']['name']
    except (FileNotFoundError, KeyError):
        return "gai-tool"


if __name__ == "__main__":
    config_manager = ConfigManager(get_app_name())
    interface = config_manager.get_config('interface')
    print(f"Config interface: {interface}")