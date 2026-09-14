"""Populates the DuckDB analytical store and creates views."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import settings
from src.analytics.database import db_manager
from src.data.loader import load_cleaned_data

def build_db():
    print("==================================================")
    print("     STUDENTIQ -- DUCKDB ANALYTICS BUILDER        ")
    print("==================================================")
    
    df = load_cleaned_data()
    db_manager.init_database(df)
    
    school_cnt = db_manager.execute_query("SELECT COUNT(*) as count FROM schools;").iloc[0]["count"]
    dist_cnt = db_manager.execute_query("SELECT COUNT(*) as count FROM district_summary;").iloc[0]["count"]
    
    print(f"DuckDB path:             {settings.DUCKDB_PATH}")
    print(f"Verified School Records: {school_cnt}")
    print(f"Verified Views:          district_summary ({dist_cnt} districts), risk_summary")
    print("==================================================")

if __name__ == "__main__":
    build_db()