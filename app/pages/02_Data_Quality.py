"""Page 2: Data Quality & Data Rescue Provenance."""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from app.components.charts import apply_chart_theme
from src.data.quality_report import QualityReport
from src.data.loader import load_raw_data, load_cleaned_data

st.set_page_config(page_title="Data Quality | StudentIQ", page_icon="🛡️", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <h1 style="font-size: 2rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Data Quality & Data Rescue</h1>
    <p style="color: #94A3B8; font-size: 0.9rem;">Verifiable audit trail detailing how messy enterprise logs were transformed into canonical ground truth.</p>
</div>
""", unsafe_allow_html=True)

report = QualityReport.load()
if not report:
    st.warning("No quality report available. Execute pipeline first: `python scripts/run_pipeline.py`")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Data Quality Score", f"{report.get('data_quality_score', 0):.1f}/100", "Composite integrity rating", accent_color="#00E676")
with c2:
    render_kpi_card("Booleans Standardized", f"{report.get('boolean_values_standardized', 0):,}", "Yes/Hai/Nahi/0/1 mapped", accent_color="#00E5FF")
with c3:
    render_kpi_card("Unit Conversions", f"{report.get('unit_conversions_performed', 0):,}", "Quintal/Qtl/Ton converted to KG", accent_color="#7C4DFF")
with c4:
    render_kpi_card("Proxy Anomalies Flagged", f"{report.get('proxy_attendance_flagged', 0)}", "Suspicious attendance detected", accent_color="#FF1744")

# Funnel Chart
st.subheader("Data Rescue Volume Transformation")
funnel_df = pd.DataFrame([
    {"Stage": "Raw Input Records", "Count": report.get("rows_before", 0)},
    {"Stage": "Cleaned Ground Truth", "Count": report.get("rows_after", 0)}
])
fig = px.bar(funnel_df, x="Stage", y="Count", text="Count", color="Stage", color_discrete_sequence=["#FF1744", "#00E676"])
fig.update_traces(textposition="outside")
st.plotly_chart(apply_chart_theme(fig, "Record Volume: Raw vs Cleaned"), use_container_width=True)

# 14-Step Audit Log
st.subheader("14-Step Cleansing & Standardization Audit Log")
audit_steps = [
    {"Step #": "Step 1 & 2", "Action": "Dataset Profiling & Intelligent Column Mapping", "Details": "Fuzzy-mapped raw headers (e.g. 'School Code', 'Mid Day Meal Served') to canonical schema", "Metric": f"{report.get('rows_before', 0)} rows inspected"},
    {"Step #": "Step 3 & 4", "Action": "Exact Deduplication & Entity Key Resolution", "Details": "Dropped exact row copies and resolved ID collisions to SCH-XXXX", "Metric": f"{report.get('duplicates_removed', 0)} duplicates removed"},
    {"Step #": "Step 5", "Action": "Boolean Infrastructure Normalization", "Details": "Standardized 'Yes', 'Y', '1', 'Hai', 'Nahi', '0' into True/False booleans", "Metric": f"{report.get('boolean_values_standardized', 0)} values mapped"},
    {"Step #": "Step 6", "Action": "Grain Procurement Unit Conversion", "Details": "Converted Quintals (x100) and Tons (x1000) to standard KG while saving raw units", "Metric": f"{report.get('unit_conversions_performed', 0)} quantities converted"},
    {"Step #": "Step 7", "Action": "Attendance Normalization & Bounds Enforcement", "Details": "Parsed percentage strings, ratios, and clamped to 0-100% scale", "Metric": f"{report.get('attendance_anomalies_repaired', 0)} repaired"},
    {"Step #": "Step 8 & 9", "Action": "Test Score & Dropout Rate Range Checks", "Details": "Enforced strict 0-100% valid bounds for exam marks and dropout rates", "Metric": "Bounds verified"},
    {"Step #": "Step 10", "Action": "District Median Imputation", "Details": "Imputed missing attendance, test scores, and procurement using district medians", "Metric": f"{report.get('missing_values_imputed', 0)} missing values imputed"},
    {"Step #": "Step 11", "Action": "Proxy Attendance Anomaly Detection", "Details": "Flagged artificial 100% attendance during meal disruptions or failing marks", "Metric": f"{report.get('proxy_attendance_flagged', 0)} anomalies flagged"},
    {"Step #": "Step 12 & 13", "Action": "Composite Indices & Retention Risk Scoring", "Details": "Computed Infrastructure Score (0-100) and Welfare Efficacy Index", "Metric": f"{report.get('rows_after', 0)} records scored"},
    {"Step #": "Step 14", "Action": "Data Quality Scoring & Audit Logging", "Details": "Generated machine-readable audit report with data quality rating", "Metric": f"Score: {report.get('data_quality_score', 0)}/100"},
]
st.dataframe(pd.DataFrame(audit_steps), use_container_width=True, hide_index=True)