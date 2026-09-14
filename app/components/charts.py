"""Plotly charts with dark enterprise analytics theme."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

ACCENT_CYAN = "#00E5FF"
ACCENT_PURPLE = "#7C4DFF"
ACCENT_GREEN = "#00E676"
ACCENT_AMBER = "#FFD600"
ACCENT_RED = "#FF1744"

RISK_COLOR_MAP = {
    "CRITICAL": "#FF1744",
    "HIGH": "#FF9100",
    "MEDIUM": "#FFD600",
    "LOW": "#00E676"
}

def apply_chart_theme(fig: go.Figure, title: str = "", height: int = 380) -> go.Figure:
    fig.update_layout(
        title={
            "text": title,
            "font": {"size": 14, "color": "#F8FAFC", "family": "Inter, sans-serif"},
            "x": 0.02,
            "y": 0.95
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#94A3B8", "family": "Inter, sans-serif"},
        height=height,
        margin={"l": 40, "r": 25, "t": 45, "b": 40},
        legend={"orientation": "h", "y": -0.2, "font": {"size": 11}},
        xaxis={"gridcolor": "rgba(255, 255, 255, 0.06)", "zerolinecolor": "rgba(255, 255, 255, 0.1)"},
        yaxis={"gridcolor": "rgba(255, 255, 255, 0.06)", "zerolinecolor": "rgba(255, 255, 255, 0.1)"},
    )
    return fig

def plot_electricity_impact(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["status"],
        y=df["avg_test_score"],
        name="Average Test Score",
        marker_color=ACCENT_CYAN,
        yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=df["status"],
        y=df["avg_dropout_rate"],
        name="Dropout Rate %",
        marker_color=ACCENT_RED,
        mode="lines+markers",
        yaxis="y2"
    ))
    fig.update_layout(
        yaxis={"title": "Test Score (Scale 0-100)", "side": "left", "range": [0, 100]},
        yaxis2={"title": "Dropout Rate %", "side": "right", "overlaying": "y", "range": [0, 30]},
    )
    return apply_chart_theme(fig, "Electricity Impact on Academic Learning & Dropout")

def plot_district_dropout_risk(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df.sort_values(by="avg_dropout_rate", ascending=True),
        x="avg_dropout_rate",
        y="district",
        orientation="h",
        color="avg_dropout_rate",
        color_continuous_scale="Reds",
        labels={"avg_dropout_rate": "Avg Dropout Rate %", "district": "District"}
    )
    fig.update_layout(coloraxis_showscale=False)
    return apply_chart_theme(fig, "District-wise Average Student Dropout Rate")

def plot_meal_vs_attendance(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df,
        x="mdm_status",
        y="avg_attendance",
        text="avg_attendance",
        color="mdm_status",
        color_discrete_sequence=[ACCENT_GREEN, ACCENT_AMBER],
        labels={"avg_attendance": "Attendance %", "mdm_status": "Mid-Day Meal Status"}
    )
    fig.update_traces(textposition="outside")
    return apply_chart_theme(fig, "Mid-Day Meal Provisioning vs Student Attendance")

def plot_attendance_vs_dropout_scatter(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="avg_student_attendance_pct",
        y="reported_dropout_rate_pct",
        color="retention_risk_level",
        color_discrete_map=RISK_COLOR_MAP,
        hover_data=["school_id", "school_name", "district"],
        labels={"avg_student_attendance_pct": "Student Attendance %", "reported_dropout_rate_pct": "Reported Dropout %"}
    )
    return apply_chart_theme(fig, "Attendance vs. Dropout Rate Correlation Matrix")

def plot_risk_donut(df: pd.DataFrame) -> go.Figure:
    colors = [RISK_COLOR_MAP.get(str(r).upper(), "#94A3B8") for r in df["retention_risk_level"]]
    fig = go.Figure(data=[go.Pie(
        labels=df["retention_risk_level"],
        values=df["school_count"],
        hole=0.55,
        marker={"colors": colors, "line": {"color": "#0B0F19", "width": 2}},
        textinfo="label+percent"
    )])
    return apply_chart_theme(fig, "State Retention Risk Tier Breakdown")