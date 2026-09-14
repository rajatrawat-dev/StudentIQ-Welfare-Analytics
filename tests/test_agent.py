"""Tests for AI Analyst, Intent Detection, AI Safety, and Chart Selection."""

import pytest
from src.agent.query_validator import validate_query
from src.agent.intent import detect_intent
from src.agent.chart_selector import recommend_chart
from src.agent.agent import student_iq_analyst
import pandas as pd

def test_ai_safety_blocks_drop():
    sql = "DROP TABLE schools;"
    ok, msg = validate_query(sql)
    assert ok is False
    assert "DROP" in msg

def test_ai_safety_blocks_delete():
    sql = "DELETE FROM schools WHERE total_enrolled < 100;"
    ok, msg = validate_query(sql)
    assert ok is False
    assert "DELETE" in msg

def test_ai_safety_blocks_multistatement():
    sql = "SELECT * FROM schools; DROP TABLE schools;"
    ok, msg = validate_query(sql)
    assert ok is False
    assert "Multi-statement" in msg

def test_ai_safety_allows_select():
    sql = "SELECT district, AVG(reported_dropout_rate_pct) FROM schools GROUP BY district;"
    ok, _ = validate_query(sql)
    assert ok is True

def test_intent_detection():
    # Official prompt 1
    intent, _ = detect_intent("Compare average test scores between schools with and without functional electricity.")
    assert intent == "ELECTRICITY_COMPARISON"

    # Official prompt 2
    intent, _ = detect_intent("Show the dropout rate by district.")
    assert intent == "DROPOUT_BY_DISTRICT"

    # Official prompt 3
    intent, _ = detect_intent("Show attendance versus meal availability.")
    assert intent == "ATTENDANCE_VS_MEAL"

def test_chart_selection():
    df = pd.DataFrame({"district": ["Dist A", "Dist B"], "avg_dropout_rate": [12.5, 8.2]})
    chart = recommend_chart("DROPOUT_BY_DISTRICT", df)
    assert chart == "bar"

def test_agent_end_to_end():
    res = student_iq_analyst.ask("Compare average test scores between schools with and without functional electricity.")
    assert res.is_safe is True
    assert res.execution_success is True
    assert res.chart_type == "bar"
    assert len(res.business_insight) > 10