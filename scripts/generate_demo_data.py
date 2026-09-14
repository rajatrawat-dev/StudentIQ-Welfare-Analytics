"""Generates realistic synthetic messy demo data for testing the Welfare & Retention pipeline."""

import random
import csv
from pathlib import Path
import pandas as pd
import numpy as np

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "demo_schools_welfare.csv"

DISTRICTS = ["North Valley", "South Hill", "East Coast", "West Plain", "Central Zila", "Lake Plateau"]
BLOCKS = ["Block Alpha", "Block Beta", "Block Gamma", "Block Delta", "Block Epsilon"]
SCHOOL_PREFIXES = ["Govt High School", "Model Primary School", "Adarsh Vidyalaya", "Zila Parishad School", "Sarvodaya Kanya School"]

BOOLEAN_CHOICES = ["Yes", "Y", "1", "Hai", "No", "N", "0", "Nahi", "true", "false", "  Yes  ", " ha "]
UNIT_CHOICES = ["Quintals", "kg", "Qtl", "Kilograms", "Ton", "KG", "quintal"]

def generate_demo_dataset(num_records: int = 500):
    random.seed(42)
    np.random.seed(42)
    
    rows = []
    for i in range(1, num_records + 1):
        sch_id = f"SCH-{1000 + i}"
        sch_name = f"{random.choice(SCHOOL_PREFIXES)} {i}"
        district = random.choice(DISTRICTS)
        block = random.choice(BLOCKS)
        total_enrolled = random.randint(80, 750)
        
        # Boolean infrastructure with realistic messy variations
        elec = random.choice(BOOLEAN_CHOICES)
        water = random.choice(BOOLEAN_CHOICES)
        girls_toilet = random.choice(BOOLEAN_CHOICES)
        boys_toilet = random.choice(BOOLEAN_CHOICES)
        mdm_status = random.choice(BOOLEAN_CHOICES)
        
        # Unit mismatches in grain procurement
        unit = random.choice(UNIT_CHOICES)
        if unit in ["Quintals", "Qtl", "quintal"]:
            qty_raw = round(random.uniform(2.0, 35.0), 1)
        elif unit == "Ton":
            qty_raw = round(random.uniform(0.2, 3.5), 2)
        else:
            qty_raw = round(random.uniform(200.0, 3500.0), 1)
            
        # Attendance & Test scores
        att_raw = round(random.uniform(42.0, 96.0), 1)
        if random.random() < 0.15:
            att_val = f"{att_raw}%"
        elif random.random() < 0.1:
            att_val = round(att_raw / 100.0, 2)
        else:
            att_val = att_raw
            
        test_score = round(random.uniform(25.0, 88.0), 1)
        dropout_rate = round(random.uniform(1.5, 28.0), 1)
        
        # Inject deliberate proxy attendance anomaly (100% attendance with 0 meal and failing score)
        if random.random() < 0.04:
            att_val = "100%"
            mdm_status = "Nahi"
            test_score = 12.5
            dropout_rate = 26.0

        rows.append({
            "School Code": sch_id,
            "School Name": sch_name,
            "District Name": district,
            "Block": block,
            "Enrolled Students": total_enrolled,
            "Electricity Available": elec,
            "Drinking Water Facility": water,
            "Separate Girls Toilet": girls_toilet,
            "Boys Toilet": boys_toilet,
            "Mid Day Meal Served": mdm_status,
            "Grain Quantity Procured": qty_raw,
            "Procurement Unit": unit,
            "Attendance Rate": att_val,
            "Average Marks": test_score,
            "Annual Dropout Rate": dropout_rate,
        })

    # Add deliberate duplicate rows
    for j in range(12):
        rows.append(rows[j].copy())
        
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated DEMO dataset with {len(df)} rows at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_demo_dataset()