from pathlib import Path
import json


def ensure_directory(path: Path):
    """
    Create directory if it does not exist.
    """
    path.mkdir(
        parents=True,
        exist_ok=True
    )


def initialize_storage():
    """
    Creates the entire storage structure.
    """
    from config import (
        STORAGE_DIR,
        PROJECTS_DIR,
        DATASETS_DIR,
        MODELS_DIR,
        EXPERIMENTS_DIR
    )

    directories = [
        STORAGE_DIR,
        PROJECTS_DIR,
        DATASETS_DIR,
        MODELS_DIR,
        EXPERIMENTS_DIR
    ]

    for directory in directories:
        ensure_directory(directory)


def save_json(data, path: Path):
    """
    Save dictionary as JSON.
    """

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


def load_json(path: Path):
    """
    Load JSON file.
    """

    with open(path, "r") as f:
        return json.load(f)