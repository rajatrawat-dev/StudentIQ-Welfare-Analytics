"""Pre-built analytical queries executed safely through DuckDB."""

from typing import Dict, Any, Optional, List
import pandas as pd
from src.analytics.database import db_manager

def get_kpis() -> Dict[str, Any]:
    query = """
    SELECT 
        COUNT(*) as total_schools,
        SUM(total_enrolled) as total_students,
        ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
        ROUND(AVG(avg_test_score), 1) as avg_test_score,
        ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate,
        ROUND(SUM(CASE WHEN mdm_served_status THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as mdm_coverage_pct,
        ROUND(SUM(CASE WHEN has_electricity THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as electricity_pct,
        ROUND(SUM(CASE WHEN has_drinking_water THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as water_pct,
        ROUND(SUM(CASE WHEN has_separate_girls_toilet THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as girls_toilet_pct,
        SUM(CASE WHEN retention_risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_schools,
        SUM(CASE WHEN retention_risk_level = 'CRITICAL' THEN 1 ELSE 0 END) as critical_schools,
        COUNT(DISTINCT district) as total_districts
    FROM schools;
    """
    df = db_manager.execute_query(query)
    if df.empty:
        return {}
    r = df.iloc[0]
    return {
        "total_schools": int(r["total_schools"] or 0),
        "total_students": int(r["total_students"] or 0),
        "avg_attendance": float(r["avg_attendance"] or 0.0),
        "avg_test_score": float(r["avg_test_score"] or 0.0),
        "avg_dropout_rate": float(r["avg_dropout_rate"] or 0.0),
        "mdm_coverage_pct": float(r["mdm_coverage_pct"] or 0.0),
        "electricity_pct": float(r["electricity_pct"] or 0.0),
        "water_pct": float(r["water_pct"] or 0.0),
        "girls_toilet_pct": float(r["girls_toilet_pct"] or 0.0),
        "at_risk_schools": int(r["at_risk_schools"] or 0),
        "critical_schools": int(r["critical_schools"] or 0),
        "total_districts": int(r["total_districts"] or 0),
    }

def get_district_summary() -> pd.DataFrame:
    query = """
    SELECT * FROM district_summary 
    ORDER BY avg_dropout_rate DESC;
    """
    return db_manager.execute_query(query)

def get_risk_distribution() -> pd.DataFrame:
    query = """
    SELECT * FROM risk_summary 
    ORDER BY 
        CASE retention_risk_level 
            WHEN 'CRITICAL' THEN 1 
            WHEN 'HIGH' THEN 2 
            WHEN 'MEDIUM' THEN 3 
            ELSE 4 
        END;
    """
    return db_manager.execute_query(query)

def get_electricity_impact_on_learning() -> pd.DataFrame:
    """Answers official question: Compare test scores between schools with/without electricity."""
    query = """
    SELECT 
        CASE WHEN has_electricity THEN 'Functional Electricity' ELSE 'No Electricity' END as status,
        COUNT(*) as school_count,
        ROUND(AVG(avg_test_score), 1) as avg_test_score,
        ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
        ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate
    FROM schools
    GROUP BY has_electricity;
    """
    return db_manager.execute_query(query)

def get_mdm_impact_on_attendance() -> pd.DataFrame:
    """Evaluates correlation between Mid-Day Meal availability and attendance."""
    query = """
    SELECT 
        CASE WHEN mdm_served_status THEN 'Mid-Day Meal Active' ELSE 'Mid-Day Meal Disrupted' END as mdm_status,
        COUNT(*) as school_count,
        ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
        ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate,
        ROUND(AVG(avg_test_score), 1) as avg_test_score
    FROM schools
    GROUP BY mdm_served_status;
    """
    return db_manager.execute_query(query)

def get_high_risk_schools(limit: int = 25) -> pd.DataFrame:
    query = f"""
    SELECT 
        school_id,
        school_name,
        district,
        has_electricity,
        has_drinking_water,
        has_separate_girls_toilet,
        mdm_served_status,
        avg_student_attendance_pct,
        reported_dropout_rate_pct,
        welfare_efficacy_index,
        retention_risk_level,
        priority_action
    FROM schools
    WHERE retention_risk_level IN ('CRITICAL', 'HIGH')
    ORDER BY reported_dropout_rate_pct DESC, infrastructure_score ASC
    LIMIT {limit};
    """
    return db_manager.execute_query(query)

def filter_schools(
    district: Optional[str] = None,
    risk_level: Optional[str] = None,
    electricity_only: Optional[bool] = None,
    water_only: Optional[bool] = None,
    girls_toilet_only: Optional[bool] = None,
    mdm_active_only: Optional[bool] = None,
    search_term: Optional[str] = None,
    limit: int = 200
) -> pd.DataFrame:
    conditions = ["1=1"]
    params: List[Any] = []

    if district and district != "All":
        conditions.append("district = ?")
        params.append(district)
    if risk_level and risk_level != "All":
        conditions.append("retention_risk_level = ?")
        params.append(risk_level)
    if electricity_only:
        conditions.append("has_electricity = true")
    if water_only:
        conditions.append("has_drinking_water = true")
    if girls_toilet_only:
        conditions.append("has_separate_girls_toilet = true")
    if mdm_active_only:
        conditions.append("mdm_served_status = true")
    if search_term:
        conditions.append("(LOWER(school_name) LIKE ? OR LOWER(school_id) LIKE ?)")
        st = f"%{search_term.lower()}%"
        params.extend([st, st])

    where_clause = " AND ".join(conditions)
    query = f"""
    SELECT 
        school_id,
        school_name,
        district,
        total_enrolled,
        has_electricity,
        has_drinking_water,
        has_separate_girls_toilet,
        mdm_served_status,
        avg_student_attendance_pct,
        avg_test_score,
        reported_dropout_rate_pct,
        proxy_attendance_flag,
        welfare_efficacy_index,
        retention_risk_level
    FROM schools
    WHERE {where_clause}
    ORDER BY reported_dropout_rate_pct DESC
    LIMIT {limit};
    """
    return db_manager.execute_query(query, params)