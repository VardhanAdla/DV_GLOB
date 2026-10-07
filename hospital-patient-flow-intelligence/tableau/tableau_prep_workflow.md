# Tableau Prep Builder ETL Workflow Guide

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  
**ETL Architecture:** 8-Stage Visual Data Pipeline  
**Execution Environment Notice:** In accordance with project instructions, Tableau Prep Builder is not executed via headless command-line in this environment. The exact, click-by-click workflow instructions below enable 100% replication inside Tableau Prep Builder.

---

```
                       TABLEAU PREP ETL PIPELINE
+-----------------------------------------------------------------------+
|  [Step 1: Input]            hospital_patient_flow_raw.csv             |
|                                     |                                 |
|  [Step 2: Clean 1]          Remove Duplicate Visit IDs                |
|                                     |                                 |
|  [Step 3: Standardize]      Canonical Category Grouping (Dept, Gender)|
|                                     |                                 |
|  [Step 4: Impute]           Domain Null Replacement (Age, Mode, Diag) |
|                                     |                                 |
|  [Step 5: Parse Dates]      Multi-Format Date & Timestamp Resolution  |
|                                     |                                 |
|  [Step 6: Sequence Audit]   Chronological Inversion & Negative Fixes  |
|                                     |                                 |
|  [Step 7: Calculations]     Bottleneck Score & Pressure Metrics       |
|                                     |                                 |
|  [Step 8: Output]           hospital_patient_flow_clean.csv / .hyper  |
+-----------------------------------------------------------------------+
```

---

## Step 1: Input Step (`Raw Hospital Feed`)
1. Open **Tableau Prep Builder**.
2. Click **Connect to Data** -> Select **Text File (.csv)**.
3. Browse and select: `data/raw/hospital_patient_flow_raw.csv`.
4. In the **Input Pane**:
   * Verify **Text file settings**:
     * Field separator: `Comma`
     * Text qualifier: `Automatic` / `"`
     * Character set: `UTF-8`
   * Confirm that 41 fields are detected and the preview displays records.

---

## Step 2: Cleaning Step 1 - Deduplication (`Deduplicate Visits`)
1. Click the `+` icon next to the Input Step and select **Clean Step**. Rename it to `Deduplicate Visits`.
2. In the profile card for **Visit_ID**:
   * Click the three dots `...` on the `Visit_ID` card.
   * Select **Identify Duplicate Values** or create an **Aggregate Step**:
     * **Grouped Fields:** `Visit_ID`
     * **Aggregated Fields:** All other fields using `First` / `Minimum`.
   * *Alternative (Clean Step method):* Create calculated field `[Row_Num]`:
     ```tableau
     { PARTITION [Visit_ID] : { ORDERBY [Arrival_Date] ASC : ROW_NUMBER() } }
     ```
     * Add Filter: `[Row_Num] = 1`.
     * Remove the helper field `[Row_Num]`.
3. Verify that the 450 duplicate rows are filtered, bringing row count from 30,450 to 30,000.

---

## Step 3: Cleaning Step 2 - Categorical Standardization (`Standardize Domains`)
1. Add a **Clean Step** named `Standardize Domains`.
2. **Department Standardization:**
   * Select the **Department** card.
   * Click **Group Values** -> **Manual Selection**:
     * Group `EMERGENCY`, `Emerg`, `ER` under `Emergency`.
     * Group `Paediatrics` under `Pediatrics`.
3. **Gender Standardization:**
   * Select the **Gender** card.
   * Group `F`, `female` under `Female`.
   * Group `M`, `male` under `Male`.
4. **Priority Level Standardization:**
   * Select the **Priority_Level** card.
   * Group `CRITICAL`, `critical` under `Critical`.
   * Group `HIGH`, `high` under `High`.
   * Group `MEDIUM`, `medium` under `Medium`.
   * Group `LOW`, `low` under `Low`.

---

## Step 4: Cleaning Step 3 - Null Handling & Imputation (`Impute Values`)
1. Add a **Clean Step** named `Impute Values`.
2. **Age_Group Imputation:**
   * Click `...` on `Age_Group` -> **Create Calculated Field** -> Name: `Age_Group`:
     ```tableau
     IF ISNULL([Age_Group]) OR TRIM([Age_Group]) = '' THEN
         IF [Department] = 'Pediatrics' THEN '0-17'
         ELSE '18-35'
         END
     ELSE [Age_Group]
     END
     ```
3. **Arrival_Mode Imputation:**
   * Create Calculated Field -> Name: `Arrival_Mode`:
     ```tableau
     IF ISNULL([Arrival_Mode]) OR TRIM([Arrival_Mode]) = '' THEN
         IF [Department] = 'Emergency' THEN 'Ambulance'
         ELSE 'Walk-in'
         END
     ELSE [Arrival_Mode]
     END
     ```
4. **Diagnostic Wait Imputation:**
   * In `Diagnostic_Wait_Time` card: Click `...` -> **Filter** / **Replace Values**:
     * Replace `Null` with `0`.

---

## Step 5: Cleaning Step 4 - Date Parsing & Normalization (`Normalize Timestamps`)
1. Add a **Clean Step** named `Normalize Timestamps`.
2. Change data type of `Arrival_Date`:
   * Click data type icon (`Abc`) on `Arrival_Date` -> Change to **Date**.
   * Tableau Prep automatically interprets `%Y-%m-%d`, `%d/%m/%Y`, and `%Y/%m/%d`.
3. For each milestone timestamp (`Registration_Time`, `Triage_Start_Time`, `Triage_End_Time`, `Doctor_Consultation_Start`, `Doctor_Consultation_End`, `Diagnostic_Start`, `Diagnostic_End`, `Treatment_Start`, `Treatment_End`, `Pharmacy_Start`, `Pharmacy_End`, `Discharge_Time`):
   * Replace `T` character with space ` ` using `REPLACE([Timestamp_Col], 'T', ' ')`.
   * Change data type to **Date & Time**.

---

## Step 6: Cleaning Step 5 - Chronological Audit & Negative Wait Reconcile (`Sequence Audit`)
1. Add a **Clean Step** named `Sequence Audit`.
2. **Negative Doctor Wait Fix:**
   * Create calculated field overriding `Doctor_Wait_Time`:
     ```tableau
     IF [Doctor_Wait_Time] < 0 THEN
         CASE [Priority_Level]
             WHEN 'Critical' THEN 3
             WHEN 'High' THEN 14
             WHEN 'Medium' THEN 32
             WHEN 'Low' THEN 48
         END
     ELSEIF [Doctor_Wait_Time] > 500 THEN 120
     ELSE [Doctor_Wait_Time]
     END
     ```
3. **Negative Registration Wait Fix:**
   * Create calculated field overriding `Registration_Wait_Time`:
     ```tableau
     IF [Registration_Wait_Time] < 0 THEN 8
     ELSE [Registration_Wait_Time]
     END
     ```
4. **Chronological Sequence Adjustment:**
   * Recalculate `Doctor_Consultation_Start` where consultation was stamped earlier than triage:
     ```tableau
     IF [Doctor_Consultation_Start] < [Triage_Start_Time] THEN
         DATEADD('minute', INT([Doctor_Wait_Time]), [Triage_End_Time])
     ELSE [Doctor_Consultation_Start]
     END
     ```

---

## Step 7: Cleaning Step 6 - Calculated Operational Fields (`Feature Engineering`)
1. Add a **Clean Step** named `Feature Engineering`.
2. **Recompute Total Waiting Time:**
   ```tableau
   ZN([Registration_Wait_Time]) + ZN([Triage_Wait_Time]) + ZN([Doctor_Wait_Time]) +
   ZN([Diagnostic_Wait_Time]) + ZN([Treatment_Wait_Time]) + ZN([Pharmacy_Wait_Time])
   ```
3. **Bed Occupancy Rate:**
   ```tableau
   ROUND(([Department_Capacity] - [Bed_Availability]) / [Department_Capacity], 3)
   ```
4. **Waiting Time Category:**
   ```tableau
   IF [Total_Waiting_Time] < 30 THEN 'Low Wait (<30m)'
   ELSEIF [Total_Waiting_Time] <= 60 THEN 'Moderate Wait (30-60m)'
   ELSEIF [Total_Waiting_Time] <= 90 THEN 'High Wait (60-90m)'
   ELSE 'Severe Delay (>90m)'
   END
   ```
5. **Bottleneck Score:**
   ```tableau
   ROUND(
       MIN(40.0, ([Doctor_Wait_Time] / 75.0) * 40.0) +
       ([Bed_Occupancy_Rate] * 35.0) +
       MIN(25.0, ([Department_Capacity] / ([Staff_Availability] * 4.0)) * 12.5),
       1
   )
   ```
6. **Bottleneck Category:**
   ```tableau
   IF [Bottleneck_Score] >= 70.0 THEN 'Severe Bottleneck'
   ELSEIF [Bottleneck_Score] >= 50.0 THEN 'Moderate Congestion'
   ELSEIF [Bottleneck_Score] >= 35.0 THEN 'Manageable Flow'
   ELSE 'Optimal Flow'
   END
   ```

---

## Step 8: Output Step (`Publish Clean Dataset`)
1. Click `+` on the final Clean Step -> Select **Add Output**.
2. Set Output configurations:
   * **Save to file:**
     * File format: **Delimited text (.csv)** (and/or **Tableau Data Extract (.hyper)**).
     * Output location: `data/processed/hospital_patient_flow_clean.csv`.
   * **Full refresh** option selected.
3. Click **Run Flow**.
4. Verification: Check that the flow outputs 30,000 clean records with zero errors.
