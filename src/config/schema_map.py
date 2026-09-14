"""Configurable mapping system to adapt to the official organizer dataset.
Inspects raw column headers and resolves them dynamically to canonical attributes.
"""

from typing import Dict, List, Optional
import re

# Synonym dictionary for candidate column detection
COLUMN_SYNONYMS: Dict[str, List[str]] = {
    "school_id": [
        "school_id", "school_code", "sch_id", "udise", "udise_code", "id", "institution_id", "school_no"
    ],
    "school_name": [
        "school_name", "school", "institution_name", "name", "school_title", "name_of_school"
    ],
    "district": [
        "district", "dist", "district_name", "zila", "region", "district_code"
    ],
    "block": [
        "block", "tehsil", "taluk", "mandal", "zone", "cluster", "block_name"
    ],
    "total_enrolled": [
        "total_enrolled", "enrollment", "total_students", "students", "enrolled", "strength", "total_strength"
    ],
    "has_electricity": [
        "has_electricity", "electricity", "power", "bijli", "electrified", "power_supply", "has_power"
    ],
    "has_drinking_water": [
        "has_drinking_water", "water", "drinking_water", "paani", "tap_water", "water_facility"
    ],
    "has_separate_girls_toilet": [
        "has_separate_girls_toilet", "girls_toilet", "toilet_girls", "separate_girls_toilet", "cwsn_toilet"
    ],
    "has_boys_toilet": [
        "has_boys_toilet", "boys_toilet", "toilet_boys", "urinal_boys", "toilet"
    ],
    "mdm_served_status": [
        "mdm_served_status", "mdm_status", "mid_day_meal_served", "mid_day_meal", "mdm_active", "meal_served", "khana_status", "meal"
    ],
    "mdm_grain_procured_kg": [
        "mdm_grain_procured_kg", "grain_quantity_procured", "grain_qty", "grain_quantity", "ration_procured", "foodgrain_kg", "grain_procurement", "grain"
    ],
    "mdm_grain_unit_raw": [
        "mdm_grain_unit_raw", "procurement_unit", "grain_unit", "unit", "ration_unit", "measurement_unit"
    ],
    "avg_student_attendance_pct": [
        "avg_student_attendance_pct", "attendance_rate", "attendance", "avg_attendance", "present_pct", "haaziri"
    ],
    "avg_test_score": [
        "avg_test_score", "average_marks", "test_score", "nas_score", "exam_score", "avg_marks", "learning_outcome", "marks", "score"
    ],
    "reported_dropout_rate_pct": [
        "reported_dropout_rate_pct", "annual_dropout_rate", "dropout_rate", "dropout_pct", "drop_out", "retention_gap", "dropout"
    ],
}

def resolve_column_mapping(raw_columns: List[str]) -> Dict[str, Optional[str]]:
    """Maps actual raw column names in organizer dataset to canonical schema.
    Returns {canonical_column_name: raw_column_name_or_None}.
    """
    resolved: Dict[str, Optional[str]] = {}
    normalized_raw = {
        re.sub(r"[^a-z0-9]", "_", str(col).strip().lower()): col
        for col in raw_columns
    }

    for canonical, synonyms in COLUMN_SYNONYMS.items():
        matched_raw = None
        for syn in synonyms:
            clean_syn = syn.lower().replace(" ", "_")
            # Exact match
            if clean_syn in normalized_raw:
                matched_raw = normalized_raw[clean_syn]
                break
            # Substring match
            for raw_norm, orig_raw in normalized_raw.items():
                if clean_syn in raw_norm:
                    matched_raw = orig_raw
                    break
            if matched_raw:
                break
        resolved[canonical] = matched_raw

    return resolved