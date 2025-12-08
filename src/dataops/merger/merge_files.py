import pandas as pd
from typing import List
from ..utils.file_io import read_csv, save_excel
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def merge_csv_files(input_files: List[str], output_path: str, join_on: List[str] = None, how: str = "inner"):
    """
    Merges multiple CSV files.
    If 'join_on' is provided, performs a join (merge) on 2 files.
    Otherwise, performs a concatenation of all files.
    
    Args:
        input_files (List[str]): List of paths to input CSV files.
        output_path (str): Path to the output file (CSV or Excel).
        join_on (List[str]): List of column names to join on. 
                             If 1 item, uses it for both. 
                             If 2 items, uses first for left, second for right.
        how (str): Type of join (inner, left, right, outer).
    """
    try:
        if join_on:
            if len(input_files) != 2:
                raise ValueError("Merging with 'on' requires exactly 2 input files.")
            
            logger.info(f"Starting {how} join of 2 files on {join_on}")
            df1 = read_csv(input_files[0])
            df2 = read_csv(input_files[1])
            
            left_on = join_on[0]
            right_on = join_on[1] if len(join_on) > 1 else join_on[0]
            
            merged_df = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)
            
        else:
            logger.info(f"Starting concatenation of {len(input_files)} files into {output_path}")
            dataframes = []
            for file in input_files:
                df = read_csv(file)
                dataframes.append(df)
                
            if not dataframes:
                logger.warning("No files to merge.")
                return

            merged_df = pd.concat(dataframes, ignore_index=True)
        
        if output_path.endswith('.xlsx'):
            save_excel(merged_df, output_path)
        else:
            merged_df.to_csv(output_path, index=False)
            logger.info(f"Successfully saved merged output to: {output_path}")
            
        logger.info("Merge completed successfully.")
    except Exception as e:
        logger.error(f"Merge failed: {e}")
        raise
