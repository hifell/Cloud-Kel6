"""
Download Jakarta House Price Dataset dari Kaggle.
Dataset: Rumah123 / Jakarta Property Price
Target: Indonesia property data
"""

import os
import zipfile
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

def download_dataset():
    """Download dataset Jakarta House Price dari Kaggle."""
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Dataset slug - Jakarta House Price (Indonesia)
    DATASET_SLUG = "abiyyurasyiq/jakarta-house-price-dataset"
    OUTPUT_DIR = RAW_DIR

    # Create directories
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading dataset: {DATASET_SLUG}")

    # Download dataset
    api.dataset_download_files(
        DATASET_SLUG,
        path=str(OUTPUT_DIR),
        unzip=True
    )

    print(f"Dataset downloaded to: {OUTPUT_DIR}")

    # List downloaded files
    downloaded_files = list(RAW_DIR.glob("*.csv"))
    print(f"Files found: {[f.name for f in downloaded_files]}")

    return downloaded_files

if __name__ == "__main__":
    download_dataset()
