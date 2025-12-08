import pytest
import pandas as pd
from dataops.merger import merge_csv_files

def test_merge_csv_files(tmp_path):
    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    output = tmp_path / "merged.csv"
    
    pd.DataFrame([{"a": 1}]).to_csv(file1, index=False)
    pd.DataFrame([{"a": 2}]).to_csv(file2, index=False)
    
    merge_csv_files([str(file1), str(file2)], str(output))
    
    assert output.exists()
    df = pd.read_csv(output)
    assert len(df) == 2
    assert df["a"].tolist() == [1, 2]
