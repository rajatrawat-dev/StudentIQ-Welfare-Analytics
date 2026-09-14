"""Dynamic data-driven executive findings synthesized from DuckDB ground truth."""

from typing import List, Dict
import pandas as pd
from src.analytics.queries import get_kpis, get_district_summary, get_electricity_impact_on_learning, get_mdm_impact_on_attendance

def generate_welfare_insights() -> List[Dict[str, str]]:
    insights = []
    
    kpis = get_kpis()
    if not kpis or kpis.get("total_schools", 0) == 0:
        return [{"type": "INFO", "title": "Awaiting Data", "text": "Execute pipeline to view executive insights."}]

    # 1. Electricity vs Academic Performance Insight
    elec_df = get_electricity_impact_on_learning()
    if len(elec_df) >= 2:
        with_elec = elec_df[elec_df["status"] == "Functional Electricity"]
        no_elec = elec_df[elec_df["status"] == "No Electricity"]
        if not with_elec.empty and not no_elec.empty:
            score_diff = round(float(with_elec.iloc[0]["avg_test_score"]) - float(no_elec.iloc[0]["avg_test_score"]), 1)
            drop_diff = round(float(no_elec.iloc[0]["avg_dropout_rate"]) - float(with_elec.iloc[0]["avg_dropout_rate"]), 1)
            insights.append({
                "type": "SUCCESS" if score_diff > 0 else "INFO",
                "title": "Electrification & Learning Dividends",
                "text": f"Schools equipped with functional electricity average a test score of {with_elec.iloc[0]['avg_test_score']} (+{score_diff} pts higher than unelectrified schools) with a {drop_diff}% lower dropout rate."
            })

    # 2. Mid-Day Meal & Attendance Retention Insight
    mdm_df = get_mdm_impact_on_attendance()
    if len(mdm_df) >= 2:
        active_mdm = mdm_df[mdm_df["mdm_status"] == "Mid-Day Meal Active"]
        disrupted_mdm = mdm_df[mdm_df["mdm_status"] == "Mid-Day Meal Disrupted"]
        if not active_mdm.empty and not disrupted_mdm.empty:
            att_boost = round(float(active_mdm.iloc[0]["avg_attendance"]) - float(disrupted_mdm.iloc[0]["avg_attendance"]), 1)
            insights.append({
                "type": "SUCCESS",
                "title": "Mid-Day Meal Welfare Impact",
                "text": f"Active Mid-Day Meal schemes demonstrate a +{att_boost}% attendance premium ({active_mdm.iloc[0]['avg_attendance']}% vs {disrupted_mdm.iloc[0]['avg_attendance']}% in disrupted schools), acting as a vital retention anchor."
            })

    # 3. High Risk District Vulnerability
    dist_df = get_district_summary()
    if not dist_df.empty:
        top_vuln = dist_df.iloc[0]
        insights.append({
            "type": "WARNING",
            "title": "District Intervention Priority",
            "text": f"{top_vuln['district']} district registers the state's highest average dropout risk ({top_vuln['avg_dropout_rate']}%), with {top_vuln['at_risk_schools']} institutions prioritized for immediate infrastructural remediation."
        })

    # 4. Critical Alert
    crit_schools = kpis.get("critical_schools", 0)
    if crit_schools > 0:
        insights.append({
            "type": "CRITICAL",
            "title": "Immediate Welfare Taskforce Required",
            "text": f"{crit_schools} educational institutions meet Critical Risk thresholds (compound deficit of basic sanitation, electricity, and elevated dropout)."
        })

    return insights