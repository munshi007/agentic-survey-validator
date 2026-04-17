"""Centralized configuration loading for models and rubric."""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load minimal env (OpenAI key)
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DELIVERABLES_DIR = PROJECT_ROOT / "deliverables"

def load_yaml_config(filename: str) -> dict:
    filepath = CONFIG_DIR / filename
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

# Global Config
RUBRIC = load_yaml_config("rubric.yaml")
MODEL_CONFIG = load_yaml_config("model_config.yaml")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")
