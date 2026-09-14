"""Central configuration for StudentIQ.
Fully portable across Windows, Linux, and macOS using pathlib.
"""

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

@dataclass(frozen=True)
class Settings:
    # Directory paths
    ROOT_DIR: Path = PROJECT_ROOT
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = PROJECT_ROOT / "data" / "raw"
    PROCESSED_DATA_DIR: Path = PROJECT_ROOT / "data" / "processed"
    
    # File paths
    DEFAULT_RAW_FILE: Path = PROJECT_ROOT / "data" / "raw" / "demo_schools_welfare.csv"
    CLEANED_DATA_PATH: Path = PROJECT_ROOT / "data" / "processed" / "cleaned_schools_welfare.csv"
    DUCKDB_PATH: Path = PROJECT_ROOT / "data" / "processed" / "analytics.duckdb"
    QUALITY_REPORT_PATH: Path = PROJECT_ROOT / "data" / "processed" / "data_quality_report.json"
    MODEL_PATH: Path = PROJECT_ROOT / "data" / "processed" / "dropout_risk_model.joblib"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"

    # Canonical Schema for the Education & EdTech Welfare & Retention Tracker
    CANONICAL_COLUMNS: List[str] = field(default_factory=lambda: [
        "school_id",
        "school_name",
        "district",
        "block",
        "total_enrolled",
        "has_electricity",
        "has_drinking_water",
        "has_separate_girls_toilet",
        "has_boys_toilet",
        "mdm_served_status",
        "mdm_grain_procured_kg",
        "mdm_grain_procured_raw",
        "mdm_grain_unit_raw",
        "avg_student_attendance_pct",
        "avg_test_score",
        "reported_dropout_rate_pct",
        "proxy_attendance_flag",
        "infrastructure_score",
        "welfare_efficacy_index",
        "retention_risk_level",
        "priority_action",
    ])

    # Configurable Boolean synonyms (English, Hindi/Hinglish, numerics)
    BOOLEAN_YES_VALUES: List[str] = field(default_factory=lambda: [
        "yes", "y", "1", "hai", "true", "t", "ha", "haan", "available", "functional", "yes/functional", "1.0"
    ])
    BOOLEAN_NO_VALUES: List[str] = field(default_factory=lambda: [
        "no", "n", "0", "nahi", "false", "f", "na", "unavailable", "non-functional", "no/non-functional", "0.0"
    ])

    # Grain Procurement Unit Conversions to Standard Kilograms (KG)
    # 1 Quintal = 100 Kilograms, 1 Ton = 1000 Kilograms, 1 Gram = 0.001 Kilograms
    UNIT_TO_KG_FACTORS: Dict[str, float] = field(default_factory=lambda: {
        "kg": 1.0,
        "kgs": 1.0,
        "kilogram": 1.0,
        "kilograms": 1.0,
        "quintal": 100.0,
        "quintals": 100.0,
        "qtl": 100.0,
        "qtls": 100.0,
        "ton": 1000.0,
        "tons": 1000.0,
        "metric ton": 1000.0,
        "gm": 0.001,
        "gms": 0.001,
        "gram": 0.001,
        "grams": 0.001,
    })

    # Risk Thresholds (Configurable)
    DROPOUT_CRITICAL_THRESHOLD: float = float(os.getenv("DROPOUT_CRITICAL_RISK_THRESHOLD", "20.0"))
    DROPOUT_HIGH_THRESHOLD: float = float(os.getenv("DROPOUT_HIGH_RISK_THRESHOLD", "12.0"))
    DROPOUT_MEDIUM_THRESHOLD: float = float(os.getenv("DROPOUT_MEDIUM_RISK_THRESHOLD", "6.0"))

    ATTENDANCE_MIN_NORMAL: float = float(os.getenv("ATTENDANCE_ANOMALY_LOW", "45.0"))
    ATTENDANCE_MAX_NORMAL: float = float(os.getenv("ATTENDANCE_ANOMALY_HIGH", "98.5"))

    # Ollama Settings (Optional - Safe Rule Engine Fallback if offline)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    OLLAMA_TIMEOUT_SECONDS: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "5"))

    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()