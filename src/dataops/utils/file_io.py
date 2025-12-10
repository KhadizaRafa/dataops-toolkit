import os
import json
import pandas as pd
from typing import Union, List, Dict
from pathlib import Path
from .logger import setup_logger




logger = setup_logger(__name__)

def read_json(file_path: Union[str, Path]) -> Union[Dict, List]:
    """Reads a JSON file safely."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully read JSON file: {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error reading JSON file {file_path}: {e}")
        raise

def save_json(data: Union[Dict, List], file_path: Union[str, Path]):
    """Saves data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully saved JSON to: {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {e}")
        raise

def read_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """Reads a CSV file into a Pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully read CSV file: {file_path} with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {e}")
        raise

def save_excel(df: pd.DataFrame, file_path: Union[str, Path]):
    """Saves a DataFrame to an Excel file."""
    try:
        df.to_excel(file_path, index=False)
        logger.info(f"Successfully saved Excel file to: {file_path}")
    except Exception as e:
        logger.error(f"Error saving Excel file {file_path}: {e}")
        raise
