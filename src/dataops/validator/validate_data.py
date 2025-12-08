import pandas as pd
from typing import Dict
from ..utils.file_io import read_csv
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_csv_data(input_path: str) -> Dict[str, any]:
    """
    Validates a CSV file for common issues: duplicates, missing values.
    
    Args:
        input_path (str): Path to the CSV file.
        
    Returns:
        Dict: Validation report.
    """
    try:
        logger.info(f"Validating file: {input_path}")
        df = read_csv(input_path)
        
        report = {
            "total_rows": len(df),
            "duplicates": df.duplicated().sum(),
            "missing_values": df.isnull().sum().to_dict(),
            "columns": list(df.columns)
        }
        
        if report["duplicates"] > 0:
            logger.warning(f"Found {report['duplicates']} duplicate rows.")
        
        if any(report["missing_values"].values()):
            logger.warning(f"Found missing values: {report['missing_values']}")
            
        logger.info("Validation completed.")
        return report
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise
