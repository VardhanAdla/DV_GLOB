"""
bottleneck_detection.py
=======================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Implements the Transparent Academic Bottleneck Model:
    Bottleneck_Score = 0.40 * (Waiting_Time_Pressure) +
                       0.30 * (Capacity_Pressure) +
                       0.20 * (Patient_Volume_Pressure) +
                       0.10 * (Staff_Pressure)

Scale: 0 to 100
Categories: Low (<35), Moderate (35-49), High (50-69), Critical (>=70)

NOTE:
"This is an academic analytical model and is not a clinically validated hospital standard."

Outputs:
    - analysis/bottleneck_matrix.csv
    - analysis/department_bottleneck_ranking.csv
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

DISCLAIMER = "This is an academic analytical model and is not a clinically validated hospital standard."

def run_bottleneck_detection():
    print(f"\n--- Bottleneck Model Initialized ---")
    print(f"DISCLAIMER: {DISCLAIMER}")

    base_dir = os.path.join(os.path.dirname(__file__), "..")
    clean_csv = os.path.join(base_dir, "data", "processed", "hospital_patient_flow_clean.csv")
    out_dir = os.path.join(base_dir, "analysis")
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(clean_csv, low_memory=False)

    # Department x Hour Bottleneck Matrix (12 Departments x 24 Hours)
    print("Constructing 12-Department x 24-Hour Congestion Matrix...")
    matrix = df.pivot_table(
        index="Department",
        columns="Hour",
        values="Bottleneck_Score",
        aggfunc="mean"
    ).round(1)

    matrix_path = os.path.join(out_dir, "bottleneck_matrix.csv")
    matrix.to_csv(matrix_path)
    print(f"-> Saved Bottleneck Matrix to: {os.path.abspath(matrix_path)}")

    # Department Bottleneck Ranking
    ranking = df.groupby("Department").agg(
        Total_Encounters=("Visit_ID", "count"),
        Avg_Bottleneck_Score=("Bottleneck_Score", "mean"),
        Critical_Hours_Count=("Bottleneck_Category", lambda x: (x == "Critical").sum()),
        High_Hours_Count=("Bottleneck_Category", lambda x: (x == "High").sum()),
        Avg_Wait_Doctor=("Wait_Doctor", "mean"),
        Avg_Utilization=("Department_Utilization", lambda x: round(x.mean() * 100, 1))
    ).round(1).reset_index().sort_values(by="Avg_Bottleneck_Score", ascending=False)

    ranking_path = os.path.join(out_dir, "department_bottleneck_ranking.csv")
    ranking.to_csv(ranking_path, index=False)
    print(f"-> Saved Department Bottleneck Rankings to: {os.path.abspath(ranking_path)}")

    return ranking

if __name__ == "__main__":
    run_bottleneck_detection()
