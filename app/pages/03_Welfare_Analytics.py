"""Page 3: Welfare Analytics - Deep Dive into Meals & Infrastructure."""

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.tables import render_styled_dataframe
from src.analytics.queries import filter_schools, db_manager

st.set_page_config(page_title="Welfare Analytics | StudentIQ", page_icon="🍲", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <h1 style="font-size: 2rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">Welfare & Infrastructure Analytics</h1>
    <p style="color: #94A3B8; font-size: 0.9rem;">Multi-criteria filtering across Mid-Day Meal provisioning, water, electricity, and sanitation.</p>
</div>
""", unsafe_allow_html=True)

# Filters
with st.expander("Filter Controls", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        districts = ["All"] + sorted(db_manager.execute_query("SELECT DISTINCT district FROM schools;")["district"].tolist())
        sel_dist = st.selectbox("District", districts)
        search_txt = st.text_input("Search School Name or Code", placeholder="e.g. Model Primary or SCH-1005")
    with f2:
        risks = ["All", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        sel_risk = st.selectbox("Retention Risk Tier", risks)
        ch_elec = st.checkbox("Only Electrified Schools")
        ch_water = st.checkbox("Only Potable Water Available")
    with f3:
        ch_girls_toilet = st.checkbox("Only Separate Girls Toilet Available")
        ch_mdm = st.checkbox("Only Active Mid-Day Meal")

filtered_df = filter_schools(
    district=sel_dist if sel_dist != "All" else None,
    risk_level=sel_risk if sel_risk != "All" else None,
    electricity_only=ch_elec,
    water_only=ch_water,
    girls_toilet_only=ch_girls_toilet,
    mdm_active_only=ch_mdm,
    search_term=search_txt if search_txt.strip() else None,
    limit=500
)

st.markdown(f"**Showing {len(filtered_df)} educational institutions** matching selected filters.")
render_styled_dataframe(filtered_df, height=450)

# CSV Download
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Welfare Cohort (CSV)",
    data=csv_data,
    file_name="studentiq_welfare_cohort.csv",
    mime="text/csv",
    type="primary"
)