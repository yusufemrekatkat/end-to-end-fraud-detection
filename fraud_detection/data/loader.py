"""Data loading and I/O operations.
Isolates the storage format from the rest of the application.
"""

import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame.
    
    Args:
        path: Path to CSV file.
    Returns:
        DataFrame with parsed timestamps.
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not path.exists():
        logger.error(f"Data file not found: {path}")
        raise FileNotFoundError(f"Data file not found: {path}")

    logger.info(f"Loading data from {path}")
    # Timestamps are auto-parsed during loading
    df = pd.read_csv(path, parse_dates=["timestamp"])
    logger.info(f"Loaded {len(df)} rows from {path.name}")
    
    return df

def save_csv(df: pd.DataFrame, path: Path) -> None:
    """Save a DataFrame to CSV, ensuring parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Saved {len(df)} rows to {path}")