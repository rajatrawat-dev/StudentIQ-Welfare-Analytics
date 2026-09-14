"""Futuristic glassmorphic KPI cards.
Guaranteed to render cleanly without raw HTML tags spilling into UI!
"""

import streamlit as st
from typing import Optional
from src.utils.helpers import clean_html

def render_kpi_card(
    title: str,
    value: str,
    subtitle: str = "",
    delta: Optional[str] = None,
    delta_color: str = "normal",
    accent_color: str = "#00E5FF"
):
    delta_html = ""
    if delta:
        d_color = "#00E676" if delta_color == "positive" else "#FF1744" if delta_color == "negative" else "#94A3B8"
        delta_html = f"<div style='font-size: 0.75rem; font-weight: 600; color: {d_color}; margin-top: 0.3rem;'>{delta}</div>"
        
    raw_html = f"""
    <div style="background: linear-gradient(145deg, rgba(18, 24, 38, 0.85) 0%, rgba(13, 17, 27, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-top: 2px solid {accent_color}; border-radius: 12px; padding: 1.1rem 1rem; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3); backdrop-filter: blur(12px); margin-bottom: 0.8rem;">
        <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94A3B8;">{title}</div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #F8FAFC; margin-top: 0.3rem; letter-spacing: -0.02em;">{value}</div>
        {delta_html}
        <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.2rem;">{subtitle}</div>
    </div>
    """
    st.markdown(clean_html(raw_html), unsafe_allow_html=True)