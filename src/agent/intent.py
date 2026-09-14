"""Intent classification mapping natural language questions to analytical concepts."""

from typing import Tuple, Dict, Any

def detect_intent(question: str) -> Tuple[str, Dict[str, Any]]:
    q = question.lower()
    
    # 1. Electricity vs Academic Performance
    if ("electricity" in q or "power" in q) and ("test" in q or "score" in q or "learning" in q or "compare" in q):
        return "ELECTRICITY_COMPARISON", {}
        
    # 2. Dropout by district
    if ("dropout" in q or "retention" in q) and ("district" in q or "region" in q or "zila" in q):
        return "DROPOUT_BY_DISTRICT", {}
        
    # 3. Attendance vs Meal
    if ("meal" in q or "mdm" in q or "khana" in q) and ("attendance" in q or "presence" in q):
        return "ATTENDANCE_VS_MEAL", {}
        
    # 4. Attendance vs Test score correlation
    if ("attendance" in q and ("score" in q or "marks" in q or "test" in q)):
        return "ATTENDANCE_VS_TEST", {}
        
    # 5. Grain procurement trends or volume
    if "grain" in q or "procurement" in q or "ration" in q or "quintal" in q:
        return "GRAIN_PROCUREMENT", {}
        
    # 6. High risk schools / intervention queue
    if "high risk" in q or "intervention" in q or "priority" in q or "critical" in q or "needing support" in q:
        return "HIGH_RISK_SCHOOLS", {}
        
    # 7. Infrastructure gaps
    if "infrastructure" in q or "toilet" in q or "water" in q or "gap" in q:
        return "INFRASTRUCTURE_GAPS", {}
        
    return "GENERAL_ANALYTICS", {}