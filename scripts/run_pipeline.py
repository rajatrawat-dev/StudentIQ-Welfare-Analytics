"""Master Reproducibility Pipeline Script.
Executes Inspect -> Clean -> Build DuckDB -> Train Model in one single command.
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.inspect_data import inspect
from scripts.clean_data import run_cleaning
from scripts.build_database import build_db
from scripts.train_model import run_train
from src.config.settings import settings

def run_full_pipeline(file_path: str = None):
    target_file = file_path or str(settings.DEFAULT_RAW_FILE)
    print("##################################################")
    print("   STUDENTIQ -- MASTER REPRODUCIBLE PIPELINE      ")
    print("##################################################\n")
    
    # 1. Inspect
    inspect(target_file)
    print("\n")
    
    # 2. Clean
    run_cleaning(target_file)
    print("\n")
    
    # 3. Build DuckDB
    build_db()
    print("\n")
    
    # 4. Train Model
    run_train()
    print("\n")
    
    print("##################################################")
    print("   ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!    ")
    print("##################################################")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run complete StudentIQ pipeline")
    parser.add_argument("--file", type=str, default=None, help="Path to raw dataset")
    args = parser.parse_args()
    run_full_pipeline(args.file)