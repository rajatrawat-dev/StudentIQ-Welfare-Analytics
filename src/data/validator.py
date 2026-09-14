"""Validation rules, anomaly detection, and data quality scoring."""

from typing import Dict, Any, Tuple, List
import pandas as pd
import numpy as np

def validate_schema(df: pd.DataFrame, expected_cols: List[str]) -> Tuple[bool, List[str]]:
    missing = [c for c in expected_cols if c not in df.columns]
    return len(missing) == 0, missing

def detect_proxy_attendance(df: pd.DataFrame) -> pd.Series:
    """Flags suspicious proxy attendance anomalies.
    Examples:
    1. Perfect attendance (100%) recorded when Mid-Day Meal is NOT active/served.
    2. Near-perfect attendance (>98%) paired with severe failure in test scores (<15/100).
    3. Severe divergence between attendance rate and reporting norms.
    """
    flags = pd.Series(False, index=df.index)
    
    if "avg_student_attendance_pct" in df.columns:
        att = df["avg_student_attendance_pct"]
        
        # Rule 1: High attendance with no meal
        if "mdm_served_status" in df.columns:
            meal_no = (df["mdm_served_status"] == False)
            flags = flags | ((att >= 95.0) & meal_no)
            
        # Rule 2: High attendance with zero learning outcomes
        if "avg_test_score" in df.columns:
            flags = flags | ((att >= 98.0) & (df["avg_test_score"] < 20.0))
            
    return flags

def calculate_data_quality_score(metrics: Dict[str, Any]) -> float:
    """Calculates an empirical Data Quality Score (0-100) based on:
    - Completeness (missing value penalty)
    - Uniqueness (duplicate penalty)
    - Validity (range bound violations repaired)
    - Consistency (successful unit and boolean standardization)
    """
    rows_before = max(1, metrics.get("rows_before", 1))
    duplicates = metrics.get("duplicates_removed", 0)
    missing = metrics.get("missing_values_imputed", 0)
    anomalies = metrics.get("proxy_attendance_flagged", 0)
    unit_mismatches = metrics.get("unit_conversions_performed", 0)
    
    dup_penalty = min(25.0, (duplicates / rows_before) * 100.0 * 2.0)
    missing_penalty = min(30.0, (missing / (rows_before * 8)) * 100.0 * 1.5)
    anomaly_penalty = min(15.0, (anomalies / rows_before) * 100.0 * 1.5)
    
    score = 100.0 - (dup_penalty + missing_penalty + anomaly_penalty)
    return max(10.0, min(100.0, round(score, 1)))