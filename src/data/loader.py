"""Data loader for raw and processed datasets."""

from pathlib import Path
from typing import Optional
import pandas as pd
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("DataLoader")

def load_raw_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    path = file_path or settings.DEFAULT_RAW_FILE
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {path}")
        
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")
        
    logger.info(f"Loaded raw dataset from {path} with {len(df)} rows and {len(df.columns)} columns.")
    return df

def load_cleaned_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    path = file_path or settings.CLEANED_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at: {path}. Run data rescue first.")
    df = pd.read_csv(path, encoding="utf-8")
    return df

def save_cleaned_data(df: pd.DataFrame, file_path: Optional[Path] = None) -> Path:
    path = file_path or settings.CLEANED_DATA_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    logger.info(f"Saved cleaned dataset to {path}")
    return path