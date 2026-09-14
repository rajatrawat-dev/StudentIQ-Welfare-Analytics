"""Executes the 14-Step Data Rescue Pipeline."""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_raw_data, save_cleaned_data
from src.data.cleaner import WelfareDataCleaner
from src.config.settings import settings

def run_cleaning(file_path: str = None):
    print("==================================================")
    print("     STUDENTIQ -- DATA RESCUE PIPELINE            ")
    print("==================================================")
    
    raw_path = Path(file_path) if file_path else settings.DEFAULT_RAW_FILE
    raw_df = load_raw_data(raw_path)
    
    cleaner = WelfareDataCleaner()
    cleaned_df, report = cleaner.clean(raw_df)
    
    save_cleaned_data(cleaned_df)
    cleaner.report.save()
    
    print("\n--- DATA RESCUE AUDIT REPORT ---")
    print(f"Rows Before:                     {report['rows_before']}")
    print(f"Rows After:                      {report['rows_after']}")
    print(f"Duplicates Removed:              {report['duplicates_removed']}")
    print(f"Boolean Values Standardized:     {report['boolean_values_standardized']}")
    print(f"Unit Conversions (to KG):        {report['unit_conversions_performed']}")
    print(f"Missing Values Imputed:          {report['missing_values_imputed']}")
    print(f"Proxy Attendance Flagged:        {report['proxy_attendance_flagged']}")
    print(f"Calculated Data Quality Score:   {report['data_quality_score']}/100")
    print("==================================================")
    print(f"Cleaned dataset saved: {settings.CLEANED_DATA_PATH}")
    print(f"Quality report saved:  {settings.QUALITY_REPORT_PATH}")
    print("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=None, help="Path to raw CSV")
    args = parser.parse_args()
    run_cleaning(args.file)