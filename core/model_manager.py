from pathlib import Path
from datetime import datetime
import uuid

import torch

from config import MODELS_DIR
from utils.file_utils import (
    save_json,
    load_json
)


class ModelManager:
    """
    Handles trained model storage.
    """

    def __init__(self):
        self.models_dir = MODELS_DIR

    def save_model(
    self,
    model,
    project_id: str,
    model_name: str,
    classes: list,
    metrics: dict,
    config: dict
    ):
        """
        Saves trained model and metadata.
        """

        # Unique model ID
        model_id = str(uuid.uuid4())[:8]


        # Create model directory
        model_path = (
            self.models_dir /
            model_id
        )

        model_path.mkdir(
            parents=True,
            exist_ok=True
        )


        # Save PyTorch weights
        weights_file = (
            model_path /
            "weights.pth"
        )

        torch.save(
            model.state_dict(),
            weights_file
        )


        # Create metadata
        metadata = {

            "id": model_id,

            "name": model_name,

            "project_id": project_id,

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

            "classes": classes,

            "metrics": metrics,

            "config": config
        }


        # Save metadata
        save_json(
            metadata,
            model_path / "metadata.json"
        )


        return metadata