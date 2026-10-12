"""
Data Loaders Module
DS 3500 - MP1
Functions for loading CSV, JSON, and YAML files.
"""
import json
import logging
from pathlib import Path

import pandas as pd
import yaml

logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a pandas DataFrame."""
    df = pd.read_csv(filepath)
    logger.info("Loaded CSV file: %s (%d rows)", filepath, len(df))
    return df


def load_json(filepath):
    """Load a JSON file into a Python object."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info("Loaded JSON file: %s", filepath)
    return data


def load_yaml(filepath):
    """Load a YAML file into a Python object."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    logger.info("Loaded YAML file: %s", filepath)
    return data


def load_data(filepath):
    """Pick the right loader based on the file extension."""
    path = Path(filepath)
    ext = path.suffix.lower()

    if ext == ".csv":
        return load_csv(path)
    if ext == ".json":
        return load_json(path)
    if ext == ".yaml":
        return load_yaml(path)

    logger.error("Unsupported file format: %s", ext)
    raise ValueError(f"Unsupported file format: {ext}")
