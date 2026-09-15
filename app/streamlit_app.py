"""StudentIQ - Student Retention & Welfare Intelligence
Official Track: Education & EdTech — Student Retention & Welfare Efficacy Tracker
TransOrg AgentIQ Datathon
"""

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.kpi_cards import render_kpi_card
from src.analytics.queries import get_kpis
from src.analytics.insights import generate_welfare_insights
from src.data.quality_report import QualityReport
from src.utils.helpers import clean_html

st.set_page_config(
    page_title="StudentIQ | Welfare & Retention Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Dark Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0A0E17; color: #F8FAFC; }
    .glass-card {
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

render_sidebar()

# Hero Banner
hero_html = clean_html("""
<div style="background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(124, 77, 255, 0.08) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <div style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #00E5FF 0%, #7C4DFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                StudentIQ
            </div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #00E5FF; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">
                Student Retention & Welfare Efficacy Tracker
            </div>
            <div style="font-size: 0.95rem; color: #94A3B8; max-width: 850px; line-height: 1.6;">
                State Education Department intelligence tracking the correlation between <b>Mid-Day Meal schemes</b>, <b>school infrastructure</b>, and <b>student retention / dropout risks</b>.
            </div>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(0, 229, 255, 0.12); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3); padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
             AGENTIQ TRACK
            </span>
        </div>
    </div>
</div>
""")
st.markdown(hero_html, unsafe_allow_html=True)

kpis = get_kpis()
q_report = QualityReport.load()

# Operational KPI Radar
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Schools", f"{kpis.get('total_schools', 0):,}", f"Cohort: {kpis.get('total_students', 0):,} students", accent_color="#00E5FF")
with c2:
    render_kpi_card("Meal Scheme Coverage", f"{kpis.get('mdm_coverage_pct', 0.0):.1f}%", "Active Mid-Day Meal distribution", accent_color="#00E676")
with c3:
    render_kpi_card("Functional Electricity", f"{kpis.get('electricity_pct', 0.0):.1f}%", f"Safe Water: {kpis.get('water_pct', 0.0):.1f}%", accent_color="#7C4DFF")
with c4:
    render_kpi_card("High-Risk Schools", f"{kpis.get('at_risk_schools', 0)}", f"{kpis.get('critical_schools', 0)} Critical priority", delta="Urgent Intervention", delta_color="negative", accent_color="#FF1744")

# Data Rescue Story Banner
if q_report:
    rescue_html = clean_html(f"""
    <div style="background: linear-gradient(90deg, rgba(0, 230, 118, 0.08) 0%, rgba(0, 229, 255, 0.05) 100%); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 12px; padding: 1.1rem 1.4rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 0.78rem; font-weight: 700; color: #00E676; text-transform: uppercase;">Layer 1: Data Rescue Provenance</span>
                <h4 style="color: #F8FAFC; margin: 0.2rem 0 0.3rem 0;">From Messy Welfare Logs to Ground Truth</h4>
                <p style="color: #94A3B8; font-size: 0.82rem; margin: 0;">
                    Repaired <b>{q_report.get('boolean_values_standardized', 0)}</b> boolean entries (Yes/Hai/Nahi/0/1), 
                    converted <b>{q_report.get('unit_conversions_performed', 0)}</b> grain logs (Quintals/Qtl/Tons &rarr; KG), 
                    flagged <b>{q_report.get('proxy_attendance_flagged', 0)}</b> proxy anomalies, 
                    removed <b>{q_report.get('duplicates_removed', 0)}</b> duplicates.
                </p>
            </div>
            <div style="text-align: right; min-width: 130px;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #00E676;">{q_report.get('data_quality_score', 0)}<span style="font-size: 0.9rem; color: #94A3B8;">/100</span></div>
                <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Quality Score</div>
            </div>
        </div>
    </div>
    """)
    st.markdown(rescue_html, unsafe_allow_html=True)

# Dynamic Findings
insights = generate_welfare_insights()
st.subheader("Executive Findings & Correlations")
cols = st.columns(len(insights) if insights else 1)
colors = {"SUCCESS": "#00E676", "WARNING": "#FF9100", "CRITICAL": "#FF1744", "INFO": "#00E5FF"}

for idx, ins in enumerate(insights):
    col_color = colors.get(ins.get("type", "INFO"), "#00E5FF")
    with cols[idx]:
        ins_html = clean_html(f"""
        <div style="background: rgba(18, 24, 38, 0.7); border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid {col_color}; border-radius: 10px; padding: 1rem; height: 100%;">
            <div style="font-size: 0.72rem; font-weight: 700; color: {col_color}; text-transform: uppercase;">{ins.get('title')}</div>
            <div style="font-size: 0.82rem; color: #E2E8F0; margin-top: 0.4rem; line-height: 1.45;">{ins.get('text')}</div>
        </div>
        """)
        st.markdown(ins_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("Navigate through the 5 intelligence pages using the sidebar on the left.")