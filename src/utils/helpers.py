"""General helper functions and clean UI HTML rendering utilities."""

import json
from typing import Any
import numpy as np
import pandas as pd

class SafeJSONEncoder(json.JSONEncoder):
    """Safely serializes NumPy, Pandas, and Path types."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, (bool, np.bool_)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp, pd.DatetimeIndex)):
            return obj.isoformat()
        if hasattr(obj, "__fspath__"):
            return str(obj)
        return super().default(obj)

def safe_json_dumps(data: Any, indent: int = 2) -> str:
    return json.dumps(data, cls=SafeJSONEncoder, indent=indent)

def safe_round(value: Any, decimals: int = 2) -> float:
    try:
        if pd.isna(value) or value is None:
            return 0.0
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return 0.0

def clean_html(html_str: str) -> str:
    """Removes leading indentation from multiline HTML strings.
    Crucial for Streamlit: prevents Python-Markdown from interpreting 4-space indents as raw code blocks!
    """
    lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    return "".join(lines)