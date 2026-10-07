# Tableau Prep Builder Workflow Documentation

Please refer to [`tableau/tableau_prep_workflow.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/tableau_prep_workflow.md) for the full 8-stage interactive ETL pipeline instructions.

### Summary of Stages:
1. **Input Step:** Ingestion of `data/raw/hospital_patient_flow_raw.csv`.
2. **Deduplication:** Filtering 450 duplicate rows via primary key `Visit_ID`.
3. **Categorical Standardization:** Harmonizing casing and department acronyms (`EMERGENCY` -> `Emergency`, `Paediatrics` -> `Pediatrics`).
4. **Imputation:** Clinical rule-based filling of missing demographic age groups, transit modes, and diagnostic wait times.
5. **Timestamp Normalization:** Resolving multi-format date stamps and ISO `T` delimiters.
6. **Chronological Inversion Fix:** Re-anchoring out-of-order sequence timestamps.
7. **Feature Engineering:** Deriving `Bottleneck_Score`, `Bed_Occupancy_Rate`, and `Waiting_Time_Category`.
8. **Output Step:** Exporting verified 30,000-record dataset to `data/processed/hospital_patient_flow_clean.csv`.
