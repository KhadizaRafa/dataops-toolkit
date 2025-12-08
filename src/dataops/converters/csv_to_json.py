from pathlib import Path
from ..utils.file_io import read_csv, save_json
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def convert_csv_to_json(input_path: str, output_path: str):
    """
    Converts a CSV file to a JSON file.
    
    Args:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to the output JSON file.
    """
    try:
        logger.info(f"Starting conversion: {input_path} -> {output_path}")
        df = read_csv(input_path)
        data = df.to_dict(orient="records")
        save_json(data, output_path)
        logger.info("Conversion completed successfully.")
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise
