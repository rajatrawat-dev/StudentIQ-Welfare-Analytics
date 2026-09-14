"""Tests for DuckDB query layer."""

import pytest
import pandas as pd
from src.analytics.database import db_manager
from src.analytics.queries import get_kpis, get_district_summary, get_risk_distribution

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    test_df = pd.DataFrame([
        {
            "school_id": "SCH-1",
            "school_name": "School A",
            "district": "North Valley",
            "total_enrolled": 150,
            "has_electricity": True,
            "has_drinking_water": True,
            "has_separate_girls_toilet": True,
            "has_boys_toilet": True,
            "mdm_served_status": True,
            "mdm_grain_procured_kg": 500.0,
            "avg_student_attendance_pct": 85.0,
            "avg_test_score": 75.0,
            "reported_dropout_rate_pct": 3.0,
            "proxy_attendance_flag": False,
            "infrastructure_score": 100.0,
            "welfare_efficacy_index": 95.0,
            "retention_risk_level": "LOW",
            "priority_action": "Routine Maintenance"
        },
        {
            "school_id": "SCH-2",
            "school_name": "School B",
            "district": "South Hill",
            "total_enrolled": 220,
            "has_electricity": False,
            "has_drinking_water": True,
            "has_separate_girls_toilet": False,
            "has_boys_toilet": True,
            "mdm_served_status": False,
            "mdm_grain_procured_kg": 0.0,
            "avg_student_attendance_pct": 48.0,
            "avg_test_score": 38.0,
            "reported_dropout_rate_pct": 21.0,
            "proxy_attendance_flag": False,
            "infrastructure_score": 45.0,
            "welfare_efficacy_index": 32.0,
            "retention_risk_level": "CRITICAL",
            "priority_action": "Urgent Infrastructure & Welfare Taskforce"
        }
    ])
    db_manager.init_database(test_df)

def test_get_kpis():
    kpis = get_kpis()
    assert kpis["total_schools"] == 2
    assert kpis["total_students"] == 370
    assert kpis["critical_schools"] == 1

def test_get_district_summary():
    df = get_district_summary()
    assert len(df) == 2
    assert "avg_dropout_rate" in df.columns

def test_get_risk_distribution():
    df = get_risk_distribution()
    assert len(df) == 2