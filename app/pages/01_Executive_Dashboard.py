"""Page 1: Executive Dashboard - Macro Welfare & Retention Correlations."""

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from app.components.charts import (
    plot_electricity_impact,
    plot_district_dropout_risk,
    plot_meal_vs_attendance,
    plot_attendance_vs_dropout_scatter
)
from src.analytics.queries import (
    get_kpis,
    get_district_summary,
    get_electricity_impact_on_learning,
    get_mdm_impact_on_attendance,
    db_manager
)

st.set_page_config(page_title="Executive Dashboard | StudentIQ", page_icon="📊", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <h1 style="font-size: 2rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Executive Dashboard</h1>
    <p style="color: #94A3B8; font-size: 0.9rem;">State-level overview analyzing the nexus between infrastructure, Mid-Day Meals, and student retention.</p>
</div>
""", unsafe_allow_html=True)

kpis = get_kpis()
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Schools", f"{kpis.get('total_schools', 0):,}", f"{kpis.get('total_districts', 0)} districts monitored", accent_color="#00E5FF")
with c2:
    render_kpi_card("State Attendance Rate", f"{kpis.get('avg_attendance', 0.0):.1f}%", "Overall enrolled engagement", accent_color="#00E676")
with c3:
    render_kpi_card("Average Dropout Rate", f"{kpis.get('avg_dropout_rate', 0.0):.1f}%", "Annual reported student attrition", accent_color="#FF9100")
with c4:
    render_kpi_card("High-Risk Institutions", f"{kpis.get('at_risk_schools', 0)}", f"{kpis.get('critical_schools', 0)} Critical priority", delta="Remediation Queue", delta_color="negative", accent_color="#FF1744")

# Core Business Visualizations
col_l, col_r = st.columns(2)

with col_l:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;'>1. Electricity Impact on Learning & Dropout</div>", unsafe_allow_html=True)
    elec_df = get_electricity_impact_on_learning()
    if not elec_df.empty:
        st.plotly_chart(plot_electricity_impact(elec_df), use_container_width=True)

with col_r:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;'>2. Mid-Day Meal Scheme vs Attendance</div>", unsafe_allow_html=True)
    mdm_df = get_mdm_impact_on_attendance()
    if not mdm_df.empty:
        st.plotly_chart(plot_meal_vs_attendance(mdm_df), use_container_width=True)

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;'>3. District Dropout Rate Benchmarks</div>", unsafe_allow_html=True)
    dist_df = get_district_summary()
    if not dist_df.empty:
        st.plotly_chart(plot_district_dropout_risk(dist_df), use_container_width=True)

with col_s2:
    st.markdown("<div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;'>4. Attendance vs. Dropout Rate Correlation</div>", unsafe_allow_html=True)
    schools_df = db_manager.execute_query("SELECT school_id, school_name, district, avg_student_attendance_pct, reported_dropout_rate_pct, retention_risk_level FROM schools;")
    if not schools_df.empty:
        st.plotly_chart(plot_attendance_vs_dropout_scatter(schools_df), use_container_width=True)