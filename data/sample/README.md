# DEMO DATA — NOT ORGANIZER DATA

## Official Problem Context
**Track:** Education & EdTech — Student Retention & Welfare Efficacy Tracker  
**Problem Statement:** The State Education Department needs to track the correlation between:
1. Mid-Day Meal scheme
2. School infrastructure
3. Student dropout risks

## Demo Dataset Purpose
The dataset provided in `data/raw/demo_schools_welfare.csv` is a **synthetic demo dataset** built strictly to demonstrate and test the UI, DuckDB analytics, machine learning pipeline, and AI Analyst before the official organizer dataset is provided.

It deliberately contains realistic messy data defects:
- Messy Booleans: `"Yes"`, `"Y"`, `"1"`, `"Hai"`, `"Nahi"`, `"0"`, `"No"`, whitespace
- Grain Procurement Unit Mismatches: `"50 Quintals"`, `"250 kg"`, `"30 Qtl"`, `"500 Kilograms"`, `"4.5 Ton"`
- Proxy Attendance Anomalies: Artificial 99-100% attendance recorded during meal disruptions or failing exam scores
- Duplicate rows, duplicate school IDs, missing values, and district-level variance

## How to Adapt When Organizer Data Arrives
1. Place the organizer raw CSV file into `data/raw/`.
2. Inspect the dataset to discover its actual columns:
   ```bash
   python scripts/inspect_data.py --file data/raw/<organizer_file>.csv
   ```
3. Run the automated data rescue pipeline:
   ```bash
   python scripts/run_pipeline.py --file data/raw/<organizer_file>.csv
   ```
4. The pipeline automatically profiles, cleans, normalizes units/booleans, builds DuckDB views, and trains the risk model.