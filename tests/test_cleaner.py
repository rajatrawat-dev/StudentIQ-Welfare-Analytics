"""Tests for Data Rescue normalizers and cleaning pipeline."""

import pytest
import pandas as pd
from src.data.normalizer import (
    normalize_boolean,
    normalize_grain_procurement,
    normalize_attendance,
    normalize_text
)
from src.data.cleaner import WelfareDataCleaner

def test_boolean_normalization():
    # Yes variants
    for val in ["Yes", "Y", "1", "Hai", "true", "  ha  "]:
        b, mod = normalize_boolean(val)
        assert b is True, f"Failed for {val}"

    # No variants
    for val in ["No", "N", "0", "Nahi", "false", "na"]:
        b, mod = normalize_boolean(val)
        assert b is False, f"Failed for {val}"

    # Nulls
    b, _ = normalize_boolean(None)
    assert b is None

def test_grain_unit_normalization():
    # Quintals conversion to KG (1 Quintal = 100 KG)
    kg, orig_q, orig_u, conv = normalize_grain_procurement(15.0, "Quintals")
    assert kg == 1500.0
    assert orig_q == 15.0
    assert orig_u.lower() == "quintals"
    assert conv is True

    # Ton conversion to KG (1 Ton = 1000 KG)
    kg, _, _, conv = normalize_grain_procurement(2.5, "Ton")
    assert kg == 2500.0
    assert conv is True

    # Standard KG
    kg, _, _, conv = normalize_grain_procurement(500.0, "kg")
    assert kg == 500.0

def test_attendance_normalization():
    # Percentage string
    att, mod = normalize_attendance("85%")
    assert att == 85.0
    assert mod is True

    # Ratio
    att, mod = normalize_attendance(0.72)
    assert att == 72.0
    assert mod is True

    # Out of bounds typo (780 -> 78.0)
    att, _ = normalize_attendance(780)
    assert att == 78.0

def test_welfare_cleaner_pipeline():
    cleaner = WelfareDataCleaner()
    raw = pd.DataFrame([
        {
            "School Code": "SCH-101",
            "School Name": "Govt High School",
            "District Name": "North Valley",
            "Electricity Available": "Hai",
            "Drinking Water Facility": "1",
            "Separate Girls Toilet": "Yes",
            "Boys Toilet": "Y",
            "Mid Day Meal Served": "Yes",
            "Grain Quantity Procured": 10.0,
            "Procurement Unit": "Quintals",
            "Attendance Rate": "88%",
            "Average Marks": 65.0,
            "Annual Dropout Rate": 4.5
        },
        # Duplicate row
        {
            "School Code": "SCH-101",
            "School Name": "Govt High School",
            "District Name": "North Valley",
            "Electricity Available": "Hai",
            "Drinking Water Facility": "1",
            "Separate Girls Toilet": "Yes",
            "Boys Toilet": "Y",
            "Mid Day Meal Served": "Yes",
            "Grain Quantity Procured": 10.0,
            "Procurement Unit": "Quintals",
            "Attendance Rate": "88%",
            "Average Marks": 65.0,
            "Annual Dropout Rate": 4.5
        }
    ])
    cleaned_df, report = cleaner.clean(raw)
    assert len(cleaned_df) == 1
    assert report["duplicates_removed"] == 1
    assert bool(cleaned_df.iloc[0]["has_electricity"]) is True
    assert cleaned_df.iloc[0]["mdm_grain_procured_kg"] == 1000.0
    assert "retention_risk_level" in cleaned_df.columns