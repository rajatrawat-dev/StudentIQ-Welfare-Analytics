"""Sidebar with system status telemetry and official hackathon context."""

import streamlit as st
import requests
from src.config.settings import settings
from src.analytics.database import db_manager
from src.utils.helpers import clean_html

def render_sidebar():
    with st.sidebar:
        html_header = clean_html("""
        <div style="text-align: center; padding: 1rem 0.5rem; margin-bottom: 1.2rem; border-bottom: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #00E5FF 0%, #7C4DFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                STUDENTIQ
            </div>
            <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94A3B8; margin-top: 0.2rem;">
                Welfare & Retention Intelligence
            </div>
        </div>
        """)
        st.markdown(html_header, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 0.4rem;'>System Telemetry</p>", unsafe_allow_html=True)
        
        # DuckDB Engine Status
        try:
            db_manager.execute_query("SELECT 1;")
            duck_html = clean_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0.6rem; background: rgba(0, 229, 255, 0.05); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 6px; margin-bottom: 0.35rem;">
                <span style="font-size: 0.78rem; color: #CBD5E1;">DuckDB Engine</span>
                <span style="font-size: 0.7rem; background: rgba(0, 229, 255, 0.2); color: #00E5FF; padding: 2px 6px; border-radius: 10px; font-weight: 600;">ACTIVE</span>
            </div>
            """)
        except Exception:
            duck_html = clean_html("""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0.6rem; background: rgba(255, 23, 68, 0.05); border: 1px solid rgba(255, 23, 68, 0.2); border-radius: 6px; margin-bottom: 0.35rem;">
                <span style="font-size: 0.78rem; color: #CBD5E1;">DuckDB Engine</span>
                <span style="font-size: 0.7rem; background: rgba(255, 23, 68, 0.2); color: #FF1744; padding: 2px 6px; border-radius: 10px; font-weight: 600;">OFFLINE</span>
            </div>
            """)
        st.markdown(duck_html, unsafe_allow_html=True)
        
        # ML Model Status
        model_ready = settings.MODEL_PATH.exists()
        m_color = "#00E676" if model_ready else "#FFD600"
        m_text = "READY" if model_ready else "RULE FALLBACK"
        ml_html = clean_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0.6rem; background: rgba(0, 230, 118, 0.05); border: 1px solid rgba(0, 230, 118, 0.2); border-radius: 6px; margin-bottom: 0.35rem;">
            <span style="font-size: 0.78rem; color: #CBD5E1;">Dropout Risk ML</span>
            <span style="font-size: 0.7rem; background: {m_color}22; color: {m_color}; padding: 2px 6px; border-radius: 10px; font-weight: 600;">{m_text}</span>
        </div>
        """)
        st.markdown(ml_html, unsafe_allow_html=True)
        
        # Ollama Status
        ollama_on = False
        try:
            r = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=1)
            if r.status_code == 200:
                ollama_on = True
        except Exception:
            pass
            
        o_color = "#7C4DFF" if ollama_on else "#94A3B8"
        o_text = "OLLAMA ACTIVE" if ollama_on else "RULE FALLBACK"
        ollama_html = clean_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0.6rem; background: rgba(124, 77, 255, 0.05); border: 1px solid rgba(124, 77, 255, 0.2); border-radius: 6px; margin-bottom: 1.2rem;">
            <span style="font-size: 0.78rem; color: #CBD5E1;">AI Copilot</span>
            <span style="font-size: 0.7rem; background: {o_color}22; color: {o_color}; padding: 2px 6px; border-radius: 10px; font-weight: 600;">{o_text}</span>
        </div>
        """)
        st.markdown(ollama_html, unsafe_allow_html=True)
        
        st.markdown("---")
        track_info = clean_html("""
        <div style="font-size: 0.75rem; color: #64748B; line-height: 1.5;">
            <b>Track:</b> Education & EdTech<br>
            <b>Datathon:</b> TransOrg AgentIQ<br>
            <b>Story:</b> Meal + Inf + Attendance &rarr; Retention
        </div>
        """)
        st.markdown(track_info, unsafe_allow_html=True)