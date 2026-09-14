"""AI Analyst Copilot Component answering the official questions."""

import streamlit as st
import plotly.express as px
from src.agent.agent import student_iq_analyst
from app.components.charts import apply_chart_theme, RISK_COLOR_MAP
from src.utils.helpers import clean_html

def render_agent_interface():
    info_box = clean_html("""
    <div style="background: rgba(124, 77, 255, 0.05); border: 1px solid rgba(124, 77, 255, 0.2); border-radius: 10px; padding: 1rem; margin-bottom: 1.2rem;">
        <h3 style="color: #F8FAFC; margin: 0 0 0.3rem 0; font-size: 1.15rem;">Ask StudentIQ Copilot</h3>
        <p style="color: #94A3B8; font-size: 0.82rem; margin: 0;">
            Natural-language analytics answering Mid-Day Meal, School Infrastructure, and Student Dropout correlations.
        </p>
    </div>
    """)
    st.markdown(info_box, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.78rem; font-weight: 600; color: #64748B;'>Official Competition Prompts:</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    p1 = c1.button("Electricity vs Test Scores", use_container_width=True)
    p2 = c2.button("Dropout Rate by District", use_container_width=True)
    p3 = c3.button("Attendance vs Meal Scheme", use_container_width=True)
    
    c4, c5, c6 = st.columns(3)
    p4 = c4.button("Attendance vs Test Scores", use_container_width=True)
    p5 = c5.button("High-Risk Schools", use_container_width=True)
    p6 = c6.button("Infrastructure Gaps", use_container_width=True)
    
    user_query = ""
    if p1:
        user_query = "Compare average test scores between schools with and without functional electricity."
    elif p2:
        user_query = "Show the dropout rate by district."
    elif p3:
        user_query = "Show attendance versus meal availability."
    elif p4:
        user_query = "Show the relationship between attendance and test scores."
    elif p5:
        user_query = "Which schools have the highest dropout risk?"
    elif p6:
        user_query = "Show infrastructure gaps by district."

    custom_input = st.text_input("Enter your analytical question:", value=user_query, placeholder="e.g. Which schools need intervention?")
    submit = st.button("Generate Insights & Chart", type="primary", use_container_width=True)
    
    if (submit or user_query) and custom_input.strip():
        with st.spinner("Analyzing question through AI Safety layer and DuckDB..."):
            res = student_iq_analyst.ask(custom_input)
            
            # Telemetry badges
            safe_pill = "<span style='background: rgba(0, 230, 118, 0.15); color: #00E676; padding: 3px 8px; border-radius: 8px; font-size: 0.75rem; font-weight: 600;'>SAFE SELECT</span>" if res.is_safe else "<span style='background: rgba(255, 23, 68, 0.15); color: #FF1744; padding: 3px 8px; border-radius: 8px; font-size: 0.75rem; font-weight: 600;'>BLOCKED</span>"
            engine_pill = f"<span style='background: rgba(124, 77, 255, 0.15); color: #7C4DFF; padding: 3px 8px; border-radius: 8px; font-size: 0.75rem; font-weight: 600;'>{res.engine_used}</span>"
            intent_pill = f"<span style='background: rgba(0, 229, 255, 0.15); color: #00E5FF; padding: 3px 8px; border-radius: 8px; font-size: 0.75rem; font-weight: 600;'>Intent: {res.intent}</span>"
            
            badge_html = clean_html(f"""
            <div style="display: flex; gap: 0.5rem; margin-top: 0.8rem; margin-bottom: 0.8rem;">
                {engine_pill} {safe_pill} {intent_pill}
            </div>
            """)
            st.markdown(badge_html, unsafe_allow_html=True)
            
            with st.expander("Inspect Generated DuckDB SQL Query", expanded=False):
                st.code(res.sql, language="sql")
                
            # Executive summary & actionable business insight
            st.info(f"**Data Summary:** {res.explanation}\n\n**Actionable Insight:** {res.business_insight}")
            
            if res.data is not None and not res.data.empty:
                df = res.data
                
                # Render correct chart
                if res.chart_type == "scatter" and "avg_student_attendance_pct" in df.columns and "avg_test_score" in df.columns:
                    fig = px.scatter(df, x="avg_student_attendance_pct", y="avg_test_score", color="retention_risk_level" if "retention_risk_level" in df.columns else None, color_discrete_map=RISK_COLOR_MAP)
                    st.plotly_chart(apply_chart_theme(fig, "Attendance vs Test Score"), use_container_width=True)
                elif res.chart_type == "horizontal_bar" and "school_name" in df.columns:
                    val_col = "reported_dropout_rate_pct" if "reported_dropout_rate_pct" in df.columns else df.columns[1]
                    fig = px.bar(df.sort_values(by=val_col, ascending=True), x=val_col, y="school_name", orientation="h", color=val_col, color_continuous_scale="Reds")
                    fig.update_layout(coloraxis_showscale=False)
                    st.plotly_chart(apply_chart_theme(fig, f"High-Risk Schools Ranking ({val_col})"), use_container_width=True)
                elif res.chart_type == "bar":
                    x_col = df.columns[0]
                    y_col = df.columns[1]
                    fig = px.bar(df, x=x_col, y=y_col, color=y_col)
                    st.plotly_chart(apply_chart_theme(fig, f"{x_col} vs {y_col}"), use_container_width=True)
                elif res.chart_type == "donut" and "retention_risk_level" in df.columns:
                    cnt_col = "school_count" if "school_count" in df.columns else df.columns[1]
                    fig = px.pie(df, names="retention_risk_level", values=cnt_col, hole=0.5)
                    st.plotly_chart(apply_chart_theme(fig, "Retention Risk Breakdown"), use_container_width=True)
                    
                st.dataframe(df, use_container_width=True, hide_index=True)