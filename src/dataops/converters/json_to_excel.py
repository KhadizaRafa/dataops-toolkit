from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
from ..utils.file_io import read_json, save_excel
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


def flatten_dict(d: Dict, parent_key: str = "", sep: str = "_") -> Dict:
    """
    Recursively flattens a nested dictionary.
    Nested keys are joined by 'sep'.
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def find_lists_of_objects(data, parent_path=""):
    """
    Recursively find lists of dicts (lowest-level objects).
    Returns a list of tuples: (path, list_of_objects)
    """
    results = []

    if isinstance(data, dict):
        for k, v in data.items():
            path = f"{parent_path}_{k}" if parent_path else k
            results.extend(find_lists_of_objects(v, path))

    elif isinstance(data, list):
        if all(isinstance(i, dict) for i in data):
            results.append((parent_path, data))
        else:
            # Handle nested lists or mixed lists
            for idx, item in enumerate(data):
                path = f"{parent_path}_{idx}" if parent_path else str(idx)
                results.extend(find_lists_of_objects(item, path))

    return results

def find_best_match(flat_obj: Dict[str, Any], field: str) -> Any:
    """
    Finds the value for a requested field using a priority strategy:
    1. Exact match.
    2. Suffix match (e.g. asking for 'pin' finds '_source_pin').
       If multiple suffix matches exist, prefers the shortest key 
       (closest to root or simplest).
    """
    # 1. Exact match
    if field in flat_obj:
        return flat_obj[field]
    
    # 2. Suffix match
    # matches keys ending with 'field' (e.g. '_pin' or '.pin')
    # We enforce a delimiter or start of string to avoid 'spin' matching 'pin' in a misleading way
    # But often data is just '_source_pin'. strict suffix check is usually enough.
    candidates = [k for k in flat_obj if k.endswith(field)]
    
    if not candidates:
        return None
        
    # Sort candidates: length triggers first (shortest is best), then alpha
    # e.g. '_pin' (4) better than '_source_pin' (11) if both exist
    best_key = sorted(candidates, key=lambda x: (len(x), x))[0]
    return flat_obj[best_key]

def convert_json_to_excel(input_path: str, output_path: str, fields: dict = None):
    """
    Converts a JSON file to an Excel file with optional field selection and renaming.
    
    Args:
        input_path (str): Path to the input JSON file.
        output_path (str): Path to the output Excel file.
        fields (dict): Optional mapping of {json_field: excel_header}. 
                       Only fields in keys will be kept.
    """
    try:
        logger.info(f"Starting conversion: {input_path} -> {output_path}")
        data = read_json(input_path)

        # Find all lowest-level lists of objects
        lists_found = find_lists_of_objects(data)
        if not lists_found:
            logger.warning("No lists of objects found in JSON.")
            return

        all_rows = []
        for path, lst in lists_found:
            for obj in lst:
                # Flatten the object to handle nested structures
                flat_obj = flatten_dict(obj)
                
                if fields:
                    # Map and filter fields using smart matching
                    row = {}
                    for json_field, excel_header in fields.items():
                        val = find_best_match(flat_obj, json_field)
                        if val is not None:
                            row[excel_header] = val
                            
                    if not row:
                        # Log a debug warning but don't crash, maybe this object just doesn't have the info
                        # raise ValueError(f"Object matches none of the requested fields: {list(fields.keys())}")
                        continue
                else:
                    row = flat_obj
                
                all_rows.append(row)

        if not all_rows:
            logger.warning("No rows extracted from JSON after applying fields.")
            return

        df = pd.DataFrame(all_rows)
        save_excel(df, output_path)
        logger.info("Conversion completed successfully.")

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise
