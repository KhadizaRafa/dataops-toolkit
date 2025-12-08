import pytest
import pandas as pd
import json
from dataops.converters import convert_json_to_excel
from dataops.merger import merge_csv_files
from click.testing import CliRunner
from dataops.cli import main

def test_json_to_excel_mapping_cli(tmp_path):
    runner = CliRunner()
    json_file = tmp_path / "test.json"
    excel_file = tmp_path / "output.xlsx"
    
    data = [
        {"key": "0108", "doc_count": 49, "ignore": "this"},
        {"key": "0109", "doc_count": 50, "ignore": "this"}
    ]
    with open(json_file, 'w') as f:
        json.dump(data, f)
        
    result = runner.invoke(main, [
        "json-to-excel", 
        str(json_file), 
        str(excel_file),
        "--json-fields", "key,doc_count",
        "--output-headers", "id,count"
    ])
    
    assert result.exit_code == 0
    
    # Read as string to preserve leading zeros
    df = pd.read_excel(excel_file, dtype=str)
    assert list(df.columns) == ["id", "count"]
    assert df.iloc[0]["id"] == "0108"
    assert df.iloc[0]["count"] == "49"

def test_json_nested_structure(tmp_path):
    """Test extracting data from nested lists (Elasticsearch style)."""
    json_file = tmp_path / "nested.json"
    excel_file = tmp_path / "output.xlsx"
    
    # Elasticsearch-like structure
    data = {
        "took": 310,
        "aggregations": {
            "by_upozila": {
                "buckets": [
                    {"key": "0108", "doc_count": 49},
                    {"key": "0114", "doc_count": 31}
                ]
            }
        }
    }
    with open(json_file, 'w') as f:
        json.dump(data, f)
        
    mapping = {"key": "id", "doc_count": "count"}
    
    # Run conversion
    convert_json_to_excel(str(json_file), str(excel_file), fields=mapping)
    
    # Verify
    assert excel_file.exists()
    df = pd.read_excel(excel_file, dtype=str)
    assert len(df) == 2
    assert "id" in df.columns
    assert "count" in df.columns
    assert df.iloc[0]["id"] == "0108"
    assert df.iloc[0]["count"] == "49"

def test_merge_join(tmp_path):
    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    output = tmp_path / "merged.csv"
    
    pd.DataFrame([{"id": 1, "val1": "a"}]).to_csv(file1, index=False)
    pd.DataFrame([{"id": 1, "val2": "b"}]).to_csv(file2, index=False)
    
    merge_csv_files(
        [str(file1), str(file2)], 
        str(output), 
        join_on=["id"], 
        how="inner"
    )
    
    df = pd.read_csv(output)
    assert len(df) == 1
    assert df.iloc[0]["val1"] == "a"
    assert df.iloc[0]["val2"] == "b"
