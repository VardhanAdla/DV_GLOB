"""
clean_hospital_data.py
======================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Performs comprehensive data cleaning, standardization, missing value imputation,
timestamp normalization, sequence validation, outlier winsorization, and derived
feature engineering on the raw hospital dataset.

Outputs:
    - data/processed/hospital_patient_flow_clean.csv
    - reports/cleaning_audit_summary.json
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def parse_flexible_date(val):
    if pd.isna(val) or val == "":
        return None
    val_str = str(val).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(val_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return val_str

def parse_flexible_datetime(val):
    if pd.isna(val) or val == "":
        return None
    val_str = str(val).strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(val_str, fmt)
        except ValueError:
            pass
    return None

def clean_dataset():
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "hospital_patient_flow_raw.csv")
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "hospital_patient_flow_clean.csv")
    audit_summary = {}

    print(f"[1/8] Reading raw dataset from {raw_path}...")
    df = pd.read_csv(raw_path, low_memory=False)
    initial_rows = len(df)
    audit_summary["initial_raw_records"] = initial_rows

    # 1. Deduplication
    print("[2/8] Identifying and removing duplicate visits...")
    duplicates_mask = df.duplicated(subset=["Visit_ID"], keep="first")
    num_duplicates = int(duplicates_mask.sum())
    df = df[~duplicates_mask].copy().reset_index(drop=True)
    audit_summary["duplicate_records_removed"] = num_duplicates
    print(f"   -> Removed {num_duplicates} duplicate records.")

    # 2. Standardize Categorical Variables
    print("[3/8] Standardizing categorical terminology and casing...")
    # Department
    dept_map = {
        "EMERGENCY": "Emergency", "Emerg": "Emergency", "ER": "Emergency",
        "Paediatrics": "Pediatrics"
    }
    df["Department"] = df["Department"].replace(dept_map).str.strip()

    # Gender
    gender_map = {
        "F": "Female", "female": "Female", "M": "Male", "male": "Male"
    }
    df["Gender"] = df["Gender"].replace(gender_map).str.strip()

    # Priority Level
    priority_map = {
        "CRITICAL": "Critical", "critical": "Critical", "HIGH": "High", "high": "High",
        "MEDIUM": "Medium", "medium": "Medium", "LOW": "Low", "low": "Low"
    }
    df["Priority_Level"] = df["Priority_Level"].replace(priority_map).str.strip()

    # 3. Handle Missing Values
    print("[4/8] Imputing missing values with domain-specific rules...")
    # Missing Age_Group
    missing_age = df["Age_Group"].isna() | (df["Age_Group"] == "")
    audit_summary["missing_age_group_imputed"] = int(missing_age.sum())
    # If pediatrics -> 0-17, else modal 18-35
    df.loc[missing_age & (df["Department"] == "Pediatrics"), "Age_Group"] = "0-17"
    df.loc[missing_age & (df["Department"] != "Pediatrics"), "Age_Group"] = "18-35"

    # Missing Arrival_Mode
    missing_mode = df["Arrival_Mode"].isna() | (df["Arrival_Mode"] == "")
    audit_summary["missing_arrival_mode_imputed"] = int(missing_mode.sum())
    df.loc[missing_mode & (df["Department"] == "Emergency"), "Arrival_Mode"] = "Ambulance"
    df.loc[missing_mode & (df["Department"] != "Emergency"), "Arrival_Mode"] = "Walk-in"

    # Missing Diagnostic_Wait_Time
    diag_nan = df["Diagnostic_Wait_Time"].isna()
    audit_summary["missing_diagnostic_wait_reset"] = int(diag_nan.sum())
    df["Diagnostic_Wait_Time"] = df["Diagnostic_Wait_Time"].fillna(0)

    # Missing Triage_End_Time
    missing_triage_end = df["Triage_End_Time"].isna() | (df["Triage_End_Time"] == "")
    audit_summary["missing_triage_end_reconstructed"] = int(missing_triage_end.sum())
    for idx in df[missing_triage_end].index:
        t_start = parse_flexible_datetime(df.at[idx, "Triage_Start_Time"])
        if t_start:
            df.at[idx, "Triage_End_Time"] = (t_start + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")

    # 4. Standardize Dates and Timestamps
    print("[5/8] Normalizing date and timestamp formats...")
    df["Arrival_Date"] = df["Arrival_Date"].apply(parse_flexible_date)

    timestamp_cols = [
        "Registration_Time", "Triage_Start_Time", "Triage_End_Time",
        "Doctor_Queue_Start", "Doctor_Consultation_Start", "Doctor_Consultation_End",
        "Diagnostic_Start", "Diagnostic_End", "Treatment_Start", "Treatment_End",
        "Pharmacy_Start", "Pharmacy_End", "Discharge_Time"
    ]
    for col in timestamp_cols:
        df[col] = df[col].astype(str).str.replace("T", " ")
        # Convert 'nan' to empty string
        df[col] = df[col].replace({"nan": "", "None": ""})

    # 5. Correct Negative Waiting Times and Chronological Inconsistencies
    print("[6/8] Correcting negative wait times and impossible timestamp sequences...")
    # Negative wait times
    neg_doc_wait = df["Doctor_Wait_Time"] < 0
    audit_summary["negative_doctor_wait_corrected"] = int(neg_doc_wait.sum())
    # Reassign based on priority level median wait
    priority_median_waits = {"Critical": 3, "High": 14, "Medium": 32, "Low": 48}
    for prio, median_val in priority_median_waits.items():
        df.loc[neg_doc_wait & (df["Priority_Level"] == prio), "Doctor_Wait_Time"] = median_val

    neg_reg_wait = df["Registration_Wait_Time"] < 0
    audit_summary["negative_registration_wait_corrected"] = int(neg_reg_wait.sum())
    df.loc[neg_reg_wait, "Registration_Wait_Time"] = 8

    # Sequence consistency: Consultation Start vs Triage Start
    seq_fixed = 0
    for idx in df.index:
        t_start = parse_flexible_datetime(df.at[idx, "Triage_Start_Time"])
        d_start = parse_flexible_datetime(df.at[idx, "Doctor_Consultation_Start"])
        if t_start and d_start and d_start < t_start:
            # Shift consultation start to after triage end
            t_end = parse_flexible_datetime(df.at[idx, "Triage_End_Time"]) or (t_start + timedelta(minutes=5))
            new_doc_start = t_end + timedelta(minutes=int(df.at[idx, "Doctor_Wait_Time"]))
            df.at[idx, "Doctor_Consultation_Start"] = new_doc_start.strftime("%Y-%m-%d %H:%M:%S")
            # Also adjust consultation end
            df.at[idx, "Doctor_Consultation_End"] = (new_doc_start + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
            seq_fixed += 1
    audit_summary["sequence_errors_reconciled"] = seq_fixed

    # 6. Treat Extreme Outliers (Winsorize data entry typos like 9999)
    print("[7/8] Handling logging typos and outlier waiting times...")
    extreme_wait_mask = (df["Doctor_Wait_Time"] > 500) | (df["Total_Waiting_Time"] > 2000)
    audit_summary["extreme_wait_outliers_winsorized"] = int(extreme_wait_mask.sum())
    df.loc[extreme_wait_mask, "Doctor_Wait_Time"] = 120  # capped at high 99th percentile

    # 7. Recalculate Metrics, Waiting Time Categories & Bottleneck Scores
    print("[8/8] Engineering clean analytical fields, operational pressure, and bottleneck score...")
    # Recalculate total wait time
    df["Total_Waiting_Time"] = (
        df["Registration_Wait_Time"].astype(float) +
        df["Triage_Wait_Time"].astype(float) +
        df["Doctor_Wait_Time"].astype(float) +
        df["Diagnostic_Wait_Time"].astype(float) +
        df["Treatment_Wait_Time"].astype(float) +
        df["Pharmacy_Wait_Time"].astype(float)
    ).astype(int)

    # Waiting Time Category
    def categorize_wait(wait_min):
        if wait_min < 30:
            return "Low Wait (<30m)"
        elif wait_min <= 60:
            return "Moderate Wait (30-60m)"
        elif wait_min <= 90:
            return "High Wait (60-90m)"
        else:
            return "Severe Delay (>90m)"

    df["Waiting_Time_Category"] = df["Total_Waiting_Time"].apply(categorize_wait)

    # Department Utilization & Capacity Pressure
    # Capacity Pressure Index = (Occupied beds approximation / Department Capacity) * (Nominal Staff / Staff Available)
    df["Bed_Occupancy_Rate"] = (
        (df["Department_Capacity"] - df["Bed_Availability"]) / df["Department_Capacity"]
    ).clip(0.0, 1.0).round(3)

    # Bottleneck Score (Project Analytical Metric: 0 to 100 scale)
    # Methodology:
    # 40% Wait Time Pressure (normalized against 90 min benchmark)
    # 35% Capacity / Bed Pressure (normalized against full capacity)
    # 25% Staff Stretch Pressure (ratio of capacity to available staff)
    wait_component = (df["Doctor_Wait_Time"] / 75.0).clip(0.0, 1.5) * 40.0
    bed_component = df["Bed_Occupancy_Rate"] * 35.0
    staff_stretch = (df["Department_Capacity"] / (df["Staff_Availability"] * 4.0)).clip(0.5, 2.0)
    staff_component = (staff_stretch / 2.0) * 25.0

    df["Bottleneck_Score"] = (wait_component + bed_component + staff_component).clip(0.0, 100.0).round(1)

    def categorize_bottleneck(score):
        if score >= 70.0:
            return "Severe Bottleneck"
        elif score >= 50.0:
            return "Moderate Congestion"
        elif score >= 35.0:
            return "Manageable Flow"
        else:
            return "Optimal Flow"

    df["Bottleneck_Category"] = df["Bottleneck_Score"].apply(categorize_bottleneck)

    # Save Cleaned Dataset
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)
    audit_summary["final_clean_records"] = len(df)
    audit_summary["clean_columns_count"] = len(df.columns)
    print(f"-> Successfully saved clean dataset ({len(df)} records) to: {os.path.abspath(clean_path)}")

    # Save Audit Summary JSON
    audit_path = os.path.join(os.path.dirname(__file__), "..", "reports", "cleaning_audit_summary.json")
    os.makedirs(os.path.dirname(audit_path), exist_ok=True)
    with open(audit_path, "w") as f:
        json.dump(audit_summary, f, indent=4)
    print(f"-> Saved cleaning audit summary to: {os.path.abspath(audit_path)}")
    return clean_path

if __name__ == "__main__":
    clean_dataset()
