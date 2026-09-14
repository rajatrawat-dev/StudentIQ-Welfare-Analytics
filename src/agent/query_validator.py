"""AI Safety Validator enforcing strict read-only analytical execution."""

import re
from typing import Tuple

FORBIDDEN_KEYWORDS = [
    r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b",
    r"\bALTER\b", r"\bCREATE\b", r"\bTRUNCATE\b", r"\bGRANT\b",
    r"\bREVOKE\b", r"\bATTACH\b", r"\bDETACH\b", r"\bCOPY\b",
    r"\bPRAGMA\b", r"\bEXEC\b", r"\bEXECUTE\b", r"\bSHUTDOWN\b",
    r"\bREPLACE\b"
]

ALLOWED_ENTITIES = ["schools", "district_summary", "risk_summary"]

def validate_query(sql: str) -> Tuple[bool, str]:
    if not sql or not sql.strip():
        return False, "Query is empty."

    cleaned = sql.strip().strip(";").strip()

    if ";" in cleaned:
        return False, "Multi-statement queries are strictly blocked for AI Safety."

    first_word = cleaned.split()[0].upper()
    if first_word not in ["SELECT", "WITH"]:
        return False, f"Forbidden query type '{first_word}'. Only read-only SELECT queries are permitted."

    for pattern in FORBIDDEN_KEYWORDS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            match = re.search(pattern, cleaned, re.IGNORECASE).group(0)
            return False, f"Security Violation: Forbidden statement keyword '{match}' blocked."

    lower_sql = cleaned.lower()
    if not any(e in lower_sql for e in ALLOWED_ENTITIES):
        return False, f"Query must reference approved educational entities: {', '.join(ALLOWED_ENTITIES)}"

    return True, "Query validated successfully."