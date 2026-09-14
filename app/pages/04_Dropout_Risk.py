"""Page 4: Dropout Risk & Early Warning System."""

import streamlit as st
import sys
from pathlib import Path
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from app.components.charts import plot_risk_donut, apply_chart_theme
from app.components.tables import render_styled_dataframe
from src.analytics.queries import get_risk_distribution, get_high_risk_schools, db_manager
from src.ml.predict import diagnose_school_risk

st.set_page_config(page_title="Dropout Risk | StudentIQ", page_icon="⚠️", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <h1 style="font-size: 2rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Student Retention & Dropout Risk Analysis</h1>
    <p style="color: #94A3B8; font-size: 0.9rem;">Predictive early-warning indicators identifying institutions facing acute student attrition.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: rgba(0, 229, 255, 0.05); border-left: 4px solid #00E5FF; padding: 0.75rem 1.1rem; border-radius: 4px; margin-bottom: 1.2rem; font-size: 0.82rem; color: #CBD5E1;">
    <b>Institutional Analytics Notice:</b> Risk classifications are calculated from empirical academic indicators (attendance consistency, sanitation facilities, Mid-Day Meal active days). This is an <b>Analytical Early-Warning Indicator</b>, strictly for administrative resource allocation.
</div>
""", unsafe_allow_html=True)

# Risk Distribution
r_df = get_risk_distribution()
col_d1, col_d2 = st.columns([4, 6])
with col_d1:
    if not r_df.empty:
        st.plotly_chart(plot_risk_donut(r_df), use_container_width=True)

with col_d2:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;'>Welfare Efficacy Index Distribution</div>", unsafe_allow_html=True)
    idx_df = db_manager.execute_query("SELECT welfare_efficacy_index, retention_risk_level FROM schools;")
    fig = px.histogram(idx_df, x="welfare_efficacy_index", color="retention_risk_level", nbins=25)
    st.plotly_chart(apply_chart_theme(fig, "Welfare Efficacy Index Spread (0-100)"), use_container_width=True)

# High Risk Priority Queue
st.subheader("High-Risk Schools Priority Intervention Queue")
high_risk_df = get_high_risk_schools(25)
render_styled_dataframe(high_risk_df, height=350)

# Individual Diagnostic Inspector
st.subheader("Individual School Risk Factor Diagnostic Inspector")
selected_id = st.selectbox(
    "Select School for Diagnostic Breakdown:",
    options=high_risk_df["school_id"].tolist(),
    format_func=lambda x: f"{x} - {high_risk_df.loc[high_risk_df['school_id'] == x, 'school_name'].values[0]} ({high_risk_df.loc[high_risk_df['school_id'] == x, 'district'].values[0]})"
)

if selected_id:
    row = high_risk_df[high_risk_df["school_id"] == selected_id].iloc[0].to_dict()
    diag = diagnose_school_risk(row)
    
    cd1, cd2 = st.columns([1, 2])
    with cd1:
        st.markdown(f"""
        <div style="background: rgba(18, 24, 38, 0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 1.1rem;">
            <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">{row['school_name']}</div>
            <div style="font-size: 0.8rem; color: #00E5FF; margin-bottom: 0.6rem;">{row['school_id']} | {row['district']}</div>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 0.4rem 0;">
            <div style="font-size: 0.8rem; color: #94A3B8;"><b>Reported Dropout Rate:</b> {row['reported_dropout_rate_pct']}%</div>
            <div style="font-size: 0.8rem; color: #94A3B8;"><b>Student Attendance:</b> {row['avg_student_attendance_pct']}%</div>
            <div style="font-size: 0.8rem; color: #94A3B8;"><b>Welfare Index:</b> {row['welfare_efficacy_index']}/100</div>
            <div style="font-size: 0.8rem; color: #FF1744; margin-top: 0.4rem;"><b>Priority Action:</b> {row['priority_action']}</div>
        </div>
        """, unsafe_allow_html=True)
    with cd2:
        st.markdown("<div style='font-size: 0.9rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;'>Underlying Risk Drivers:</div>", unsafe_allow_html=True)
        for factor in diag["key_risk_factors"]:
            st.markdown(f"""
            <div style="background: rgba(255, 23, 68, 0.08); border: 1px solid rgba(255, 23, 68, 0.2); border-left: 4px solid #FF1744; border-radius: 6px; padding: 0.5rem 0.8rem; margin-bottom: 0.35rem; font-size: 0.82rem; color: #F1F5F9;">
                {factor}
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"Diagnostic Model: {diag['model_type']}")