"""Scikit-Learn Risk Classification Pipeline and Transparent Rule-Based Fallback."""

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
from src.ml.features import build_preprocessor
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("DropoutRiskModel")

class RuleBasedDropoutClassifier:
    """Transparent deterministic fallback classifier for school dropout risk."""
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        preds = []
        for _, row in X.iterrows():
            inf = float(row.get("infrastructure_score", 60.0))
            att = float(row.get("avg_student_attendance_pct", 75.0))
            mdm = bool(row.get("mdm_served_status", True))
            
            # Risk formula combining infrastructure, attendance, and MDM
            risk_points = (100.0 - inf) * 0.45 + (100.0 - att) * 0.40 + (0.0 if mdm else 15.0)
            
            if risk_points >= 50.0:
                preds.append("CRITICAL")
            elif risk_points >= 35.0:
                preds.append("HIGH")
            elif risk_points >= 20.0:
                preds.append("MEDIUM")
            else:
                preds.append("LOW")
        return np.array(preds)

class DropoutRiskPipeline:
    def __init__(self):
        self.pipeline: Optional[Pipeline] = None
        self.fallback = RuleBasedDropoutClassifier()
        self.is_trained = False
        self.metrics: Dict[str, Any] = {}
        self.classes_ = np.array(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    def train(self, X_train: pd.DataFrame, y_train: pd.Series, X_test: Optional[pd.DataFrame] = None, y_test: Optional[pd.Series] = None) -> Dict[str, Any]:
        n_samples = len(X_train)
        if n_samples < 30 or (y_test is not None and len(y_test) < 8):
            logger.warning("Dataset too small for statistically reliable model evaluation.")
            self.metrics = {
                "status": "DATASET_TOO_SMALL",
                "message": "Dataset too small for statistically reliable model evaluation.",
                "accuracy": None,
                "f1_macro": None,
                "n_samples": n_samples,
                "using_fallback": True,
            }
            self.is_trained = True
            return self.metrics

        preprocessor = build_preprocessor()
        clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, class_weight="balanced")
        
        self.pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        self.pipeline.fit(X_train, y_train)
        self.classes_ = self.pipeline.named_steps["classifier"].classes_
        self.is_trained = True
        
        if X_test is not None and y_test is not None and len(y_test) > 0:
            y_pred = self.pipeline.predict(X_test)
            acc = round(float(accuracy_score(y_test, y_pred)), 3)
            f1 = round(float(f1_score(y_test, y_pred, average="macro", zero_division=0)), 3)
            rep = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
            
            self.metrics = {
                "status": "TRAINED",
                "message": "Random Forest model evaluated successfully.",
                "accuracy": acc,
                "f1_macro": f1,
                "report": rep,
                "n_train": len(X_train),
                "n_test": len(X_test),
                "using_fallback": False,
            }
        else:
            self.metrics = {
                "status": "TRAINED_NO_TEST",
                "message": "Trained without test split.",
                "accuracy": None,
                "n_train": len(X_train),
                "using_fallback": False,
            }
        return self.metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if self.pipeline and self.is_trained and not self.metrics.get("using_fallback"):
            try:
                return self.pipeline.predict(X)
            except Exception:
                return self.fallback.predict(X)
        return self.fallback.predict(X)

    def save(self, path = settings.MODEL_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"pipeline": self.pipeline, "metrics": self.metrics, "classes": self.classes_}, path)
        logger.info(f"Model saved to {path}")

    def load(self, path = settings.MODEL_PATH) -> bool:
        if not path.exists():
            return False
        try:
            data = joblib.load(path)
            self.pipeline = data.get("pipeline")
            self.metrics = data.get("metrics", {})
            self.classes_ = data.get("classes", np.array(["LOW", "MEDIUM", "HIGH", "CRITICAL"]))
            self.is_trained = True
            return True
        except Exception:
            return False