"""AI Analyst endpoint translating natural language questions into safe SQL and insights."""

from typing import Optional, Dict, Any, List
from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.agent.agent import student_iq_analyst

router = APIRouter(prefix="/agent", tags=["AI Analyst"])

class QueryRequest(BaseModel):
    question: str = Field(..., example="Compare average test scores between schools with and without functional electricity.")

class QueryResponse(BaseModel):
    question: str
    intent: str
    sql: str
    is_safe: bool
    safety_message: str
    execution_success: bool
    data: Optional[List[Dict[str, Any]]] = None
    chart_type: str
    explanation: str
    business_insight: str
    engine_used: str

@router.post("/query", response_model=QueryResponse)
def ask_analyst(payload: QueryRequest):
    res = student_iq_analyst.ask(payload.question)
    data_records = res.data.to_dict(orient="records") if res.data is not None else None
    
    return QueryResponse(
        question=res.question,
        intent=res.intent,
        sql=res.sql,
        is_safe=res.is_safe,
        safety_message=res.safety_message,
        execution_success=res.execution_success,
        data=data_records,
        chart_type=res.chart_type,
        explanation=res.explanation,
        business_insight=res.business_insight,
        engine_used=res.engine_used
    )