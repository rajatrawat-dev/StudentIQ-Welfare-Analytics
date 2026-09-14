"""Trains and evaluates the School Retention Risk ML Model."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ml.train import train_and_save_model
from src.config.settings import settings

def run_train():
    print("==================================================")
    print("     STUDENTIQ -- DROPOUT RISK ML TRAINING        ")
    print("==================================================")
    
    metrics = train_and_save_model()
    print(f"Status:            {metrics.get('status')}")
    print(f"Message:           {metrics.get('message')}")
    if metrics.get("status") == "TRAINED":
        print(f"Accuracy:          {metrics.get('accuracy')}")
        print(f"F1-Macro:          {metrics.get('f1_macro')}")
        print(f"Training Samples:  {metrics.get('n_train')}")
        print(f"Test Samples:      {metrics.get('n_test')}")
    print(f"Model saved to:    {settings.MODEL_PATH}")
    print("==================================================")

if __name__ == "__main__":
    run_train()