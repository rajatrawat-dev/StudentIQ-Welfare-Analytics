"""Quality report logger tracking before/after audit metrics."""

import json
from pathlib import Path
from typing import Dict, Any, List
from src.config.settings import settings
from src.utils.helpers import safe_json_dumps
from src.utils.logging import get_logger

logger = get_logger("QualityReport")

class QualityReport:
    def __init__(self):
        self.rows_before = 0
        self.rows_after = 0
        self.duplicates_removed = 0
        self.missing_values_imputed = 0
        self.boolean_values_standardized = 0
        self.unit_conversions_performed = 0
        self.attendance_anomalies_repaired = 0
        self.proxy_attendance_flagged = 0
        self.data_quality_score = 0.0
        self.actions_taken: List[Dict[str, Any]] = []

    def log_action(self, step: str, description: str, affected_count: int):
        self.actions_taken.append({
            "step": step,
            "description": description,
            "affected_count": affected_count
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rows_before": self.rows_before,
            "rows_after": self.rows_after,
            "duplicates_removed": self.duplicates_removed,
            "missing_values_imputed": self.missing_values_imputed,
            "boolean_values_standardized": self.boolean_values_standardized,
            "unit_conversions_performed": self.unit_conversions_performed,
            "attendance_anomalies_repaired": self.attendance_anomalies_repaired,
            "proxy_attendance_flagged": self.proxy_attendance_flagged,
            "data_quality_score": self.data_quality_score,
            "actions_taken": self.actions_taken,
        }

    def save(self, path: Path = settings.QUALITY_REPORT_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(safe_json_dumps(self.to_dict()), encoding="utf-8")
        logger.info(f"Quality report persisted to {path}")

    @classmethod
    def load(cls, path: Path = settings.QUALITY_REPORT_PATH) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}