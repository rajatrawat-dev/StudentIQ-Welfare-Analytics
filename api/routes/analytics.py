"""Analytical endpoints for State Education Department decision support."""

from typing import Dict, Any, List
from fastapi import APIRouter
from src.analytics.queries import get_kpis, get_district_summary, get_risk_distribution
from src.analytics.insights import generate_welfare_insights

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_state_summary() -> Dict[str, Any]:
    kpis = get_kpis()
    insights = generate_welfare_insights()
    return {
        "kpis": kpis,
        "executive_insights": insights
    }

@router.get("/districts")
def get_districts() -> List[Dict[str, Any]]:
    df = get_district_summary()
    return df.to_dict(orient="records")

@router.get("/risk")
def get_risk_summary() -> List[Dict[str, Any]]:
    df = get_risk_distribution()
    return df.to_dict(orient="records")