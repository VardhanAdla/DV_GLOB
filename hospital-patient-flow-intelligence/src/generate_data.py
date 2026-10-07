"""
generate_data.py
================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Generates approximately 30,000 realistic synthetic hospital patient encounter records
spanning 10 months across 12 departments with queue mechanics, peak hours, shifts,
acuity rules, and controlled EHR data quality anomalies.

Outputs:
    - data/raw/hospital_patient_flow_raw.csv
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

DEPARTMENTS = [
    "Emergency", "General Medicine", "Cardiology", "Orthopedics",
    "Neurology", "Pediatrics", "General Surgery", "Radiology",
    "Laboratory", "Pharmacy", "ICU", "OPD"
]

DEPT_WEIGHTS = [
    0.20,  # Emergency
    0.18,  # General Medicine
    0.09,  # Cardiology
    0.10,  # Orthopedics
    0.05,  # Neurology
    0.10,  # Pediatrics
    0.06,  # General Surgery
    0.05,  # Radiology
    0.05,  # Laboratory
    0.04,  # Pharmacy
    0.03,  # ICU
    0.05   # OPD
]

DEPT_CONFIG = {
    "Emergency": {"capacity": 60, "staff_range": (10, 18), "consult_time": (12, 28)},
    "General Medicine": {"capacity": 65, "staff_range": (8, 14), "consult_time": (10, 22)},
    "Cardiology": {"capacity": 35, "staff_range": (4, 8), "consult_time": (15, 30)},
    "Orthopedics": {"capacity": 40, "staff_range": (5, 9), "consult_time": (12, 25)},
    "Neurology": {"capacity": 25, "staff_range": (3, 6), "consult_time": (18, 35)},
    "Pediatrics": {"capacity": 45, "staff_range": (6, 10), "consult_time": (10, 22)},
    "General Surgery": {"capacity": 30, "staff_range": (4, 7), "consult_time": (15, 35)},
    "Radiology": {"capacity": 35, "staff_range": (4, 8), "consult_time": (8, 20)},
    "Laboratory": {"capacity": 45, "staff_range": (5, 9), "consult_time": (5, 15)},
    "Pharmacy": {"capacity": 50, "staff_range": (4, 8), "consult_time": (4, 10)},
    "ICU": {"capacity": 20, "staff_range": (6, 12), "consult_time": (25, 50)},
    "OPD": {"capacity": 70, "staff_range": (10, 16), "consult_time": (8, 18)}
}

def determine_shift(hour):
    if 6 <= hour < 14:
        return "Morning"
    elif 14 <= hour < 22:
        return "Afternoon"
    else:
        return "Night"

def generate_dataset(num_records=30000):
    print(f"[1/5] Initializing synthetic patient flow generation ({num_records} baseline visits)...")
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 10, 31)
    total_days = (end_date - start_date).days + 1

    num_unique_patients = int(num_records * 0.70)
    patient_pool = [f"P-{10000 + i}" for i in range(num_unique_patients)]

    # Outpatient hourly curve (peaks 09:00-12:00, 16:00-18:00)
    outpatient_hourly_prob = np.array([
        0.005, 0.003, 0.002, 0.002, 0.005, 0.015,
        0.040, 0.075, 0.110, 0.125, 0.115, 0.095,
        0.065, 0.045, 0.055, 0.075, 0.080, 0.050,
        0.025, 0.010, 0.003, 0.002, 0.001, 0.001
    ])
    outpatient_hourly_prob /= outpatient_hourly_prob.sum()

    # Emergency & ICU hourly curve (active 24/7, peak late afternoon and evening/night)
    emergency_hourly_prob = np.array([
        0.035, 0.030, 0.025, 0.020, 0.020, 0.025,
        0.030, 0.035, 0.045, 0.050, 0.050, 0.050,
        0.045, 0.045, 0.050, 0.055, 0.060, 0.065,
        0.070, 0.070, 0.060, 0.050, 0.045, 0.040
    ])
    emergency_hourly_prob /= emergency_hourly_prob.sum()

    # Seasonal surge dates
    surge_emergency_days = [datetime.date(2025, 5, d) for d in range(10, 18)]
    surge_monsoon_days = [datetime.date(2025, 7, d) for d in range(15, 27)]

    records = []
    print("[2/5] Simulating patient journeys, stage durations, and operational metrics...")

    for idx in range(num_records):
        visit_id = f"V-2025-{idx + 1:05d}"
        patient_id = random.choice(patient_pool)

        # Date & Day
        day_offset = random.randint(0, total_days - 1)
        arrival_date = start_date + datetime.timedelta(days=day_offset)
        dow = arrival_date.strftime("%A")
        month = arrival_date.strftime("%B")
        is_weekend = dow in ["Saturday", "Sunday"]

        # Season
        if month in ["December", "January", "February"]:
            season = "Winter"
        elif month in ["March", "April"]:
            season = "Spring"
        elif month in ["May", "June"]:
            season = "Summer"
        elif month in ["July", "August", "September"]:
            season = "Monsoon"
        else:
            season = "Autumn"

        # Department selection
        if is_weekend or arrival_date in surge_emergency_days:
            curr_weights = [0.30, 0.15, 0.08, 0.09, 0.04, 0.08, 0.05, 0.04, 0.04, 0.04, 0.05, 0.04]
        elif arrival_date in surge_monsoon_days:
            curr_weights = [0.18, 0.25, 0.07, 0.07, 0.04, 0.18, 0.05, 0.04, 0.04, 0.03, 0.02, 0.03]
        else:
            curr_weights = DEPT_WEIGHTS

        dept = np.random.choice(DEPARTMENTS, p=curr_weights)
        is_emerg = dept in ["Emergency", "ICU"]
        emergency_flag = "Yes" if (is_emerg or random.random() < 0.06) else "No"

        # Hour of arrival
        if is_emerg:
            hour = np.random.choice(range(24), p=emergency_hourly_prob)
        else:
            hour = np.random.choice(range(24), p=outpatient_hourly_prob)

        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        arr_dt = datetime.datetime(arrival_date.year, arrival_date.month, arrival_date.day, hour, minute, second)
        shift = determine_shift(hour)

        # Demographics
        if dept == "Pediatrics":
            age = random.randint(1, 16)
        else:
            age = int(np.clip(np.random.normal(46, 19), 17, 92))
        gender = np.random.choice(["Female", "Male", "Other"], p=[0.50, 0.48, 0.02])

        # Patient Type & Priority Level
        if is_emerg:
            patient_type = "Emergency"
            priority = np.random.choice(["Critical", "High", "Medium", "Low"], p=[0.20, 0.40, 0.32, 0.08])
        else:
            patient_type = np.random.choice(["Walk-in", "Appointment", "Referral", "Follow-up"], p=[0.46, 0.32, 0.12, 0.10])
            if patient_type == "Appointment":
                priority = np.random.choice(["Medium", "Low"], p=[0.30, 0.70])
            else:
                priority = np.random.choice(["High", "Medium", "Low"], p=[0.14, 0.56, 0.30])

        # Department Capacity & Resources
        dinfo = DEPT_CONFIG[dept]
        capacity = dinfo["capacity"]
        s_min, s_max = dinfo["staff_range"]

        if shift == "Night":
            staff_avail = random.randint(s_min, max(s_min, int(s_max * 0.75)))
        elif 9 <= hour <= 17:
            staff_avail = random.randint(int(s_min * 1.1), s_max)
        else:
            staff_avail = random.randint(s_min, s_max)

        # Bed availability
        base_free = max(1, int(capacity * 0.30))
        if arrival_date in surge_emergency_days and is_emerg:
            bed_avail = max(0, random.randint(0, 3))
        elif arrival_date in surge_monsoon_days and dept in ["General Medicine", "Pediatrics"]:
            bed_avail = max(1, random.randint(1, 4))
        else:
            bed_avail = max(1, random.randint(3, base_free))

        # Hourly congestion factor
        if (9 <= hour <= 12 or 16 <= hour <= 18) and not is_emerg:
            cong_mult = 1.35
        elif is_emerg and (18 <= hour <= 23 or 0 <= hour <= 2):
            cong_mult = 1.45
        else:
            cong_mult = 0.85

        # --- Stage 1: Registration ---
        if priority == "Critical":
            wait_reg = random.randint(0, 2)
            reg_dur = random.randint(1, 3)
        elif patient_type == "Appointment":
            wait_reg = max(2, int(np.random.normal(5, 2) * cong_mult))
            reg_dur = random.randint(3, 5)
        else:
            wait_reg = max(3, int(np.random.normal(11, 4) * cong_mult))
            reg_dur = random.randint(3, 7)

        reg_time = arr_dt + datetime.timedelta(minutes=wait_reg + reg_dur)

        # --- Stage 2: Triage ---
        if priority == "Critical":
            wait_triage = 0
            triage_dur = random.randint(2, 4)
        elif priority == "High":
            wait_triage = max(1, int(np.random.normal(5, 2) * cong_mult))
            triage_dur = random.randint(3, 6)
        elif priority == "Medium":
            wait_triage = max(3, int(np.random.normal(12, 4) * cong_mult))
            triage_dur = random.randint(4, 7)
        else:
            wait_triage = max(5, int(np.random.normal(18, 5) * cong_mult))
            triage_dur = random.randint(4, 8)

        triage_time = reg_time + datetime.timedelta(minutes=wait_triage + triage_dur)

        # --- Stage 3: Doctor Consultation ---
        staff_ratio = s_max / max(1, staff_avail)
        base_doc_wait = {
            "Critical": random.randint(1, 5),
            "High": random.randint(8, 18),
            "Medium": random.randint(20, 48),
            "Low": random.randint(35, 70)
        }[priority]

        if dept == "Emergency":
            wait_doc = int(base_doc_wait * staff_ratio * (1.4 if is_weekend else 1.0))
            if priority == "Critical":
                wait_doc = random.randint(1, 4)
        elif dept in ["General Medicine", "Orthopedics", "Cardiology"]:
            wait_doc = int(base_doc_wait * cong_mult * staff_ratio * 1.1)
        elif dept in ["Radiology", "Laboratory", "Pharmacy"]:
            wait_doc = int(base_doc_wait * 0.6 * cong_mult)
        else:
            wait_doc = int(base_doc_wait * cong_mult)

        wait_doc = max(1, wait_doc)
        c_min, c_max = dinfo["consult_time"]
        doc_dur = random.randint(c_min, c_max)

        doc_start = triage_time + datetime.timedelta(minutes=wait_doc)
        doc_end = doc_start + datetime.timedelta(minutes=doc_dur)

        # --- Stage 4: Diagnostics ---
        diag_prob = {
            "Emergency": 0.65, "Cardiology": 0.78, "Orthopedics": 0.75,
            "Neurology": 0.60, "General Medicine": 0.45, "General Surgery": 0.60,
            "Pediatrics": 0.30, "Radiology": 1.00, "Laboratory": 1.00,
            "Pharmacy": 0.05, "ICU": 0.85, "OPD": 0.30
        }.get(dept, 0.35)

        has_diag = (random.random() < diag_prob)
        if has_diag:
            wait_diag = max(5, int(np.random.normal(22, 6) * cong_mult))
            diag_dur = random.randint(15, 38)
            diag_start = doc_end + datetime.timedelta(minutes=wait_diag)
            diag_end = diag_start + datetime.timedelta(minutes=diag_dur)
            post_diag_anchor = diag_end
        else:
            wait_diag = 0
            diag_dur = 0
            diag_start = None
            diag_end = None
            post_diag_anchor = doc_end

        # --- Stage 5: Treatment ---
        treat_prob = 0.85 if is_emerg else (0.45 if priority in ["Critical", "High"] else 0.20)
        has_treat = (random.random() < treat_prob)
        if has_treat:
            wait_treat = max(3, int(np.random.normal(9, 3)))
            treat_dur = random.randint(20, 90) if is_emerg else random.randint(15, 50)
            treat_start = post_diag_anchor + datetime.timedelta(minutes=wait_treat)
            treat_end = treat_start + datetime.timedelta(minutes=treat_dur)
            post_treat_anchor = treat_end
        else:
            wait_treat = 0
            treat_dur = 0
            treat_start = None
            treat_end = None
            post_treat_anchor = post_diag_anchor

        # --- Stage 6: Pharmacy ---
        has_pharm = (random.random() < 0.68 and dept not in ["Radiology", "Laboratory", "ICU"])
        if has_pharm:
            wait_pharm = max(4, int(np.random.normal(13, 4) * cong_mult))
            pharm_dur = random.randint(4, 10)
            pharm_start = post_treat_anchor + datetime.timedelta(minutes=wait_pharm)
            pharm_end = pharm_start + datetime.timedelta(minutes=pharm_dur)
            final_anchor = pharm_end
        else:
            wait_pharm = 0
            pharm_dur = 0
            pharm_start = None
            pharm_end = None
            final_anchor = post_treat_anchor

        # Discharge
        disch_delay = random.randint(5, 14)
        discharge_dt = final_anchor + datetime.timedelta(minutes=disch_delay)

        # Operational Metrics
        total_wait = wait_reg + wait_triage + wait_doc + wait_diag + wait_treat + wait_pharm
        los = int((discharge_dt - arr_dt).total_seconds() / 60)
        dept_util = round(float(np.clip((capacity - bed_avail) / capacity, 0.05, 0.98)), 3)
        cap_pressure = round(float(np.clip(dept_util * (s_max / max(1, staff_avail)), 0.1, 2.5)), 2)
        patient_throughput = round(float(np.clip(60.0 / max(10, los / 3.0), 0.2, 5.0)), 2)

        # Admission & Discharge Status
        if is_emerg:
            if priority == "Critical":
                adm_status = np.random.choice(["Admitted ICU", "Admitted Ward", "Transferred"], p=[0.50, 0.40, 0.10])
                disch_status = "Inpatient Admitted"
                ref_status = "Internal Transfer"
            elif priority == "High":
                adm_status = np.random.choice(["Admitted Ward", "Discharged", "Admitted ICU"], p=[0.55, 0.40, 0.05])
                disch_status = "Inpatient Admitted" if "Admitted" in adm_status else "Routine Discharge"
                ref_status = "None"
            else:
                adm_status = np.random.choice(["Discharged", "Admitted Ward", "Left Without Treatment"], p=[0.84, 0.12, 0.04])
                disch_status = "LWBS" if adm_status == "Left Without Treatment" else "Routine Discharge"
                ref_status = "None"
        else:
            if priority == "High":
                adm_status = np.random.choice(["Discharged", "Admitted Ward"], p=[0.78, 0.22])
            else:
                adm_status = np.random.choice(["Discharged", "Left Without Treatment"], p=[0.97, 0.03])
            disch_status = "LWBS" if adm_status == "Left Without Treatment" else "Routine Discharge"
            ref_status = "External Referral" if patient_type == "Referral" else "None"

        # Bottleneck Model (0-100)
        w_score = min(40.0, (wait_doc / 75.0) * 40.0)
        c_score = min(30.0, dept_util * 30.0)
        v_score = min(20.0, (cong_mult / 1.5) * 20.0)
        s_score = min(10.0, (staff_ratio / 2.0) * 10.0)
        bottleneck_score = round(float(np.clip(w_score + c_score + v_score + s_score, 5.0, 98.0)), 1)

        if bottleneck_score >= 70.0:
            bottleneck_cat = "Critical"
        elif bottleneck_score >= 50.0:
            bottleneck_cat = "High"
        elif bottleneck_score >= 35.0:
            bottleneck_cat = "Moderate"
        else:
            bottleneck_cat = "Low"

        # Controlled Anomaly Flagging
        anomaly_flag = "No"
        anomaly_type = "None"
        if arrival_date in surge_emergency_days and is_emerg:
            anomaly_flag = "Yes"
            anomaly_type = "Emergency Surge / Trauma Outbreak"
        elif arrival_date in surge_monsoon_days and dept in ["General Medicine", "Pediatrics"]:
            anomaly_flag = "Yes"
            anomaly_type = "Monsoon Epidemic Outbreak"
        elif wait_doc > 70:
            anomaly_flag = "Yes"
            anomaly_type = "Severe Queue Bottleneck"
        elif dept_util >= 0.92:
            anomaly_flag = "Yes"
            anomaly_type = "Capacity Saturation Alert"

        record = {
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Arrival_Date": arrival_date.strftime("%Y-%m-%d"),
            "Arrival_Time": arr_dt.strftime("%H:%M:%S"),
            "Arrival_DateTime": arr_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "Age": age,
            "Gender": gender,
            "Patient_Type": patient_type,
            "Priority_Level": priority,
            "Department": dept,
            "Registration_Time": reg_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Triage_Time": triage_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Doctor_Start_Time": doc_start.strftime("%Y-%m-%d %H:%M:%S"),
            "Doctor_End_Time": doc_end.strftime("%Y-%m-%d %H:%M:%S"),
            "Diagnostic_Start_Time": diag_start.strftime("%Y-%m-%d %H:%M:%S") if diag_start else "",
            "Diagnostic_End_Time": diag_end.strftime("%Y-%m-%d %H:%M:%S") if diag_end else "",
            "Treatment_Start_Time": treat_start.strftime("%Y-%m-%d %H:%M:%S") if treat_start else "",
            "Treatment_End_Time": treat_end.strftime("%Y-%m-%d %H:%M:%S") if treat_end else "",
            "Pharmacy_Start_Time": pharm_start.strftime("%Y-%m-%d %H:%M:%S") if pharm_start else "",
            "Pharmacy_End_Time": pharm_end.strftime("%Y-%m-%d %H:%M:%S") if pharm_end else "",
            "Discharge_DateTime": discharge_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "Wait_Registration": wait_reg,
            "Wait_Triage": wait_triage,
            "Wait_Doctor": wait_doc,
            "Wait_Diagnostics": wait_diag,
            "Wait_Treatment": wait_treat,
            "Wait_Pharmacy": wait_pharm,
            "Total_Waiting_Time": total_wait,
            "Treatment_Duration": treat_dur,
            "Diagnostic_Duration": diag_dur,
            "Length_of_Stay": los,
            "Department_Capacity": capacity,
            "Bed_Available": bed_avail,
            "Staff_Available": staff_avail,
            "Department_Utilization": dept_util,
            "Capacity_Pressure": cap_pressure,
            "Patient_Throughput": patient_throughput,
            "Emergency_Flag": emergency_flag,
            "Admission_Status": adm_status,
            "Discharge_Status": disch_status,
            "Referral_Status": ref_status,
            "Day_of_Week": dow,
            "Hour": hour,
            "Shift": shift,
            "Month": month,
            "Season": season,
            "Bottleneck_Score": bottleneck_score,
            "Bottleneck_Category": bottleneck_cat,
            "Anomaly_Flag": anomaly_flag,
            "Anomaly_Type": anomaly_type
        }
        records.append(record)

    df = pd.DataFrame(records)
    print(f"[3/5] Base dataset generated with {len(df)} records.")

    # ---------------------------------------------------------
    # Inject Controlled Data Quality Issues into the Raw Feed
    # ---------------------------------------------------------
    print("[4/5] Injecting controlled EHR data quality anomalies into raw feed...")
    # 1. Duplicates (~450)
    dupe_idx = np.random.choice(df.index, size=450, replace=False)
    dupes = df.loc[dupe_idx].copy()
    df_raw = pd.concat([df, dupes], ignore_index=True)

    # 2. Inconsistent Date/Time formatting (e.g. DD/MM/YYYY, ISO T)
    dt_idx = np.random.choice(df_raw.index, size=1200, replace=False)
    for i in dt_idx[:400]:
        parts = df_raw.at[i, "Arrival_Date"].split("-")
        df_raw.at[i, "Arrival_Date"] = f"{parts[2]}/{parts[1]}/{parts[0]}"
    for i in dt_idx[400:800]:
        df_raw.at[i, "Registration_Time"] = df_raw.at[i, "Registration_Time"].replace(" ", "T")

    # 3. Category Inconsistencies
    cat_idx = np.random.choice(df_raw.index, size=1400, replace=False)
    for i in cat_idx[:300]:
        if df_raw.at[i, "Department"] == "Emergency":
            df_raw.at[i, "Department"] = random.choice(["EMERGENCY", "Emerg", "ER"])
        elif df_raw.at[i, "Department"] == "Pediatrics":
            df_raw.at[i, "Department"] = "Paediatrics"
    for i in cat_idx[300:700]:
        g = df_raw.at[i, "Gender"]
        if g == "Female":
            df_raw.at[i, "Gender"] = random.choice(["F", "female"])
        elif g == "Male":
            df_raw.at[i, "Gender"] = random.choice(["M", "male"])
    for i in cat_idx[700:1100]:
        p = df_raw.at[i, "Priority_Level"]
        if p == "Critical":
            df_raw.at[i, "Priority_Level"] = random.choice(["CRITICAL", "critical"])
        elif p == "High":
            df_raw.at[i, "Priority_Level"] = "HIGH"

    # 4. Missing values
    miss_idx = np.random.choice(df_raw.index, size=600, replace=False)
    for i in miss_idx[:250]:
        df_raw.at[i, "Gender"] = ""
    for i in miss_idx[250:500]:
        df_raw.at[i, "Referral_Status"] = ""

    # 5. Negative wait times & Inverted sequences
    inv_idx = np.random.choice(df_raw.index, size=100, replace=False)
    for i in inv_idx[:35]:
        df_raw.at[i, "Wait_Doctor"] = -random.randint(5, 20)
    for i in inv_idx[35:60]:
        df_raw.at[i, "Doctor_Start_Time"] = "2025-01-01 00:00:00"

    # 6. Typographical Outliers
    for i in inv_idx[60:75]:
        df_raw.at[i, "Wait_Doctor"] = 9999
        df_raw.at[i, "Total_Waiting_Time"] = 9999

    print(f"[5/5] Final RAW dataset contains {len(df_raw)} records.")
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "hospital_patient_flow_raw.csv")
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    df_raw.to_csv(raw_path, index=False)
    print(f"-> Saved raw dataset to: {os.path.abspath(raw_path)}")
    return raw_path

if __name__ == "__main__":
    generate_dataset(30000)
