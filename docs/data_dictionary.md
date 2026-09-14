# StudentIQ Data Dictionary

The canonical schema represents ground truth for the State Education Department:

| Column Name | Data Type | Permitted Values / Range | Cleaning & Standardization Rule | Business Usage |
|---|---|---|---|---|
| `school_id` | String | `SCH-XXXX` | Formatted alphanumeric unique institutional identifier | Primary key for school tracking |
| `school_name` | String | Title Case Text | Stripped of extra spaces, punctuation cleaned | Human-readable school reference |
| `district` | String | Standardized District | Normalized district taxonomy | Regional policy aggregation |
| `block` | String | Standardized Block | Normalized administrative sub-district | Local administrative cluster |
| `total_enrolled` | Integer | $\ge 0$ | Parsed numeric count of registered students | Per-capita grain and attendance denominator |
| `has_electricity` | Boolean | `True` / `False` | Mapped from `"Yes"`, `"Y"`, `"1"`, `"Hai"`, `"Nahi"`, `"No"`, `"0"` | Basic learning infrastructure indicator |
| `has_drinking_water` | Boolean | `True` / `False` | Mapped from boolean synonyms | Health and basic welfare compliance |
| `has_separate_girls_toilet` | Boolean | `True` / `False` | Mapped from boolean synonyms | Key gender-retention determinant |
| `has_boys_toilet` | Boolean | `True` / `False` | Mapped from boolean synonyms | Basic sanitation compliance |
| `mdm_served_status` | Boolean | `True` / `False` | Mapped from boolean synonyms | Daily Mid-Day Meal active indicator |
| `mdm_grain_procured_kg` | Float | $\ge 0.0$ | Converted from Quintals (x100) or Tons (x1000) into KG | Nutritional procurement tracking |
| `mdm_grain_unit_raw` | String | Text | Preserves original reported unit (`Quintals`, `kg`, etc.) | Auditing and data provenance |
| `avg_student_attendance_pct` | Float | $0.0 - 100.0$ | Parsed percentages and decimal ratios | Student engagement benchmark |
| `avg_test_score` | Float | $0.0 - 100.0$ | Academic marks clamped to valid 0-100 scale | Academic outcome indicator |
| `reported_dropout_rate_pct` | Float | $0.0 - 100.0$ | Annual student dropout rate clamped to valid bounds | Core retention risk target |
| `proxy_attendance_flag` | Boolean | `True` / `False` | Triggered if 100% attendance occurs with 0 meals or failing scores | Integrity and audit alert |
| `infrastructure_score` | Float | $0.0 - 100.0$ | Weighted sum (Electricity 30%, Water 30%, Girls Toilet 25%, Boys Toilet 15%) | Comprehensive school facility rating |
| `welfare_efficacy_index` | Float | $0.0 - 100.0$ | Combined score (Inf 40%, Meal 30%, Attendance 30%) | Composite school welfare rating |
| `retention_risk_level` | String | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | Calibrated categorization of student retention vulnerability | Decision support prioritization |
| `priority_action` | String | Text | Actionable administrative prescription | Field taskforce dispatch queue |