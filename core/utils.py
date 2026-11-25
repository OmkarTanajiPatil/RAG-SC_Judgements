from pathlib import Path
from typing import Any

import yaml


def read_yaml_config(filename: str) -> dict[str, Any]:
	"""Read and return a YAML configuration from the project's config folder."""
	config_path = Path(__file__).resolve().parent.parent / "config" / filename
	with config_path.open("r", encoding="utf-8") as file:
		config = yaml.safe_load(file)

	return config or {}
