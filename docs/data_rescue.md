# Data Rescue Engine Specification

## Handled Messy Data Defects

1. **Multilingual & Mixed Boolean Representations**:
   - `"Yes"`, `"Y"`, `"1"`, `"Hai"`, `"true"`, `"ha"` &rarr; `True`
   - `"No"`, `"N"`, `"0"`, `"Nahi"`, `"false"`, `"na"` &rarr; `False`
2. **Grain Procurement Unit Mismatches**:
   - Quantities recorded as `"Quintals"`, `"Qtl"`, `"Kilograms"`, `"kg"`, `"Ton"`.
   - Normalizes mathematically to standard `KG` (1 Quintal = 100 KG; 1 Ton = 1000 KG) while preserving original values and units for auditability.
3. **Proxy Attendance Detection**:
   - Flags suspicious records where attendance is reported as 99-100% despite disrupted Mid-Day Meals or failing exam scores (<20/100).
4. **Range & Bound Violations**:
   - Clamps attendance, test scores, and dropout rates to valid $0.0 - 100.0$ bounds.
5. **Exact & Key Collisions**:
   - Drops duplicate rows and resolves colliding school codes into `SCH-XXXX`.
6. **Missing Value Imputation**:
   - Imputes missing continuous variables using district medians rather than crude global averages.