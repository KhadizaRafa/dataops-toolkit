import pytest
import pandas as pd
import json
from dataops.converters import convert_json_to_excel

def test_json_flattening(tmp_path):
    """Test that nested dicts are flattened and fields can be accessed via dot notation."""
    json_file = tmp_path / "flatten.json"
    excel_file = tmp_path / "output.xlsx"
    
    data = [
        {
            "id": 1,
            "info": {
                "name": "Alice",
                "details": {"age": 30}
            }
        },
        {
            "id": 2,
            "info": {
                "name": "Bob",
                "details": {"age": 25}
            }
        }
    ]
    with open(json_file, 'w') as f:
        json.dump(data, f)
        
    # Map flattened keys to headers
    # "info_name" comes from info.name (default sep is _)
    mapping = {"id": "ID", "info_name": "Name", "info_details_age": "Age"}
    
    convert_json_to_excel(str(json_file), str(excel_file), fields=mapping)
    
    assert excel_file.exists()
    df = pd.read_excel(excel_file)
    assert len(df) == 2
    assert "Name" in df.columns
    assert "Age" in df.columns
    assert df.iloc[0]["Name"] == "Alice"
    assert df.iloc[0]["Age"] == 30
