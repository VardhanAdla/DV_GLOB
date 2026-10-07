"""
feature_engineering.py
======================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Performs comprehensive feature engineering for Tableau and Streamlit dashboards:
    - Waiting Time Categories (<30m, 30-60m, 60-90m, >90m)
    - LOS Categories (<2h, 2-4h, 4-6h, >6h)
    - Department Utilization & Capacity Pressure Index
    - Transparent Academic Bottleneck Scoring (0-100) & Tiers (Low, Moderate, High, Critical)
    - Peak Hour and Peak Shift indicators

Outputs:
    - data/processed/hospital_patient_flow_clean.csv (enriched)
    - tableau/data/hospital_patient_flow_tableau.csv
"""

import os
import numpy as np
import pandas as pd

def engineer_features():
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "hospital_patient_flow_clean.csv")
    tableau_data_path = os.path.join(os.path.dirname(__file__), "..", "tableau", "data", "hospital_patient_flow_tableau.csv")

    print(f"[1/4] Loading clean dataset from {clean_path}...")
    df = pd.read_csv(clean_path, low_memory=False)

    # 1. Waiting Time Category
    print("[2/4] Engineering binned categorical metrics...")
    def categorize_wait(m):
        if m < 30:
            return "Low Wait (<30m)"
        elif m <= 60:
            return "Moderate Wait (30-60m)"
        elif m <= 90:
            return "High Wait (60-90m)"
        else:
            return "Severe Delay (>90m)"

    df["Waiting_Time_Category"] = df["Total_Waiting_Time"].apply(categorize_wait)

    # 2. Length of Stay Category
    def categorize_los(m):
        if m < 120:
            return "Under 2 Hours"
        elif m <= 240:
            return "2 - 4 Hours"
        elif m <= 360:
            return "4 - 6 Hours"
        else:
            return "Over 6 Hours"

    df["LOS_Category"] = df["Length_of_Stay"].apply(categorize_los)

    # 3. Transparent Academic Bottleneck Score (0-100 scale)
    # Formula:
    # 40% Waiting Time Pressure (Doctor wait normalized against 75m benchmark)
    # 30% Capacity Pressure (Department Utilization normalized against 100%)
    # 20% Volume Pressure (Patient arrivals / peak threshold)
    # 10% Staffing Strain (Staff ratio against max shift capacity)
    # "This is an academic analytical model and is not a clinically validated hospital standard."
    print("[3/4] Re-evaluating transparent academic Bottleneck Model...")
    w_comp = (df["Wait_Doctor"] / 75.0).clip(0.0, 1.5) * 40.0
    c_comp = df["Department_Utilization"] * 30.0
    v_comp = (df["Capacity_Pressure"] / 2.0).clip(0.0, 1.5) * 20.0
    s_comp = (df["Department_Capacity"] / (df["Staff_Available"] * 5.0)).clip(0.5, 2.0) * 5.0

    df["Bottleneck_Score"] = (w_comp + c_comp + v_comp + s_comp).clip(5.0, 98.0).round(1)

    def categorize_bottleneck(s):
        if s >= 70.0:
            return "Critical"
        elif s >= 50.0:
            return "High"
        elif s >= 35.0:
            return "Moderate"
        else:
            return "Low"

    df["Bottleneck_Category"] = df["Bottleneck_Score"].apply(categorize_bottleneck)

    # 4. Department Utilization Percentage
    df["Department_Utilization_Pct"] = (df["Department_Utilization"] * 100).round(1)

    # 5. Peak Hour & Shift Markers
    peak_hours = [9, 10, 11, 16, 17, 18, 19, 20]
    df["Is_Peak_Hour"] = df["Hour"].isin(peak_hours).map({True: "Peak Hour", False: "Off-Peak"})
    df["Is_Peak_Shift"] = df["Shift"].map({"Morning": "High Load", "Afternoon": "Moderate Load", "Night": "Emergency Load"})

    # Save enriched data
    print("[4/4] Writing enriched dataset to processed and Tableau locations...")
    df.to_csv(clean_path, index=False)
    os.makedirs(os.path.dirname(tableau_data_path), exist_ok=True)
    df.to_csv(tableau_data_path, index=False)
    print(f"-> Processed CSV updated: {os.path.abspath(clean_path)}")
    print(f"-> Tableau Data Source ready: {os.path.abspath(tableau_data_path)}")
    return tableau_data_path

if __name__ == "__main__":
    engineer_features()
