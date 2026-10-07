# Data Dictionary: Hospital Patient Flow Intelligence

**Course Code:** GR24A3144 (Data Visualization Lab)  
**Dataset Reference:** `data/processed/hospital_patient_flow_clean.csv`  
**Record Count:** 30,000 distinct patient encounters  
**Observation Window:** 2025-01-01 to 2025-10-31  

---

## Attribute Specifications

| Field Name | Data Type | Nullable | Domain / Example Values | Description & Role |
| :--- | :--- | :---: | :--- | :--- |
| `Patient_ID` | String | No | `P-10000` to `P-31599` | Unique identifier for an individual patient across recurrent visits. |
| `Visit_ID` | String | No | `V-2025-00001` to `V-2025-30000` | Primary key uniquely identifying an encounter episode of care. |
| `Arrival_Date` | Date | No | `2025-01-01` to `2025-10-31` | Calendar date of patient arrival at hospital. |
| `Arrival_Time` | String | No | `00:00:00` to `23:59:59` | Clock time of initial patient presentation. |
| `Day_of_Week` | String | No | `Monday` to `Sunday` | Calendar day of week derived from arrival date. |
| `Month` | String | No | `January` to `October` | Calendar month of visit for seasonal modeling. |
| `Hour` | Integer | No | `0` to `23` | Binned arrival hour in 24-hour notation. |
| `Department` | String | No | 12 Clinical Units (Emergency, General Medicine, Cardiology, etc.) | Clinical service unit managing the encounter. |
| `Patient_Type` | String | No | `Emergency`, `Walk-in`, `Appointment`, `Referral`, `Follow-up` | Mode of access to healthcare service. |
| `Priority_Level` | String | No | `Critical`, `High`, `Medium`, `Low` | Clinical triage acuity level assigned by triage nurse. |
| `Age_Group` | String | No | `0-17`, `18-35`, `36-50`, `51-65`, `65+` | Demographic age bracket. |
| `Gender` | String | No | `Female`, `Male`, `Other` | Patient demographic gender classification. |
| `Arrival_Mode` | String | No | `Ambulance`, `Walk-in`, `Private Vehicle`, `Public Transport` | Physical transport method to facility. |
| `Registration_Time` | DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp when administrative check-in concluded. |
| `Triage_Start_Time` | DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp when clinical nurse triage began. |
| `Triage_End_Time` | DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp when triage assessment completed. |
| `Doctor_Queue_Start`| DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp patient queued for physician examination. |
| `Doctor_Consultation_Start` | DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp physician examination started. |
| `Doctor_Consultation_End` | DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp physician examination concluded. |
| `Diagnostic_Required` | String | No | `Yes`, `No` | Flag indicating whether lab or imaging was ordered. |
| `Diagnostic_Start` | DateTime | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp diagnostic imaging/testing began. |
| `Diagnostic_End` | DateTime | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp diagnostic test completed. |
| `Treatment_Start` | DateTime | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp medical therapy/procedure started. |
| `Treatment_End` | DateTime | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp medical therapy/procedure completed. |
| `Pharmacy_Required` | String | No | `Yes`, `No` | Flag indicating outpatient prescription ordered. |
| `Pharmacy_Start` | DateTime | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp prescription queued at dispensary. |
| `Pharmacy_End` | DateTime | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp prescription dispensed to patient. |
| `Discharge_Time` | DateTime | No | `YYYY-MM-DD HH:MM:SS` | Timestamp patient exited hospital care unit. |
| `Total_Waiting_Time` | Integer | No | `0` to `300+` min | Cumulative sum of all queue delays across stages. |
| `Registration_Wait_Time` | Integer | No | `0` to `60` min | Elapsed wait duration prior to registration. |
| `Triage_Wait_Time` | Integer | No | `0` to `45` min | Elapsed wait duration prior to triage. |
| `Doctor_Wait_Time` | Integer | No | `0` to `180` min | Elapsed wait duration prior to doctor examination. |
| `Diagnostic_Wait_Time` | Integer | No | `0` to `120` min | Elapsed wait duration prior to diagnostic testing. |
| `Treatment_Wait_Time` | Integer | No | `0` to `90` min | Elapsed wait duration prior to acute therapy. |
| `Pharmacy_Wait_Time` | Integer | No | `0` to `60` min | Elapsed wait duration prior to pharmacy pickup. |
| `Total_Length_of_Stay` | Integer | No | `15` to `480+` min | Total encounter duration from entry to discharge. |
| `Patient_Status` | String | No | `Completed`, `Admitted`, `Transferred`, `LWBS` | Disposition status of episode. |
| `Outcome_Category` | String | No | `Discharged Home`, `Admitted to Ward`, `Admitted to ICU`, `Transferred`, `Left Without Treatment` | Administrative disposition category. |
| `Department_Capacity`| Integer | No | `20` to `65` beds/chairs | Maximum concurrent bed capacity of the unit. |
| `Staff_Availability` | Integer | No | `3` to `16` clinical staff | Active clinical staff on duty during visit shift. |
| `Bed_Availability` | Integer | No | `0` to `25` beds | Free unallocated beds at time of arrival. |
| `Day_Type` | String | No | `Weekday`, `Weekend`, `Holiday` | Operational calendar classification. |
| `Season` | String | No | `Winter`, `Spring`, `Summer`, `Monsoon`, `Autumn` | Climate season of arrival. |
| `Waiting_Time_Category` | String | No | `<30m`, `30-60m`, `60-90m`, `>90m` | Operational binned delay tier. |
| `Bed_Occupancy_Rate` | Float | No | `0.000` to `1.000` | Proportion of beds in active clinical use. |
| `Bottleneck_Score` | Float | No | `0.0` to `100.0` | Composite operational bottleneck score. |
| `Bottleneck_Category` | String | No | `Optimal Flow`, `Manageable Flow`, `Moderate Congestion`, `Severe Bottleneck` | Threshold tier for bottleneck score. |
