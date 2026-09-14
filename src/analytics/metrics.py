"""Core metric computations for Mid-Day Meal, Infrastructure, and Dropout correlation."""

from typing import Dict, Any
import pandas as pd
from src.utils.helpers import safe_round

def compute_overall_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {
            "total_schools": 0,
            "total_students": 0,
            "avg_attendance": 0.0,
            "avg_dropout_rate": 0.0,
            "mdm_coverage_pct": 0.0,
            "electricity_pct": 0.0,
            "water_pct": 0.0,
            "girls_toilet_pct": 0.0,
            "at_risk_schools": 0,
            "critical_schools": 0,
        }
        
    n_schools = len(df)
    n_students = int(df["total_enrolled"].sum()) if "total_enrolled" in df else 0
    at_risk = int(df["retention_risk_level"].isin(["HIGH", "CRITICAL"]).sum())
    critical = int((df["retention_risk_level"] == "CRITICAL").sum())
    
    return {
        "total_schools": n_schools,
        "total_students": n_students,
        "avg_attendance": safe_round(df["avg_student_attendance_pct"].mean(), 1),
        "avg_dropout_rate": safe_round(df["reported_dropout_rate_pct"].mean(), 1),
        "mdm_coverage_pct": safe_round((df["mdm_served_status"].sum() / n_schools) * 100.0, 1),
        "electricity_pct": safe_round((df["has_electricity"].sum() / n_schools) * 100.0, 1),
        "water_pct": safe_round((df["has_drinking_water"].sum() / n_schools) * 100.0, 1),
        "girls_toilet_pct": safe_round((df["has_separate_girls_toilet"].sum() / n_schools) * 100.0, 1),
        "at_risk_schools": at_risk,
        "critical_schools": critical,
    }