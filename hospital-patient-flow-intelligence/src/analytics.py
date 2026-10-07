"""
analytics.py
============
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Performs comprehensive descriptive, operational, and patient journey stage analytics:
    - Average, median, max stage waiting times
    - Stage contribution percentage to total encounter delay
    - Departmental throughput and wait time benchmarking
    - Diurnal and shift workload distributions

Outputs:
    - analysis/patient_journey_stages.csv
    - analysis/department_benchmarks.csv
    - analysis/statistical_analysis/stage_wait_by_department.csv
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

def run_analytics():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    clean_csv = os.path.join(base_dir, "data", "processed", "hospital_patient_flow_clean.csv")
    out_dir = os.path.join(base_dir, "analysis")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "patient_flow"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "statistical_analysis"), exist_ok=True)

    print(f"[1/3] Loading clean data from {clean_csv}...")
    df = pd.read_csv(clean_csv, low_memory=False)

    # 1. Patient Journey Stage Decomposition
    print("[2/3] Analyzing multi-stage patient journey delays...")
    stages = [
        {"Stage": "1. Registration", "Wait_Col": "Wait_Registration", "Dur_Col": None},
        {"Stage": "2. Triage", "Wait_Col": "Wait_Triage", "Dur_Col": None},
        {"Stage": "3. Doctor Consultation", "Wait_Col": "Wait_Doctor", "Dur_Col": None},
        {"Stage": "4. Diagnostics", "Wait_Col": "Wait_Diagnostics", "Dur_Col": "Diagnostic_Duration"},
        {"Stage": "5. Treatment", "Wait_Col": "Wait_Treatment", "Dur_Col": "Treatment_Duration"},
        {"Stage": "6. Pharmacy", "Wait_Col": "Wait_Pharmacy", "Dur_Col": None}
    ]

    total_sum_waits = df["Total_Waiting_Time"].sum()
    stage_metrics = []

    for s in stages:
        w_series = df[s["Wait_Col"]]
        # Non-zero for stages that are conditional
        active_w = w_series[w_series > 0] if s["Wait_Col"] in ["Wait_Diagnostics", "Wait_Treatment", "Wait_Pharmacy"] else w_series

        mean_w = round(float(w_series.mean()), 1)
        med_w = round(float(w_series.median()), 1)
        active_mean = round(float(active_w.mean()), 1) if len(active_w) > 0 else 0.0
        max_w = int(w_series.max())
        contrib_pct = round(float((w_series.sum() / total_sum_waits) * 100), 1)

        stage_metrics.append({
            "Stage_Order": s["Stage"],
            "Overall_Avg_Wait_Min": mean_w,
            "Median_Wait_Min": med_w,
            "Active_Patient_Avg_Wait_Min": active_mean,
            "Max_Wait_Min": max_w,
            "Contribution_To_Total_Wait_Pct": contrib_pct
        })

    stage_df = pd.DataFrame(stage_metrics)
    stage_df.to_csv(os.path.join(out_dir, "patient_journey_stages.csv"), index=False)
    stage_df.to_csv(os.path.join(out_dir, "patient_flow", "stage_funnel_summary.csv"), index=False)
    print("   -> Patient journey stage summary exported.")

    # 2. Department Benchmarks
    print("[3/3] Generating clinical department operational benchmarks...")
    dept_bench = df.groupby("Department").agg(
        Patient_Volume=("Visit_ID", "count"),
        Avg_Doctor_Wait=("Wait_Doctor", "mean"),
        Median_Doctor_Wait=("Wait_Doctor", "median"),
        Avg_Total_Wait=("Total_Waiting_Time", "mean"),
        Avg_Length_of_Stay=("Length_of_Stay", "mean"),
        Avg_Capacity_Pressure=("Capacity_Pressure", "mean"),
        Avg_Utilization_Pct=("Department_Utilization", lambda x: round(x.mean() * 100, 1)),
        Avg_Bottleneck_Score=("Bottleneck_Score", "mean"),
        Emergency_Rate_Pct=("Emergency_Flag", lambda x: round((x == "Yes").mean() * 100, 1))
    ).round(1).reset_index().sort_values(by="Avg_Doctor_Wait", ascending=False)

    dept_bench.to_csv(os.path.join(out_dir, "department_benchmarks.csv"), index=False)
    dept_bench.to_csv(os.path.join(out_dir, "statistical_analysis", "department_summary_statistics.csv"), index=False)

    print("-> Analytics module completed successfully.")

if __name__ == "__main__":
    run_analytics()
