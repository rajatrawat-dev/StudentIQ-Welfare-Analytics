"""Data Rescue Engine orchestrating the 14-Step Cleansing and Standardization Pipeline.
Transforms messy school infrastructure, Mid-Day Meal, and attendance logs into validated ground truth.
"""

from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from src.config.settings import settings
from src.config.schema_map import resolve_column_mapping
from src.data.normalizer import (
    normalize_boolean,
    normalize_grain_procurement,
    normalize_attendance,
    normalize_text
)
from src.data.validator import detect_proxy_attendance, calculate_data_quality_score
from src.data.quality_report import QualityReport
from src.utils.logging import get_logger

logger = get_logger("DataRescueCleaner")

class WelfareDataCleaner:
    def __init__(self):
        self.report = QualityReport()

    def clean(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        logger.info("Starting Data Rescue pipeline...")
        self.report.rows_before = len(df_raw)
        
        df = df_raw.copy()
        
        # 1. Resolve raw column names to canonical attributes
        df = self._map_columns(df)
        
        # 2. Drop exact duplicate rows
        initial_len = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        exact_dups = initial_len - len(df)
        self.report.duplicates_removed += exact_dups
        if exact_dups > 0:
            self.report.log_action("Deduplication", f"Removed {exact_dups} exact duplicate rows", exact_dups)
            
        # 3. Standardize IDs & resolve ID collisions
        df = self._clean_ids(df)
        
        # 4. Standardize text attributes (School names, Districts, Blocks)
        df = self._clean_text(df)
        
        # 5. Standardize infrastructure booleans (Electricity, Water, Toilets, MDM)
        df = self._clean_booleans(df)
        
        # 6. Normalize grain procurement quantities & units (KG, Quintal -> KG)
        df = self._clean_grain_procurement(df)
        
        # 7. Normalize attendance & detect anomalies
        df = self._clean_attendance(df)
        
        # 8. Clean academic outcomes (Test scores & Dropout rates)
        df = self._clean_outcomes(df)
        
        # 9. Intelligent missing value imputation (District-level medians)
        df = self._impute_missing(df)
        
        # 10. Flag proxy attendance records
        df["proxy_attendance_flag"] = detect_proxy_attendance(df)
        anomalies_count = int(df["proxy_attendance_flag"].sum())
        self.report.proxy_attendance_flagged = anomalies_count
        if anomalies_count > 0:
            self.report.log_action("ProxyAnomaly", f"Flagged {anomalies_count} proxy attendance records", anomalies_count)
            
        # 11. Compute derived composite indices
        df = self._compute_indices(df)
        
        # 12. Finalize Quality Report
        self.report.rows_after = len(df)
        self.report.data_quality_score = calculate_data_quality_score(self.report.to_dict())
        
        logger.info(f"Data rescue complete. Rows: {self.report.rows_before} -> {self.report.rows_after}. Score: {self.report.data_quality_score}")
        return df, self.report.to_dict()

    def _map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = resolve_column_mapping(list(df.columns))
        rename_dict = {}
        for canonical, raw_col in mapping.items():
            if raw_col and raw_col in df.columns:
                rename_dict[raw_col] = canonical
        df = df.rename(columns=rename_dict)
        return df

    def _clean_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        if "school_id" not in df.columns:
            df["school_id"] = [f"SCH-{1000 + i}" for i in range(len(df))]
        else:
            # Clean formatting
            df["school_id"] = df["school_id"].astype(str).str.strip().str.upper()
            before_dedup = len(df)
            df = df.drop_duplicates(subset=["school_id"], keep="first").reset_index(drop=True)
            dropped = before_dedup - len(df)
            self.report.duplicates_removed += dropped
        return df

    def _clean_text(self, df: pd.DataFrame) -> pd.DataFrame:
        for text_col in ["school_name", "district", "block"]:
            if text_col not in df.columns:
                df[text_col] = "State Central District" if text_col == "district" else "General Block" if text_col == "block" else "State Model School"
            else:
                cleaned = []
                for val in df[text_col]:
                    cval, _ = normalize_text(val)
                    cleaned.append(cval)
                df[text_col] = cleaned
        return df

    def _clean_booleans(self, df: pd.DataFrame) -> pd.DataFrame:
        bool_cols = ["has_electricity", "has_drinking_water", "has_separate_girls_toilet", "has_boys_toilet", "mdm_served_status"]
        bool_mod_count = 0
        for col in bool_cols:
            if col not in df.columns:
                df[col] = True
            else:
                norm_vals = []
                for val in df[col]:
                    bval, mod = normalize_boolean(val)
                    norm_vals.append(bval)
                    if mod:
                        bool_mod_count += 1
                df[col] = norm_vals
        self.report.boolean_values_standardized += bool_mod_count
        return df

    def _clean_grain_procurement(self, df: pd.DataFrame) -> pd.DataFrame:
        qty_col = "mdm_grain_procured_kg"
        unit_col = "mdm_grain_unit_raw"
        
        procured_kgs = []
        raw_qtys = []
        raw_units = []
        conv_count = 0
        
        for idx in range(len(df)):
            q_val = df[qty_col].iloc[idx] if qty_col in df.columns else 250.0
            u_val = df[unit_col].iloc[idx] if unit_col in df.columns else "KG"
            
            kg_val, orig_q, orig_u, was_conv = normalize_grain_procurement(q_val, u_val)
            procured_kgs.append(kg_val)
            raw_qtys.append(orig_q)
            raw_units.append(orig_u)
            if was_conv:
                conv_count += 1
                
        df["mdm_grain_procured_kg"] = procured_kgs
        df["mdm_grain_procured_raw"] = raw_qtys
        df["mdm_grain_unit_raw"] = raw_units
        self.report.unit_conversions_performed = conv_count
        return df

    def _clean_attendance(self, df: pd.DataFrame) -> pd.DataFrame:
        col = "avg_student_attendance_pct"
        if col not in df.columns:
            df[col] = 75.0
            return df
            
        cleaned_att = []
        mod_count = 0
        for val in df[col]:
            norm_att, mod = normalize_attendance(val)
            cleaned_att.append(norm_att)
            if mod:
                mod_count += 1
        df[col] = cleaned_att
        self.report.attendance_anomalies_repaired = mod_count
        return df

    def _clean_outcomes(self, df: pd.DataFrame) -> pd.DataFrame:
        # Test score (0-100)
        if "avg_test_score" not in df.columns:
            df["avg_test_score"] = 55.0
        else:
            df["avg_test_score"] = pd.to_numeric(df["avg_test_score"], errors="coerce").clip(0.0, 100.0)
            
        # Dropout rate (0-100)
        if "reported_dropout_rate_pct" not in df.columns:
            df["reported_dropout_rate_pct"] = 8.5
        else:
            df["reported_dropout_rate_pct"] = pd.to_numeric(df["reported_dropout_rate_pct"], errors="coerce").clip(0.0, 100.0)
            
        # Total enrolled
        if "total_enrolled" not in df.columns:
            df["total_enrolled"] = 250
        else:
            df["total_enrolled"] = pd.to_numeric(df["total_enrolled"], errors="coerce").fillna(250).astype(int)
        return df

    def _impute_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        imputed_count = 0
        
        # Fill missing booleans with False (conservative infrastructure reporting)
        for b_col in ["has_electricity", "has_drinking_water", "has_separate_girls_toilet", "has_boys_toilet", "mdm_served_status"]:
            nulls = int(df[b_col].isna().sum())
            if nulls > 0:
                df[b_col] = df[b_col].fillna(False).astype(bool)
                imputed_count += nulls
                
        # Fill missing numeric continuous values with district medians
        for num_col, default_val in [
            ("avg_student_attendance_pct", 75.0),
            ("avg_test_score", 55.0),
            ("reported_dropout_rate_pct", 8.0),
            ("mdm_grain_procured_kg", 200.0)
        ]:
            nulls = int(df[num_col].isna().sum())
            if nulls > 0:
                imputed_count += nulls
                district_median = df.groupby("district")[num_col].transform("median")
                df[num_col] = df[num_col].fillna(district_median).fillna(default_val).round(2)
                
        self.report.missing_values_imputed = imputed_count
        return df

    def _compute_indices(self, df: pd.DataFrame) -> pd.DataFrame:
        # 1. Infrastructure Score (0-100 scale: Electricity 30%, Water 30%, Girls Toilet 25%, Boys Toilet 15%)
        inf_score = (
            df["has_electricity"].astype(int) * 30.0 +
            df["has_drinking_water"].astype(int) * 30.0 +
            df["has_separate_girls_toilet"].astype(int) * 25.0 +
            df["has_boys_toilet"].astype(int) * 15.0
        )
        df["infrastructure_score"] = inf_score.round(1)
        
        # 2. Welfare Efficacy Index (0-100: Inf Score 40%, MDM active 30%, Attendance 30%)
        mdm_score = df["mdm_served_status"].astype(int) * 100.0
        df["welfare_efficacy_index"] = (
            df["infrastructure_score"] * 0.4 +
            mdm_score * 0.3 +
            df["avg_student_attendance_pct"] * 0.3
        ).round(1)
        
        # 3. Retention Risk Level (LOW, MEDIUM, HIGH, CRITICAL)
        conditions = [
            (df["reported_dropout_rate_pct"] >= settings.DROPOUT_CRITICAL_THRESHOLD) | ((df["avg_student_attendance_pct"] < 50.0) & (df["infrastructure_score"] < 40.0)),
            (df["reported_dropout_rate_pct"] >= settings.DROPOUT_HIGH_THRESHOLD) | (df["infrastructure_score"] < 50.0) | (df["avg_student_attendance_pct"] < 65.0),
            (df["reported_dropout_rate_pct"] >= settings.DROPOUT_MEDIUM_THRESHOLD) | (df["infrastructure_score"] < 75.0),
        ]
        choices = ["CRITICAL", "HIGH", "MEDIUM"]
        df["retention_risk_level"] = np.select(conditions, choices, default="LOW")
        
        # 4. Priority Action
        act_conditions = [
            df["retention_risk_level"] == "CRITICAL",
            df["retention_risk_level"] == "HIGH",
            df["retention_risk_level"] == "MEDIUM"
        ]
        act_choices = ["Urgent Infrastructure & Welfare Taskforce", "District Officer Advisory", "Standard Monitoring"]
        df["priority_action"] = np.select(act_conditions, act_choices, default="Routine Maintenance")
        
        return df