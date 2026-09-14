"""Tests for welfare metrics calculation."""

import pytest
import pandas as pd
from src.analytics.metrics import compute_overall_kpis

def test_compute_kpis():
    df = pd.DataFrame([
        {
            "school_id": "SCH-1",
            "total_enrolled": 200,
            "avg_student_attendance_pct": 80.0,
            "reported_dropout_rate_pct": 5.0,
            "mdm_served_status": True,
            "has_electricity": True,
            "has_drinking_water": True,
            "has_separate_girls_toilet": True,
            "retention_risk_level": "LOW"
        },
        {
            "school_id": "SCH-2",
            "total_enrolled": 300,
            "avg_student_attendance_pct": 50.0,
            "reported_dropout_rate_pct": 22.0,
            "mdm_served_status": False,
            "has_electricity": False,
            "has_drinking_water": False,
            "has_separate_girls_toilet": False,
            "retention_risk_level": "CRITICAL"
        }
    ])
    kpis = compute_overall_kpis(df)
    assert kpis["total_schools"] == 2
    assert kpis["total_students"] == 500
    assert kpis["mdm_coverage_pct"] == 50.0
    assert kpis["electricity_pct"] == 50.0
    assert kpis["critical_schools"] == 1