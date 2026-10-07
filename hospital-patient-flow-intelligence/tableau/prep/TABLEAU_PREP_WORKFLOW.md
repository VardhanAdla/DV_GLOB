# Tableau Prep Builder ETL Workflow Guide

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Complete ETL Visual Architecture

```
[ Step 1: Input ] --> hospital_patient_flow_raw.csv (30,450 records)
         │
[ Step 2: Clean 1 ] -> Deduplicate Visit_ID (Remove 450 duplicate rows)
         │
[ Step 3: Clean 2 ] -> Standardize Categories (Department, Gender, Priority)
         │
[ Step 4: Clean 3 ] -> Missing Value Imputation (Gender, Referral_Status)
         │
[ Step 5: Clean 4 ] -> Normalize Dates & Delimiters (Replace 'T' with space, cast to Date/Time)
         │
[ Step 6: Clean 5 ] -> Reconcile Sequence Inversions & Negative Waits (Re-anchor doctor consult)
         │
[ Step 7: Clean 6 ] -> Calculate Operational Fields (Bottleneck Score, Utilization, Categories)
         │
[ Step 8: Output  ] -> hospital_patient_flow_tableau.csv / .hyper extract
```

---

## 2. Step-by-Step Instructions Inside Tableau Prep Builder

### Step 1: Input Step (`Ingest Raw Hospital Data`)
1. Click **Connect to Data** -> **Text file**.
2. Select: `data/raw/hospital_patient_flow_raw.csv`.
3. Verify settings: Comma delimited, text qualifier `"`, UTF-8 encoding.

### Step 2: Clean Step 1 - Deduplication (`Deduplicate Encounters`)
1. Add a **Clean Step** named `Deduplicate Encounters`.
2. Create calculated field `[Row_Number]`:
   ```tableau
   { PARTITION [Visit_ID] : { ORDERBY [Arrival_Date] ASC : ROW_NUMBER() } }
   ```
3. Add a filter: `[Row_Number] = 1`.
4. Right-click and delete `[Row_Number]`. Row count updates from 30,450 to 30,000.

### Step 3: Clean Step 2 - Domain Standardization (`Standardize Categorical Fields`)
1. Select the **Department** profile card:
   * Group `EMERGENCY`, `Emerg`, `ER` into `Emergency`.
   * Group `Paediatrics` into `Pediatrics`.
2. Select the **Gender** profile card:
   * Group `F`, `female` into `Female`.
   * Group `M`, `male` into `Male`.
3. Select the **Priority_Level** card:
   * Group `CRITICAL`, `critical` into `Critical`.
   * Group `HIGH`, `high` into `High`.
   * Group `MEDIUM`, `medium` into `Medium`.
   * Group `LOW`, `low` into `Low`.

### Step 4: Clean Step 3 - Null Imputation (`Impute Missing Values`)
1. Create calculated field on `Gender`:
   ```tableau
   IF ISNULL([Gender]) OR TRIM([Gender]) = '' THEN 'Female' ELSE [Gender] END
   ```
2. Create calculated field on `Referral_Status`:
   ```tableau
   IF ISNULL([Referral_Status]) OR TRIM([Referral_Status]) = '' THEN 'None' ELSE [Referral_Status] END
   ```

### Step 5: Clean Step 4 - Date & Timestamp Normalization (`Normalize Timestamps`)
1. Convert `Arrival_Date` to data type **Date**.
2. For all timestamp fields (`Arrival_DateTime`, `Registration_Time`, `Triage_Time`, `Doctor_Start_Time`, `Doctor_End_Time`, `Discharge_DateTime`):
   * Replace `T` character with space: `REPLACE([Timestamp_Field], 'T', ' ')`
   * Convert data type to **Date & Time**.

### Step 6: Clean Step 5 - Negative Waits & Sequence Repairs (`Repair Queues`)
1. Fix negative doctor waits:
   ```tableau
   IF [Wait_Doctor] < 0 THEN
       CASE [Priority_Level]
           WHEN 'Critical' THEN 3
           WHEN 'High' THEN 14
           WHEN 'Medium' THEN 32
           WHEN 'Low' THEN 48
       END
   ELSEIF [Wait_Doctor] > 500 THEN 120
   ELSE [Wait_Doctor]
   END
   ```
2. Fix inverted consultation sequences:
   ```tableau
   IF [Doctor_Start_Time] < [Triage_Time] THEN
       DATEADD('minute', INT([Wait_Doctor]), [Triage_Time])
   ELSE [Doctor_Start_Time]
   END
   ```

### Step 7: Clean Step 6 - Calculated Operational Metrics (`Feature Engineering`)
1. **Total Waiting Time:**
   ```tableau
   ZN([Wait_Registration]) + ZN([Wait_Triage]) + ZN([Wait_Doctor]) + ZN([Wait_Diagnostics]) + ZN([Wait_Treatment]) + ZN([Wait_Pharmacy])
   ```
2. **Bottleneck Score:**
   ```tableau
   ROUND(
       MIN(40.0, ([Wait_Doctor] / 75.0) * 40.0) +
       ([Department_Utilization] * 30.0) +
       MIN(20.0, ([Capacity_Pressure] / 2.0) * 20.0) +
       MIN(10.0, ([Department_Capacity] / ([Staff_Available] * 5.0)) * 5.0),
       1
   )
   ```
3. **Bottleneck Category:**
   ```tableau
   IF [Bottleneck_Score] >= 70.0 THEN 'Critical'
   ELSEIF [Bottleneck_Score] >= 50.0 THEN 'High'
   ELSEIF [Bottleneck_Score] >= 35.0 THEN 'Moderate'
   ELSE 'Low'
   END
   ```

### Step 8: Output Step (`Publish Clean Dataset`)
1. Add an **Output Step**.
2. Save to file: `tableau/data/hospital_patient_flow_tableau.csv` and/or Tableau Data Extract (`.hyper`).
3. Click **Run Flow**. Verify that exactly 30,000 clean records are generated.
