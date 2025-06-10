# Purpose:
# Load and validate global configuration from a YAML file (e.g., main_config.yaml).

# Requirements:
#   pip install pyyaml
#
# Usage:
#   from configs.config_loader import load_config
#   config = load_config("configs/main_config.yaml")

import yaml
from pathlib import Path

def load_config(path):
    # Loads a YAML configuration file and returns its contents as a dictionary.
    #
    # Args:
    #   path (str or Path): Path to the YAML config file.
    #
    # Returns:
    #   dict: Parsed configuration data.
    #
    # Raises:
    #   FileNotFoundError: If the config file does not exist.
    #   ValueError: If the YAML is invalid or can't be parsed.

    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")
