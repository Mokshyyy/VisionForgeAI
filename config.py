from pathlib import Path


BASE_DIR = Path(__file__).parent


# Storage directories
STORAGE_DIR = BASE_DIR / "storage"

PROJECTS_DIR = STORAGE_DIR / "projects"
DATASETS_DIR = STORAGE_DIR / "datasets"
MODELS_DIR = STORAGE_DIR / "models"
EXPERIMENTS_DIR = STORAGE_DIR / "experiments"


# Supported image formats
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# Training defaults
DEFAULT_IMAGE_SIZE = 224
DEFAULT_BATCH_SIZE = 32
DEFAULT_LEARNING_RATE = 1e-3
DEFAULT_EPOCHS = 10


# Models available
AVAILABLE_MODELS = {
    "ResNet18": "resnet18",
    "MobileNetV3": "mobilenet_v3_small",
    "EfficientNet-B0": "efficientnet_b0"
}

# Create storage directories automatically

STORAGE_DIR.mkdir(
    exist_ok=True
)

PROJECTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATASETS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPERIMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)