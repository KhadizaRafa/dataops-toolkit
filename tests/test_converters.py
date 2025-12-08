import pytest
import pandas as pd
import json
from dataops.converters import convert_csv_to_json, convert_json_to_excel

def test_csv_to_json(tmp_path):
    # Create dummy CSV
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "output.json"
    
    df = pd.DataFrame([{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}])
    df.to_csv(csv_file, index=False)
    
    convert_csv_to_json(str(csv_file), str(json_file))
    
    assert json_file.exists()
    with open(json_file) as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["col1"] == 1

def test_json_to_excel(tmp_path):
    # Create dummy JSON
    json_file = tmp_path / "test.json"
    excel_file = tmp_path / "output.xlsx"
    
    data = [{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]
    with open(json_file, 'w') as f:
        json.dump(data, f)
        
    convert_json_to_excel(str(json_file), str(excel_file))
    
    assert excel_file.exists()
    df = pd.read_excel(excel_file)
    assert len(df) == 2
    assert df.iloc[0]["col1"] == 1
