import pytest
import pandas as pd
from dataops.validator import validate_csv_data

def test_validate_csv_data(tmp_path):
    csv_file = tmp_path / "test.csv"
    
    # Create data with duplicates and missing value in 'b'
    df = pd.DataFrame([
        {"a": 1, "b": 2},
        {"a": 1, "b": 2}, # Duplicate
        {"a": 3, "b": None} # Missing
    ])
    df.to_csv(csv_file, index=False)
    
    report = validate_csv_data(str(csv_file))
    
    assert report["total_rows"] == 3
    assert report["duplicates"] == 1
    assert report["missing_values"]["b"] == 1
    assert report["missing_values"]["a"] == 0
