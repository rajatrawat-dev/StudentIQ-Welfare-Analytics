"""Page 5: Ask StudentIQ - Controlled Natural Language AI Analyst Copilot."""

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.sidebar import render_sidebar
from app.components.agent_chat import render_agent_interface

st.set_page_config(page_title="AI Analyst | StudentIQ", page_icon="🤖", layout="wide")
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <h1 style="font-size: 2rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">AI Analyst — Ask StudentIQ</h1>
    <p style="color: #94A3B8; font-size: 0.9rem;">Controlled AI copilot translating natural language questions into safe DuckDB SQL queries, visualizations, and insights.</p>
</div>
""", unsafe_allow_html=True)

render_agent_interface()