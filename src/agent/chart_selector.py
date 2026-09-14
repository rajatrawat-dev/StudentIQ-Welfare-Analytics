"""Deterministic chart recommendation and validation engine."""

import pandas as pd

def recommend_chart(intent: str, df: pd.DataFrame) -> str:
    """Selects the mathematically most appropriate visualization:
    - Comparison -> 'bar'
    - Trend / Time -> 'line'
    - Relationship -> 'scatter'
    - Distribution -> 'histogram'
    - Ranking -> 'horizontal_bar'
    - Composition -> 'donut'
    - Single Metric -> 'kpi_card'
    """
    if df.empty:
        return "table"
        
    rows, cols = df.shape
    
    if rows == 1 and cols <= 3:
        return "kpi_card"
        
    if intent in ["ATTENDANCE_VS_TEST", "ATTENDANCE_VS_MEAL"] or ("avg_student_attendance_pct" in df.columns and "avg_test_score" in df.columns):
        return "scatter"
        
    if intent == "HIGH_RISK_SCHOOLS" or ("school_name" in df.columns and "reported_dropout_rate_pct" in df.columns and rows <= 15):
        return "horizontal_bar"
        
    if intent == "DROPOUT_BY_DISTRICT" or ("district" in df.columns and "avg_dropout_rate" in df.columns):
        return "bar"
        
    if intent == "ELECTRICITY_COMPARISON" or ("status" in df.columns and "avg_test_score" in df.columns):
        return "bar"
        
    if "retention_risk_level" in df.columns and ("percentage" in df.columns or "school_count" in df.columns):
        return "donut"
        
    if cols >= 4:
        return "table"
        
    return "bar"