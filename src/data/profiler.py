"""Automated data profiling for unknown organizer datasets."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from src.config.schema_map import resolve_column_mapping

def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyzes raw dataset to report shape, missing values, duplicates, and candidate columns."""
    total_rows, total_cols = df.shape
    duplicate_rows = int(df.duplicated().sum())
    
    col_profiles: Dict[str, Any] = {}
    for col in df.columns:
        s = df[col]
        null_count = int(s.isna().sum())
        n_unique = int(s.nunique(dropna=True))
        sample_vals = [str(x) for x in s.dropna().head(5).tolist()]
        
        # Detect candidate types
        is_numeric = pd.api.types.is_numeric_dtype(s)
        sample_lower = [str(x).lower().strip() for x in sample_vals]
        possible_bool = any(x in ["yes", "no", "hai", "nahi", "1", "0", "true", "false"] for x in sample_lower)
        
        col_profiles[str(col)] = {
            "dtype": str(s.dtype),
            "null_count": null_count,
            "null_percentage": round((null_count / max(1, total_rows)) * 100, 1),
            "unique_count": n_unique,
            "sample_values": sample_vals,
            "is_numeric": is_numeric,
            "possible_boolean": possible_bool,
        }
        
    mapped_schema = resolve_column_mapping(list(df.columns))
    
    return {
        "total_rows": total_rows,
        "total_columns": total_cols,
        "duplicate_rows": duplicate_rows,
        "columns": col_profiles,
        "auto_detected_mapping": mapped_schema,
    }