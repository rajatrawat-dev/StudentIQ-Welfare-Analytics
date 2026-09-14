"""Tests for schema validation, proxy attendance detection, and quality scores."""

import pytest
import pandas as pd
from src.data.validator import validate_schema, detect_proxy_attendance, calculate_data_quality_score

def test_schema_validation():
    df = pd.DataFrame(columns=["school_id", "school_name", "district", "has_electricity"])
    ok, missing = validate_schema(df, ["school_id", "district"])
    assert ok is True
    assert len(missing) == 0

    ok, missing = validate_schema(df, ["school_id", "non_existent_col"])
    assert ok is False
    assert "non_existent_col" in missing

def test_proxy_attendance_detection():
    df = pd.DataFrame([
        # Anomaly 1: 100% attendance with disrupted meal
        {"school_id": "SCH-1", "avg_student_attendance_pct": 100.0, "mdm_served_status": False, "avg_test_score": 60.0},
        # Normal
        {"school_id": "SCH-2", "avg_student_attendance_pct": 82.0, "mdm_served_status": True, "avg_test_score": 70.0},
    ])
    flags = detect_proxy_attendance(df)
    assert bool(flags.iloc[0]) is True
    assert bool(flags.iloc[1]) is False

def test_data_quality_score():
    metrics = {
        "rows_before": 100,
        "duplicates_removed": 2,
        "missing_values_imputed": 5,
        "proxy_attendance_flagged": 1,
    }
    score = calculate_data_quality_score(metrics)
    assert 80.0 <= score <= 100.0