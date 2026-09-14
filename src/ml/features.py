"""Feature preparation for school retention and dropout risk modeling."""

from typing import Tuple, List
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

NUMERICAL_FEATURES = [
    "total_enrolled",
    "avg_student_attendance_pct",
    "avg_test_score",
    "mdm_grain_procured_kg",
    "infrastructure_score",
]

BOOLEAN_FEATURES = [
    "has_electricity",
    "has_drinking_water",
    "has_separate_girls_toilet",
    "has_boys_toilet",
    "mdm_served_status",
]

def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("passthrough", "passthrough", BOOLEAN_FEATURES)
        ],
        remainder="drop"
    )

def prepare_xy(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    cols = NUMERICAL_FEATURES + BOOLEAN_FEATURES + ["retention_risk_level"]
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for ML: {missing}")

    X = df[NUMERICAL_FEATURES + BOOLEAN_FEATURES].copy()
    for b in BOOLEAN_FEATURES:
        X[b] = X[b].astype(int)
    y = df["retention_risk_level"].copy()
    return X, y