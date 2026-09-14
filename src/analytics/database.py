"""Embedded DuckDB analytical database manager."""

import duckdb
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger("DatabaseManager")

class DatabaseManager:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.DUCKDB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        if self._conn is None:
            try:
                self._conn = duckdb.connect(database=str(self.db_path), read_only=False)
            except Exception as e:
                logger.warning(f"Could not open file-based DuckDB ({e}), using in-memory mode.")
                self._conn = duckdb.connect(database=":memory:")
        return self._conn

    def init_database(self, df: Optional[pd.DataFrame] = None) -> None:
        conn = self.get_connection()
        if df is None:
            if settings.CLEANED_DATA_PATH.exists():
                df = pd.read_csv(settings.CLEANED_DATA_PATH)
            else:
                logger.warning("No data found to populate DuckDB.")
                return

        conn.register("df_schools_temp", df)
        conn.execute("CREATE OR REPLACE TABLE schools AS SELECT * FROM df_schools_temp;")
        conn.unregister("df_schools_temp")

        # District-level analytical summary
        conn.execute("""
            CREATE OR REPLACE VIEW district_summary AS
            SELECT 
                district,
                COUNT(*) as school_count,
                SUM(total_enrolled) as total_students,
                ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
                ROUND(AVG(avg_test_score), 1) as avg_test_score,
                ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate,
                ROUND(SUM(CASE WHEN has_electricity THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as electricity_pct,
                ROUND(SUM(CASE WHEN has_drinking_water THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as water_pct,
                ROUND(SUM(CASE WHEN has_separate_girls_toilet THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as girls_toilet_pct,
                ROUND(SUM(CASE WHEN mdm_served_status THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as mdm_coverage_pct,
                SUM(CASE WHEN retention_risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_schools
            FROM schools
            GROUP BY district;
        """)

        # Risk breakdown summary
        conn.execute("""
            CREATE OR REPLACE VIEW risk_summary AS
            SELECT 
                retention_risk_level,
                COUNT(*) as school_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM schools), 1) as percentage,
                ROUND(AVG(avg_student_attendance_pct), 1) as avg_attendance,
                ROUND(AVG(avg_test_score), 1) as avg_test_score,
                ROUND(AVG(reported_dropout_rate_pct), 1) as avg_dropout_rate
            FROM schools
            GROUP BY retention_risk_level;
        """)

        logger.info(f"DuckDB initialized with {len(df)} school records and analytical views.")

    def execute_query(self, query: str, params: Optional[Any] = None) -> pd.DataFrame:
        conn = self.get_connection()
        try:
            if params:
                return conn.execute(query, params).df()
            return conn.execute(query).df()
        except Exception as e:
            logger.error(f"Query execution failed: {e} | Query: {query}")
            raise

    def close(self):
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

db_manager = DatabaseManager()