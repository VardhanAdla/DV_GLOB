"""
generate_hospital_data.py
=========================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Generates a realistic, synthetic hospital patient flow dataset representing 10 months
of hospital activity (~30,000 patient visits) across 12 departments.
Simulates realistic queue dynamics, priority rules, peak hours, staffing variations,
controlled seasonal surges, and injects controlled data-quality anomalies into RAW data.

Outputs:
    - data/raw/hospital_patient_flow_raw.csv
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

# Set fixed seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

def generate_raw_dataset(num_records=30000):
    print(f"[1/5] Initializing synthetic patient flow generation ({num_records} baseline visits)...")

    # Time frame: 2025-01-01 to 2025-10-31 (304 days)
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 10, 31)
    total_days = (end_date - start_date).days + 1

    # Departments and volume weights
    departments = [
        "Emergency", "General Medicine", "Cardiology", "Orthopedics",
        "Pediatrics", "Neurology", "Dermatology", "ENT",
        "Ophthalmology", "General Surgery", "Radiology", "Laboratory"
    ]
    dept_weights = [0.20, 0.18, 0.09, 0.10, 0.11, 0.05, 0.05, 0.05, 0.04, 0.05, 0.04, 0.04]

    # Department capacity configuration (max beds/chairs, nominal staff on shift)
    dept_config = {
        "Emergency": {"capacity": 55, "staff_range": (10, 16), "consult_time": (12, 25)},
        "General Medicine": {"capacity": 65, "staff_range": (8, 14), "consult_time": (10, 20)},
        "Cardiology": {"capacity": 30, "staff_range": (4, 8), "consult_time": (15, 30)},
        "Orthopedics": {"capacity": 35, "staff_range": (4, 8), "consult_time": (12, 25)},
        "Pediatrics": {"capacity": 40, "staff_range": (5, 9), "consult_time": (10, 22)},
        "Neurology": {"capacity": 25, "staff_range": (3, 6), "consult_time": (18, 35)},
        "Dermatology": {"capacity": 25, "staff_range": (3, 5), "consult_time": (8, 16)},
        "ENT": {"capacity": 25, "staff_range": (3, 5), "consult_time": (8, 18)},
        "Ophthalmology": {"capacity": 25, "staff_range": (3, 5), "consult_time": (10, 20)},
        "General Surgery": {"capacity": 30, "staff_range": (4, 7), "consult_time": (15, 35)},
        "Radiology": {"capacity": 30, "staff_range": (4, 8), "consult_time": (10, 25)},
        "Laboratory": {"capacity": 40, "staff_range": (5, 9), "consult_time": (5, 15)}
    }

    # Patient pools for realistic repeat visits
    num_unique_patients = int(num_records * 0.72)
    patient_pool = [f"P-{10000 + i}" for i in range(num_unique_patients)]

    # Hourly distribution curves (weights for each hour 0-23)
    # Outpatient: peaks at 09:00-12:00 and 16:00-18:00, very low at night
    outpatient_hourly_prob = np.array([
        0.005, 0.003, 0.002, 0.002, 0.005, 0.015,
        0.040, 0.075, 0.110, 0.125, 0.115, 0.095,
        0.065, 0.045, 0.055, 0.075, 0.080, 0.050,
        0.025, 0.010, 0.003, 0.002, 0.001, 0.001
    ])
    outpatient_hourly_prob /= outpatient_hourly_prob.sum()

    # Emergency: active 24/7, peak in late afternoon, evening, and night
    emergency_hourly_prob = np.array([
        0.035, 0.030, 0.025, 0.020, 0.020, 0.025,
        0.030, 0.035, 0.045, 0.050, 0.050, 0.050,
        0.045, 0.045, 0.050, 0.055, 0.060, 0.065,
        0.070, 0.070, 0.060, 0.050, 0.045, 0.040
    ])
    emergency_hourly_prob /= emergency_hourly_prob.sum()

    records = []
    print("[2/5] Simulating patient journeys with queue mechanics and shift pressures...")

    # Define seasonal surge windows
    # Surge 1: Heat wave / Emergency trauma surge in May (May 10 to May 16)
    # Surge 2: Monsoon flu / dengue outbreak in July (July 15 to July 25)
    surge_emergency_days = [datetime.date(2025, 5, d) for d in range(10, 17)]
    surge_monsoon_days = [datetime.date(2025, 7, d) for d in range(15, 26)]

    for idx in range(num_records):
        visit_id = f"V-2025-{idx + 1:05d}"
        patient_id = random.choice(patient_pool)

        # Pick date
        day_offset = random.randint(0, total_days - 1)
        arrival_date = start_date + datetime.timedelta(days=day_offset)
        dow = arrival_date.strftime("%A")
        month = arrival_date.strftime("%B")
        is_weekend = dow in ["Saturday", "Sunday"]
        day_type = "Weekend" if is_weekend else "Weekday"

        # Determine Season
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
        # On weekends, Emergency weight goes up
        if is_weekend or arrival_date in surge_emergency_days:
            curr_dept_weights = [0.32, 0.15, 0.08, 0.09, 0.09, 0.04, 0.04, 0.04, 0.03, 0.05, 0.03, 0.04]
        elif arrival_date in surge_monsoon_days:
            curr_dept_weights = [0.18, 0.26, 0.07, 0.07, 0.18, 0.04, 0.04, 0.04, 0.03, 0.04, 0.03, 0.02]
        else:
            curr_dept_weights = dept_weights

        department = np.random.choice(departments, p=curr_dept_weights)
        is_emergency_dept = (department == "Emergency")

        # Arrival hour
        if is_emergency_dept:
            hour = np.random.choice(range(24), p=emergency_hourly_prob)
        else:
            hour = np.random.choice(range(24), p=outpatient_hourly_prob)

        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        arrival_dt = datetime.datetime(arrival_date.year, arrival_date.month, arrival_date.day, hour, minute, second)

        # Demographics
        age_group = np.random.choice(
            ["0-17", "18-35", "36-50", "51-65", "65+"],
            p=[0.14, 0.27, 0.24, 0.20, 0.15]
        )
        if department == "Pediatrics":
            age_group = "0-17"

        gender = np.random.choice(["Female", "Male", "Other"], p=[0.51, 0.47, 0.02])

        # Patient Type & Priority Level
        if is_emergency_dept:
            patient_type = "Emergency"
            priority = np.random.choice(["Critical", "High", "Medium", "Low"], p=[0.16, 0.38, 0.36, 0.10])
            arrival_mode = np.random.choice(["Ambulance", "Private Vehicle", "Walk-in", "Public Transport"], p=[0.42, 0.38, 0.12, 0.08])
        else:
            patient_type = np.random.choice(
                ["Walk-in", "Appointment", "Referral", "Follow-up"],
                p=[0.45, 0.32, 0.13, 0.10]
            )
            # Outpatient priority
            if patient_type == "Appointment":
                priority = np.random.choice(["Medium", "Low"], p=[0.25, 0.75])
            else:
                priority = np.random.choice(["High", "Medium", "Low"], p=[0.12, 0.58, 0.30])
            arrival_mode = np.random.choice(["Walk-in", "Private Vehicle", "Public Transport", "Ambulance"], p=[0.48, 0.32, 0.18, 0.02])

        # Capacity, Staffing & Bed Availability
        dept_info = dept_config[department]
        capacity = dept_info["capacity"]
        min_staff, max_staff = dept_info["staff_range"]

        # Staff availability depends on shift (Night shift 22:00-06:00 has fewer staff)
        if hour in [22, 23, 0, 1, 2, 3, 4, 5]:
            staff_avail = random.randint(min_staff, max(min_staff, int(max_staff * 0.7)))
        elif 9 <= hour <= 17:
            staff_avail = random.randint(int(min_staff * 1.1), max_staff)
        else:
            staff_avail = random.randint(min_staff, max_staff)

        # Bed availability inversely proportional to department capacity pressure and surge
        base_free_beds = max(2, int(capacity * 0.25))
        if arrival_date in surge_emergency_days and is_emergency_dept:
            bed_avail = max(0, random.randint(0, 3))
            staff_avail = max(min_staff, staff_avail - 2)
        elif arrival_date in surge_monsoon_days and department in ["General Medicine", "Pediatrics"]:
            bed_avail = max(1, random.randint(1, 4))
        else:
            bed_avail = max(1, random.randint(3, base_free_beds))

        # Hourly congestion factor (higher during peak hours)
        if 9 <= hour <= 12 or 16 <= hour <= 18:
            hourly_congestion_mult = 1.35
        elif is_emergency_dept and (19 <= hour <= 23 or 0 <= hour <= 2):
            hourly_congestion_mult = 1.45
        else:
            hourly_congestion_mult = 0.85

        # -------------------------------------------------------------
        # Stage Queues and Waiting Times Simulation (in minutes)
        # -------------------------------------------------------------

        # Stage 1: Registration Wait
        # Critical patients expedited directly to triage/resuscitation
        if priority == "Critical":
            reg_wait = random.randint(0, 3)
            reg_duration = random.randint(1, 3)
        elif patient_type == "Appointment":
            reg_wait = max(2, int(np.random.normal(6, 2) * hourly_congestion_mult))
            reg_duration = random.randint(3, 6)
        else:
            reg_wait = max(3, int(np.random.normal(12, 4) * hourly_congestion_mult))
            reg_duration = random.randint(3, 8)

        reg_time = arrival_dt + datetime.timedelta(minutes=reg_wait + reg_duration)

        # Stage 2: Triage Wait & Duration
        if priority == "Critical":
            triage_wait = 0
            triage_duration = random.randint(2, 5)
        elif priority == "High":
            triage_wait = max(1, int(np.random.normal(5, 2) * hourly_congestion_mult))
            triage_duration = random.randint(3, 7)
        elif priority == "Medium":
            triage_wait = max(3, int(np.random.normal(12, 4) * hourly_congestion_mult))
            triage_duration = random.randint(4, 8)
        else:
            triage_wait = max(5, int(np.random.normal(18, 6) * hourly_congestion_mult))
            triage_duration = random.randint(4, 9)

        triage_start = reg_time + datetime.timedelta(minutes=triage_wait)
        triage_end = triage_start + datetime.timedelta(minutes=triage_duration)

        # Stage 3: Doctor Consultation Wait & Duration
        doc_queue_start = triage_end
        c_min, c_max = dept_info["consult_time"]
        consult_duration = random.randint(c_min, c_max)

        # Queuing bottleneck logic:
        # High volume + lower staff = longer queue
        staff_ratio = (max_staff / max(1, staff_avail))
        base_doc_wait = {
            "Critical": random.randint(1, 6),
            "High": random.randint(8, 20),
            "Medium": random.randint(20, 50),
            "Low": random.randint(35, 75)
        }[priority]

        # Specific departmental nuances
        if department == "Emergency":
            doc_wait = int(base_doc_wait * staff_ratio * (1.5 if is_weekend else 1.0))
            if priority == "Critical":
                doc_wait = random.randint(1, 4)
        elif department in ["General Medicine", "Orthopedics", "Cardiology"]:
            doc_wait = int(base_doc_wait * hourly_congestion_mult * staff_ratio * 1.15)
        elif department in ["Dermatology", "ENT", "Ophthalmology"]:
            doc_wait = int(base_doc_wait * 0.75 * hourly_congestion_mult)
        else:
            doc_wait = int(base_doc_wait * hourly_congestion_mult)

        doc_wait = max(1, doc_wait)
        doc_consult_start = doc_queue_start + datetime.timedelta(minutes=doc_wait)
        doc_consult_end = doc_consult_start + datetime.timedelta(minutes=consult_duration)

        # Stage 4: Diagnostics
        # Likelihood depends on department and priority
        diag_prob = {
            "Emergency": 0.65,
            "Cardiology": 0.78,
            "Orthopedics": 0.75,
            "Neurology": 0.60,
            "General Medicine": 0.45,
            "General Surgery": 0.60,
            "Pediatrics": 0.30,
            "Radiology": 1.00,
            "Laboratory": 1.00,
            "ENT": 0.20,
            "Ophthalmology": 0.25,
            "Dermatology": 0.15
        }.get(department, 0.35)

        diagnostic_required = "Yes" if random.random() < diag_prob else "No"
        if diagnostic_required == "Yes":
            diag_wait = max(5, int(np.random.normal(22, 7) * hourly_congestion_mult))
            diag_duration = random.randint(15, 40)
            diag_start = doc_consult_end + datetime.timedelta(minutes=diag_wait)
            diag_end = diag_start + datetime.timedelta(minutes=diag_duration)
            post_diag_anchor = diag_end
        else:
            diag_wait = 0
            diag_duration = 0
            diag_start = None
            diag_end = None
            post_diag_anchor = doc_consult_end

        # Stage 5: Treatment / Observation
        # Required for critical/high or surgical/emergency patients, plus random sample of others
        treat_prob = 0.85 if is_emergency_dept else (0.45 if priority in ["Critical", "High"] else 0.20)
        treatment_required = (random.random() < treat_prob)

        if treatment_required:
            treat_wait = max(3, int(np.random.normal(10, 4)))
            treat_duration = random.randint(15, 65) if not is_emergency_dept else random.randint(25, 120)
            treat_start = post_diag_anchor + datetime.timedelta(minutes=treat_wait)
            treat_end = treat_start + datetime.timedelta(minutes=treat_duration)
            post_treat_anchor = treat_end
        else:
            treat_wait = 0
            treat_duration = 0
            treat_start = post_diag_anchor
            treat_end = post_diag_anchor
            post_treat_anchor = post_diag_anchor

        # Stage 6: Pharmacy
        pharmacy_required = "Yes" if (random.random() < 0.70 and department not in ["Radiology", "Laboratory"]) else "No"
        if pharmacy_required == "Yes":
            pharm_wait = max(4, int(np.random.normal(14, 5) * hourly_congestion_mult))
            pharm_duration = random.randint(4, 12)
            pharm_start = post_treat_anchor + datetime.timedelta(minutes=pharm_wait)
            pharm_end = pharm_start + datetime.timedelta(minutes=pharm_duration)
            final_anchor = pharm_end
        else:
            pharm_wait = 0
            pharm_duration = 0
            pharm_start = None
            pharm_end = None
            final_anchor = post_treat_anchor

        # Discharge Wrap-up
        discharge_admin_delay = random.randint(5, 15)
        discharge_dt = final_anchor + datetime.timedelta(minutes=discharge_admin_delay)

        # Outcomes and Status
        if is_emergency_dept:
            if priority == "Critical":
                outcome = np.random.choice(["Admitted to ICU", "Admitted to Ward", "Transferred"], p=[0.45, 0.45, 0.10])
            elif priority == "High":
                outcome = np.random.choice(["Admitted to Ward", "Discharged Home", "Admitted to ICU", "Transferred"], p=[0.50, 0.40, 0.05, 0.05])
            else:
                outcome = np.random.choice(["Discharged Home", "Admitted to Ward", "Left Without Treatment"], p=[0.82, 0.14, 0.04])
        else:
            if priority == "High":
                outcome = np.random.choice(["Discharged Home", "Admitted to Ward"], p=[0.75, 0.25])
            else:
                outcome = np.random.choice(["Discharged Home", "Left Without Treatment"], p=[0.97, 0.03])

        patient_status = "Admitted" if "Admitted" in outcome else ("Transferred" if outcome == "Transferred" else ("LWBS" if outcome == "Left Without Treatment" else "Completed"))

        # Calculate total wait time and LOS
        total_waiting_time = reg_wait + triage_wait + doc_wait + diag_wait + treat_wait + pharm_wait
        total_los = int((discharge_dt - arrival_dt).total_seconds() / 60)

        record = {
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Arrival_Date": arrival_date.strftime("%Y-%m-%d"),
            "Arrival_Time": arrival_dt.strftime("%H:%M:%S"),
            "Day_of_Week": dow,
            "Month": month,
            "Hour": hour,
            "Department": department,
            "Patient_Type": patient_type,
            "Priority_Level": priority,
            "Age_Group": age_group,
            "Gender": gender,
            "Arrival_Mode": arrival_mode,
            "Registration_Time": reg_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Triage_Start_Time": triage_start.strftime("%Y-%m-%d %H:%M:%S"),
            "Triage_End_Time": triage_end.strftime("%Y-%m-%d %H:%M:%S"),
            "Doctor_Queue_Start": doc_queue_start.strftime("%Y-%m-%d %H:%M:%S"),
            "Doctor_Consultation_Start": doc_consult_start.strftime("%Y-%m-%d %H:%M:%S"),
            "Doctor_Consultation_End": doc_consult_end.strftime("%Y-%m-%d %H:%M:%S"),
            "Diagnostic_Required": diagnostic_required,
            "Diagnostic_Start": diag_start.strftime("%Y-%m-%d %H:%M:%S") if diag_start else "",
            "Diagnostic_End": diag_end.strftime("%Y-%m-%d %H:%M:%S") if diag_end else "",
            "Treatment_Start": treat_start.strftime("%Y-%m-%d %H:%M:%S") if treatment_required else "",
            "Treatment_End": treat_end.strftime("%Y-%m-%d %H:%M:%S") if treatment_required else "",
            "Pharmacy_Required": pharmacy_required,
            "Pharmacy_Start": pharm_start.strftime("%Y-%m-%d %H:%M:%S") if pharm_start else "",
            "Pharmacy_End": pharm_end.strftime("%Y-%m-%d %H:%M:%S") if pharm_end else "",
            "Discharge_Time": discharge_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "Total_Waiting_Time": total_waiting_time,
            "Registration_Wait_Time": reg_wait,
            "Triage_Wait_Time": triage_wait,
            "Doctor_Wait_Time": doc_wait,
            "Diagnostic_Wait_Time": diag_wait,
            "Treatment_Wait_Time": treat_wait,
            "Pharmacy_Wait_Time": pharm_wait,
            "Total_Length_of_Stay": total_los,
            "Patient_Status": patient_status,
            "Outcome_Category": outcome,
            "Department_Capacity": capacity,
            "Staff_Availability": staff_avail,
            "Bed_Availability": bed_avail,
            "Day_Type": day_type,
            "Season": season
        }
        records.append(record)

    df = pd.DataFrame(records)
    print(f"[3/5] Base dataset generated with {len(df)} rows.")

    # -------------------------------------------------------------
    # Inject Controlled Data Quality Issues into the RAW Dataset
    # -------------------------------------------------------------
    print("[4/5] Injecting controlled real-world data quality anomalies into RAW dataset...")

    # 1. Duplicates (~450 duplicate rows)
    num_dupes = 450
    dupe_indices = np.random.choice(df.index, size=num_dupes, replace=False)
    dupes = df.loc[dupe_indices].copy()
    df_raw = pd.concat([df, dupes], ignore_index=True)

    # 2. Inconsistent Date/Time Formats (e.g. DD/MM/YYYY or YYYY/MM/DD, ISO with T)
    date_formats_idx = np.random.choice(df_raw.index, size=1200, replace=False)
    for i in date_formats_idx[:400]:
        val = df_raw.at[i, "Arrival_Date"]
        # Convert YYYY-MM-DD to DD/MM/YYYY
        p = val.split("-")
        df_raw.at[i, "Arrival_Date"] = f"{p[2]}/{p[1]}/{p[0]}"
    for i in date_formats_idx[400:800]:
        val = df_raw.at[i, "Arrival_Date"]
        p = val.split("-") if "-" in val else val.split("/")
        df_raw.at[i, "Arrival_Date"] = f"{p[0]}/{p[1]}/{p[2]}"
    for i in date_formats_idx[800:]:
        val = df_raw.at[i, "Registration_Time"]
        df_raw.at[i, "Registration_Time"] = val.replace(" ", "T")

    # 3. Category Inconsistencies
    cat_indices = np.random.choice(df_raw.index, size=1500, replace=False)
    # Department variations
    for i in cat_indices[:300]:
        if df_raw.at[i, "Department"] == "Emergency":
            df_raw.at[i, "Department"] = random.choice(["EMERGENCY", "Emerg", "ER"])
        elif df_raw.at[i, "Department"] == "Pediatrics":
            df_raw.at[i, "Department"] = "Paediatrics"
    # Gender variations
    for i in cat_indices[300:700]:
        g = df_raw.at[i, "Gender"]
        if g == "Female":
            df_raw.at[i, "Gender"] = random.choice(["F", "female"])
        elif g == "Male":
            df_raw.at[i, "Gender"] = random.choice(["M", "male"])
    # Priority variations
    for i in cat_indices[700:1100]:
        p = df_raw.at[i, "Priority_Level"]
        if p == "Critical":
            df_raw.at[i, "Priority_Level"] = random.choice(["CRITICAL", "critical"])
        elif p == "High":
            df_raw.at[i, "Priority_Level"] = "HIGH"

    # 4. Missing Values (simulate unrecorded fields)
    missing_indices = np.random.choice(df_raw.index, size=800, replace=False)
    for i in missing_indices[:250]:
        df_raw.at[i, "Arrival_Mode"] = ""  # Missing arrival mode
    for i in missing_indices[250:500]:
        df_raw.at[i, "Age_Group"] = ""      # Blank age group
    for i in missing_indices[500:750]:
        if df_raw.at[i, "Diagnostic_Required"] == "No":
            df_raw.at[i, "Diagnostic_Wait_Time"] = np.nan  # NaN representation
        else:
            df_raw.at[i, "Triage_End_Time"] = ""

    # 5. Invalid values / Negative waiting times (clock desync)
    invalid_indices = np.random.choice(df_raw.index, size=120, replace=False)
    for i in invalid_indices[:40]:
        df_raw.at[i, "Doctor_Wait_Time"] = -random.randint(5, 25)
    for i in invalid_indices[40:70]:
        df_raw.at[i, "Registration_Wait_Time"] = -random.randint(2, 10)

    # 6. Impossible sequence (consultation before triage)
    for i in invalid_indices[70:95]:
        orig_triage = df_raw.at[i, "Triage_Start_Time"]
        df_raw.at[i, "Doctor_Consultation_Start"] = "2025-01-01 00:00:00"  # corrupted sequence

    # 7. Extreme Outliers (logging glitch: 9999 or 850 minutes wait)
    for i in invalid_indices[95:110]:
        df_raw.at[i, "Doctor_Wait_Time"] = random.choice([9999, 8888, 1250])
        df_raw.at[i, "Total_Waiting_Time"] = 9999

    print(f"[5/5] Final RAW dataset prepared with {len(df_raw)} records (including anomalies).")

    # Save RAW dataset
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    raw_path = os.path.join(output_dir, "hospital_patient_flow_raw.csv")
    df_raw.to_csv(raw_path, index=False)
    print(f"-> Successfully saved raw dataset to: {os.path.abspath(raw_path)}")
    return raw_path

if __name__ == "__main__":
    generate_raw_dataset(30000)
