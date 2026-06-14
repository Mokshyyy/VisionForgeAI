from dataclasses import dataclass
from pathlib import Path
from core.model_manager import ModelManager

import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms, models

from config import DATASETS_DIR

@dataclass
class TrainingConfig:
    """
    Stores all training configuration.
    """

    # Basic Settings
    epochs: int = 10
    batch_size: int = 32
    learning_rate: float = 0.001
    image_size: int = 224

    # Dataset split
    train_split: float = 0.8

    # Data augmentation
    augmentation: bool = True


    # Model
    architecture: str = "resnet18"


    # Advanced
    optimizer: str = "adam"
    weight_decay: float = 0.0001

    freeze_backbone: bool = True


class Trainer:
    """
    Handles model training pipeline.
    """

    def __init__(
        self,
        config: TrainingConfig
    ):

        self.config = config

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )


        self.dataset = None
        self.classes = None

        self.train_loader = None
        self.val_loader = None

        self.model = None

        self.loss_function = None
        self.optimizer = None


        self.history = {
            "train_loss": [],
            "train_accuracy": [],
            "val_loss": [],
            "val_accuracy": []
        }

        self.model_manager = ModelManager()


    def train(
    self,
    project_id: str
    ):
        """
        Complete training pipeline.
        """

        self.load_dataset(
            project_id
        )

        self.create_dataloaders()

        self.initialize_model()

        self.setup_training()

        self.training_loop()


        model_info = (
            self.save_training_result(
                project_id
            )
        )


        return {
            "history": self.history,
            "model": model_info
        }


    def get_transforms(self):
        """
        Creates image preprocessing pipeline.
        """

        transform_list = [
            transforms.Resize(
                (
                    self.config.image_size,
                    self.config.image_size
                )
            )
        ]

        if self.config.augmentation:

            transform_list.extend([
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(15)
            ])

        transform_list.extend([
            transforms.ToTensor(),

            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        return transforms.Compose(
            transform_list
        )
    def load_dataset(self, project_id: str):
        """
        Loads dataset from project directory.
        """

        dataset_path = (
            DATASETS_DIR /
            project_id
        )


        if not dataset_path.exists():
            raise FileNotFoundError(
                "Dataset not found."
            )


        self.dataset = datasets.ImageFolder(
            dataset_path,
            transform=self.get_transforms()
        )


        self.classes = (
            self.dataset.classes
        )


        if len(self.classes) < 2:
            raise ValueError(
                "Need at least 2 classes for training."
            )


        if len(self.dataset) < 10:
            raise ValueError(
                "Dataset too small. Add more images."
            )


        return {
            "classes": self.classes,
            "images": len(self.dataset)
        }
    
    def create_dataloaders(self):
        """
        Splits dataset and creates PyTorch dataloaders.
        """

        dataset_size = len(self.dataset)


        train_size = int(
            dataset_size * self.config.train_split
        )


        val_size = (
            dataset_size - train_size
        )


        train_dataset, val_dataset = (
            random_split(
                self.dataset,
                [
                    train_size,
                    val_size
                ]
            )
        )


        self.train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.batch_size,
            shuffle=True
        )


        self.val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.batch_size,
            shuffle=False
        )


        return {
            "train_images": train_size,
            "validation_images": val_size
        }
    
    def initialize_model(self):
        """
        Loads ResNet18 and modifies the final layer.
        """

        # Load pretrained ResNet18
        self.model = models.resnet18(
            weights=models.ResNet18_Weights.DEFAULT
        )


        # Freeze feature extractor
        if self.config.freeze_backbone:

            for param in self.model.parameters():
                param.requires_grad = False


        # Get number of input features to classifier
        in_features = (
            self.model.fc.in_features
        )


        # Replace classification head
        self.model.fc = torch.nn.Linear(
            in_features,
            len(self.classes)
        )


        # Move model to CPU/GPU
        self.model.to(
            self.device
        )


        return {
            "architecture": self.config.architecture,
            "classes": len(self.classes),
            "device": self.device
        }

    def setup_training(self):
        """
        Creates loss function and optimizer.
        """

        # Classification loss
        self.loss_function = (
            torch.nn.CrossEntropyLoss()
        )


        # Get trainable parameters only
        trainable_parameters = filter(
            lambda p: p.requires_grad,
            self.model.parameters()
        )


        # Optimizer selection
        if self.config.optimizer.lower() == "adam":

            self.optimizer = torch.optim.Adam(
                trainable_parameters,
                lr=self.config.learning_rate,
                weight_decay=self.config.weight_decay
            )

        else:
            raise ValueError(
                "Unsupported optimizer."
            )


        return {
            "optimizer": self.config.optimizer,
            "learning_rate": self.config.learning_rate,
            "weight_decay": self.config.weight_decay
        }

    
    def train_epoch(self):
        """
        Trains model for one epoch.
        """

        # Put model in training mode
        self.model.train()

        running_loss = 0
        correct_predictions = 0
        total_samples = 0


        for images, labels in self.train_loader:

            # Move data to GPU/CPU
            images = images.to(self.device)
            labels = labels.to(self.device)


            # Clear old gradients
            self.optimizer.zero_grad()


            # Forward pass
            outputs = self.model(images)


            # Calculate error
            loss = self.loss_function(
                outputs,
                labels
            )


            # Backpropagation
            loss.backward()


            # Update weights
            self.optimizer.step()


            # Statistics
            running_loss += loss.item()


            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct_predictions += (
                predictions == labels
            ).sum().item()

            total_samples += labels.size(0)


        epoch_loss = (
            running_loss /
            len(self.train_loader)
        )


        epoch_accuracy = (
            correct_predictions /
            total_samples
        ) * 100


        return {
            "loss": epoch_loss,
            "accuracy": epoch_accuracy
        }
    

    def validate_epoch(self):
        """
        Evaluates model on validation dataset.
        """

        # Set model to evaluation mode
        self.model.eval()

        running_loss = 0
        correct_predictions = 0
        total_samples = 0


        # Disable gradient calculations
        with torch.no_grad():

            for images, labels in self.val_loader:

                # Move to CPU/GPU
                images = images.to(self.device)
                labels = labels.to(self.device)


                # Forward pass only
                outputs = self.model(images)


                # Calculate loss
                loss = self.loss_function(
                    outputs,
                    labels
                )


                running_loss += loss.item()


                predictions = torch.argmax(
                    outputs,
                    dim=1
                )


                correct_predictions += (
                    predictions == labels
                ).sum().item()


                total_samples += labels.size(0)


        epoch_loss = (
            running_loss /
            len(self.val_loader)
        )


        epoch_accuracy = (
            correct_predictions /
            total_samples
        ) * 100


        return {
            "loss": epoch_loss,
            "accuracy": epoch_accuracy
        }
    

    def training_loop(self):
        """
        Runs complete training process.
        """

        for epoch in range(self.config.epochs):

            # Train for one epoch
            train_metrics = (
                self.train_epoch()
            )


            # Validate model
            val_metrics = (
                self.validate_epoch()
            )


            # Store history
            self.history["train_loss"].append(
                train_metrics["loss"]
            )

            self.history["train_accuracy"].append(
                train_metrics["accuracy"]
            )

            self.history["val_loss"].append(
                val_metrics["loss"]
            )

            self.history["val_accuracy"].append(
                val_metrics["accuracy"]
            )


            # Display progress
            print(
                f"""
    Epoch {epoch + 1}/{self.config.epochs}

    Train Loss: {train_metrics['loss']:.4f}
    Train Accuracy: {train_metrics['accuracy']:.2f}%

    Validation Loss: {val_metrics['loss']:.4f}
    Validation Accuracy: {val_metrics['accuracy']:.2f}%

    -----------------------------
                """
            )


        return self.history
    

    def save_training_result(
    self,
    project_id: str
    ):
        """
        Saves the trained model.
        """

        final_metrics = {
            "train_accuracy":
                self.history["train_accuracy"][-1],

            "validation_accuracy":
                self.history["val_accuracy"][-1],

            "train_loss":
                self.history["train_loss"][-1],

            "validation_loss":
                self.history["val_loss"][-1]
        }


        model_metadata = self.model_manager.save_model(
            model=self.model,

            project_id=project_id,

            model_name=(
                f"{self.config.architecture}_"
                "model"
            ),

            classes=self.classes,

            metrics=final_metrics,

            config=self.config.__dict__
        )


        return model_metadata