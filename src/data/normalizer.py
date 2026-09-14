"""Normalizers for boolean values (Yes/Hai/Nahi), units (Quintals/KG), and attendance."""

import re
from typing import Any, Tuple, Optional
import pandas as pd
import numpy as np
from src.config.settings import settings

def normalize_boolean(val: Any) -> Tuple[Optional[bool], bool]:
    """Converts diverse boolean inputs into Python True, False, or None.
    Handles 'Yes', 'Y', '1', 'Hai', 'No', '0', 'Nahi', whitespace, etc.
    Returns (normalized_value, was_modified).
    """
    if pd.isna(val) or val is None:
        return None, False
        
    s = str(val).strip().lower()
    
    if s in settings.BOOLEAN_YES_VALUES:
        return True, True
    elif s in settings.BOOLEAN_NO_VALUES:
        return False, True
        
    return None, True

def normalize_grain_procurement(qty_val: Any, unit_val: Any = None) -> Tuple[Optional[float], Optional[float], str, bool]:
    """Normalizes grain quantities into standard Kilograms (KG).
    Preserves original quantity and original unit.
    Converts Quintals to KG (1 Quintal = 100 KG) based on verified mathematical factors.
    Returns (qty_kg, original_qty, original_unit, was_converted).
    """
    if pd.isna(qty_val) or qty_val is None:
        return None, None, "KG", False
        
    raw_str = str(qty_val).strip()
    orig_unit = str(unit_val).strip().lower() if (unit_val and not pd.isna(unit_val)) else ""
    
    # Check if unit is embedded in the quantity string e.g. '50 Quintals' or '250 kg'
    unit_match = re.search(r'([a-zA-Z\s]+)', raw_str)
    if unit_match and not orig_unit:
        orig_unit = unit_match.group(1).strip().lower()
        
    # Extract numerical value
    num_match = re.search(r'([-+]?\d*\.?\d+)', raw_str.replace(",", ""))
    if not num_match:
        return None, None, orig_unit or "KG", False
        
    orig_qty = float(num_match.group(1))
    if orig_qty < 0:
        return None, orig_qty, orig_unit or "KG", False
        
    conversion_factor = settings.UNIT_TO_KG_FACTORS.get(orig_unit, 1.0)
    qty_kg = round(orig_qty * conversion_factor, 2)
    was_converted = (conversion_factor != 1.0) or (orig_unit != "kg")
    
    return qty_kg, orig_qty, orig_unit or "KG", was_converted

def normalize_attendance(val: Any) -> Tuple[Optional[float], bool]:
    """Normalizes student attendance to a 0.0 - 100.0 percentage float."""
    if pd.isna(val) or val is None:
        return None, False
        
    s = str(val).strip().replace("%", "").strip()
    try:
        num = float(s)
        modified = False
        
        # If expressed as decimal ratio e.g. 0.82
        if 0.0 < num <= 1.0:
            num = num * 100.0
            modified = True
        elif num < 0.0:
            return None, True
        elif num > 100.0:
            # Check for typo e.g. 850 instead of 85.0
            if num <= 1000.0 and (num / 10.0) <= 100.0:
                num = num / 10.0
                modified = True
            else:
                return None, True
                
        return round(num, 2), modified or ("%" in str(val))
    except (ValueError, TypeError):
        return None, True

def normalize_text(val: Any) -> Tuple[str, bool]:
    """Standardizes school and district names."""
    if pd.isna(val) or val is None:
        return "Unknown", False
    orig = str(val)
    cleaned = re.sub(r'\s+', ' ', orig).strip().title()
    return cleaned, (orig != cleaned)