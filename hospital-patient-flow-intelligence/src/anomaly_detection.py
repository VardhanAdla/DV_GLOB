"""
anomaly_detection.py
====================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Performs operational anomaly detection using:
    1. Interquartile Range (IQR) Thresholding: Delays > Q3 + 1.5 * IQR
    2. Scikit-learn Isolation Forest on multi-variable operational state:
       [Wait_Doctor, Length_of_Stay, Department_Utilization, Capacity_Pressure]

Outputs:
    - data/validation/anomaly_analysis.csv
    - analysis/anomalies/operational_anomalies_detected.csv
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def run_anomaly_detection():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    clean_csv = os.path.join(base_dir, "data", "processed", "hospital_patient_flow_clean.csv")
    val_out = os.path.join(base_dir, "data", "validation", "anomaly_analysis.csv")
    anom_dir = os.path.join(base_dir, "analysis", "anomalies")
    os.makedirs(anom_dir, exist_ok=True)
    os.makedirs(os.path.dirname(val_out), exist_ok=True)

    print(f"[1/4] Ingesting data from {clean_csv} for anomaly detection...")
    df = pd.read_csv(clean_csv, low_memory=False)

    # 1. IQR-based Detection on Wait_Doctor & Capacity_Pressure
    print("[2/4] Computing non-parametric IQR outlier boundaries...")
    q75_wait, q25_wait = np.percentile(df["Wait_Doctor"], [75, 25])
    iqr_wait = q75_wait - q25_wait
    wait_cutoff = q75_wait + (1.5 * iqr_wait)

    q75_los, q25_los = np.percentile(df["Length_of_Stay"], [75, 25])
    iqr_los = q75_los - q25_los
    los_cutoff = q75_los + (1.5 * iqr_los)

    df["IQR_Wait_Anomaly"] = df["Wait_Doctor"] > wait_cutoff
    df["IQR_LOS_Anomaly"] = df["Length_of_Stay"] > los_cutoff

    # 2. Machine Learning Isolation Forest Detection
    print("[3/4] Fitting Scikit-Learn Isolation Forest on multi-dimensional operational metrics...")
    feature_cols = ["Wait_Doctor", "Length_of_Stay", "Department_Utilization", "Capacity_Pressure"]
    X = df[feature_cols].copy()

    iso = IsolationForest(n_estimators=100, contamination=0.035, random_state=42)
    iso_preds = iso.fit_predict(X)  # -1 for anomaly, 1 for normal
    df["Isolation_Forest_Anomaly"] = (iso_preds == -1)

    # Combine flags
    df["Operational_Anomaly"] = df["IQR_Wait_Anomaly"] | df["Isolation_Forest_Anomaly"] | (df["Anomaly_Flag"] == "Yes")

    # 3. Export Summary & Table
    print("[4/4] Writing anomaly analysis dataset and flagged events...")
    anomaly_subset = df[df["Operational_Anomaly"]][[
        "Visit_ID", "Arrival_Date", "Department", "Shift", "Hour",
        "Wait_Doctor", "Length_of_Stay", "Department_Utilization",
        "Capacity_Pressure", "Bottleneck_Score", "Anomaly_Type", "Isolation_Forest_Anomaly"
    ]].copy()

    anomaly_subset.to_csv(val_out, index=False)
    anomaly_subset.to_csv(os.path.join(anom_dir, "operational_anomalies_detected.csv"), index=False)

    print(f"-> Successfully flagged {len(anomaly_subset)} operational anomaly records.")
    print(f"-> Saved to: {os.path.abspath(val_out)}")
    return val_out

if __name__ == "__main__":
    run_anomaly_detection()
