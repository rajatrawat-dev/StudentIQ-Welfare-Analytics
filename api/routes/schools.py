"""Schools directory and diagnostic endpoints."""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.analytics.queries import filter_schools
from src.analytics.database import db_manager
from src.ml.predict import diagnose_school_risk

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.get("", response_model=List[Dict[str, Any]])
def list_schools(
    district: Optional[str] = Query(None, description="Filter by district"),
    risk_level: Optional[str] = Query(None, description="Filter by retention risk level"),
    electricity_only: Optional[bool] = Query(None, description="Only electrified schools"),
    water_only: Optional[bool] = Query(None, description="Only schools with drinking water"),
    girls_toilet_only: Optional[bool] = Query(None, description="Only schools with separate girls toilet"),
    mdm_active_only: Optional[bool] = Query(None, description="Only schools with active Mid-Day Meal"),
    search: Optional[str] = Query(None, description="Search school name or ID"),
    limit: int = Query(100, ge=1, le=1000)
):
    df = filter_schools(
        district=district,
        risk_level=risk_level,
        electricity_only=electricity_only,
        water_only=water_only,
        girls_toilet_only=girls_toilet_only,
        mdm_active_only=mdm_active_only,
        search_term=search,
        limit=limit
    )
    return df.to_dict(orient="records")

@router.get("/{school_id}")
def get_school_profile(school_id: str):
    query = "SELECT * FROM schools WHERE UPPER(school_id) = UPPER(?);"
    df = db_manager.execute_query(query, [school_id])
    if df.empty:
        raise HTTPException(status_code=404, detail=f"School ID '{school_id}' not found.")
        
    school_dict = df.iloc[0].to_dict()
    diagnosis = diagnose_school_risk(school_dict)
    
    return {
        "school": school_dict,
        "retention_risk_diagnosis": diagnosis
    }