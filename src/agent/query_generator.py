"""SQL generator with Dual Mode: Local Ollama LLM + Deterministic Rule Engine."""

import re
import requests
from typing import Tuple
from src.config.settings import settings
from src.agent.prompts import SYSTEM_PROMPT

def generate_sql_via_rules(intent: str, question: str) -> str:
    """Deterministic fallback producing verified, accurate DuckDB SQL without any LLM."""
    q = question.lower()
    
    # 1. Compare average test scores between schools with and without functional electricity
    if intent == "ELECTRICITY_COMPARISON":
        return """
SELECT 
    CASE WHEN has_electricity THEN 'Functional Electricity' ELSE 'No Electricity' END as status,
    COUNT(*) as school_count,
    ROUND(AVG(avg_test_score), 1) as avg_test_score,
    ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
    ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate
FROM schools
GROUP BY has_electricity;
""".strip()

    # 2. Show dropout rate by district
    if intent == "DROPOUT_BY_DISTRICT":
        return """
SELECT 
    district, 
    ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate,
    COUNT(*) as total_schools,
    SUM(CASE WHEN retention_risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_schools
FROM schools
GROUP BY district
ORDER BY avg_dropout_rate DESC;
""".strip()

    # 3. Attendance versus meal availability
    if intent == "ATTENDANCE_VS_MEAL":
        return """
SELECT 
    CASE WHEN mdm_served_status THEN 'Mid-Day Meal Active' ELSE 'Mid-Day Meal Disrupted' END as meal_status,
    COUNT(*) as school_count,
    ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
    ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate
FROM schools
GROUP BY mdm_served_status;
""".strip()

    # 4. Relationship between attendance and test scores
    if intent == "ATTENDANCE_VS_TEST":
        return """
SELECT 
    school_id, 
    school_name, 
    district, 
    avg_student_attendance_pct, 
    avg_test_score, 
    reported_dropout_rate_pct,
    retention_risk_level
FROM schools
ORDER BY avg_student_attendance_pct DESC
LIMIT 100;
""".strip()

    # 5. Which schools have the highest dropout risk / need intervention?
    if intent == "HIGH_RISK_SCHOOLS":
        return """
SELECT 
    school_id, 
    school_name, 
    district, 
    reported_dropout_rate_pct,
    avg_student_attendance_pct,
    infrastructure_score,
    retention_risk_level,
    priority_action
FROM schools
WHERE retention_risk_level IN ('CRITICAL', 'HIGH')
ORDER BY reported_dropout_rate_pct DESC, infrastructure_score ASC
LIMIT 15;
""".strip()

    # 6. Infrastructure gaps by district
    if intent == "INFRASTRUCTURE_GAPS":
        return """
SELECT 
    district,
    COUNT(*) as total_schools,
    ROUND(SUM(CASE WHEN has_electricity THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as electricity_pct,
    ROUND(SUM(CASE WHEN has_drinking_water THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as water_pct,
    ROUND(SUM(CASE WHEN has_separate_girls_toilet THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as girls_toilet_pct,
    ROUND(AVG(infrastructure_score), 1) as avg_infrastructure_score
FROM schools
GROUP BY district
ORDER BY avg_infrastructure_score ASC;
""".strip()

    # 7. Grain procurement analysis
    if intent == "GRAIN_PROCUREMENT":
        return """
SELECT 
    district,
    ROUND(SUM(mdm_grain_procured_kg), 1) as total_grain_kg,
    ROUND(AVG(mdm_grain_procured_kg), 1) as avg_grain_per_school_kg,
    ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance
FROM schools
GROUP BY district
ORDER BY total_grain_kg DESC;
""".strip()

    # Default fallback
    return """
SELECT 
    school_id, 
    school_name, 
    district, 
    reported_dropout_rate_pct, 
    avg_student_attendance_pct, 
    retention_risk_level
FROM schools
ORDER BY reported_dropout_rate_pct DESC
LIMIT 15;
""".strip()

def generate_sql_via_ollama(question: str) -> Tuple[bool, str]:
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": f"{SYSTEM_PROMPT}\nOfficer Question: {question}\nSQL Query:",
        "stream": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=settings.OLLAMA_TIMEOUT_SECONDS)
        if resp.status_code == 200:
            text = resp.json().get("response", "")
            match = re.search(r'```(?:sql)?(.*?)```', text, re.DOTALL)
            if match:
                return True, match.group(1).strip()
            return True, text.strip()
    except Exception:
        pass
    return False, ""