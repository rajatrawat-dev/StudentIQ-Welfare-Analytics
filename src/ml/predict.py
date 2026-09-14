"""Inference service explaining school-level dropout risks."""

from typing import Dict, Any, List
import pandas as pd
from src.ml.model import DropoutRiskPipeline
from src.config.settings import settings

_model_cache: DropoutRiskPipeline = None

def get_model() -> DropoutRiskPipeline:
    global _model_cache
    if _model_cache is None:
        _model_cache = DropoutRiskPipeline()
        _model_cache.load(settings.MODEL_PATH)
    return _model_cache

def diagnose_school_risk(school_data: Dict[str, Any]) -> Dict[str, Any]:
    model = get_model()
    df_row = pd.DataFrame([school_data])
    
    pred_level = model.predict(df_row)[0]
    
    factors: List[str] = []
    if not school_data.get("has_electricity", True):
        factors.append("No functional electricity: hinders digital education & classroom engagement.")
    if not school_data.get("has_drinking_water", True):
        factors.append("No safe drinking water facility: severe basic welfare violation.")
    if not school_data.get("has_separate_girls_toilet", True):
        factors.append("Lack of dedicated girls' toilet: empirical driver of adolescent female dropouts.")
    if not school_data.get("mdm_served_status", True):
        factors.append("Mid-Day Meal disrupted: eliminates vital daily nutritional incentive.")
    if float(school_data.get("avg_student_attendance_pct", 75.0)) < 60.0:
        factors.append(f"Depressed student attendance ({school_data.get('avg_student_attendance_pct')}%) indicates critical chronic absenteeism.")
        
    if not factors:
        factors.append("Baseline infrastructure and welfare services adhere to state standards.")
        
    return {
        "school_id": school_data.get("school_id"),
        "school_name": school_data.get("school_name"),
        "predicted_risk_level": pred_level,
        "key_risk_factors": factors,
        "disclaimer": "Analytical Early-Warning Indicator only. Not a clinical or psychological evaluation.",
        "model_type": "Random Forest ML Classifier" if (model.pipeline and not model.metrics.get("using_fallback")) else "Calibrated Welfare Rule Engine"
    }