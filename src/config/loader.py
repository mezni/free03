from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file."""
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise ValueError(f"Configuration root must be a mapping: {config_path}")

    return data
