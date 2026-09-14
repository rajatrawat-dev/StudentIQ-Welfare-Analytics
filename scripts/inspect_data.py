"""Inspects and profiles any raw dataset before data rescue."""

import sys
import argparse
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.profiler import profile_dataset
from src.config.settings import settings

def inspect(file_path: str):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found at {path}")
        sys.exit(1)
        
    print("==================================================")
    print(f"    DATA INSPECTION & PROFILING: {path.name}     ")
    print("==================================================")
    
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")
        
    profile = profile_dataset(df)
    
    print(f"Total Rows:       {profile['total_rows']}")
    print(f"Total Columns:    {profile['total_columns']}")
    print(f"Duplicate Rows:   {profile['duplicate_rows']}")
    print("\n--- DETECTED COLUMN MAPPINGS TO CANONICAL SCHEMA ---")
    for canonical, matched in profile["auto_detected_mapping"].items():
        status = f"-> Matched: '{matched}'" if matched else "-> (Not found in raw data)"
        print(f"  {canonical:<28} {status}")
        
    print("\n--- COLUMN DETAILS & SUSPICIOUS ANOMALIES ---")
    for col_name, info in profile["columns"].items():
        print(f"\n* Column: '{col_name}' (dtype: {info['dtype']})")
        print(f"  Missing: {info['null_count']} ({info['null_percentage']}%) | Unique Values: {info['unique_count']}")
        print(f"  Sample Values: {info['sample_values']}")
        if info["possible_boolean"]:
            print("  [Notice]: Column contains candidate boolean variations (Yes/No/Hai/Nahi/1/0)")
    print("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect raw dataset")
    parser.add_argument("--file", type=str, default=str(settings.DEFAULT_RAW_FILE), help="Path to raw CSV file")
    args = parser.parse_args()
    inspect(args.file)