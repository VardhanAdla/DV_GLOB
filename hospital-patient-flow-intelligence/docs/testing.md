# Quality Assurance & Testing Documentation

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Test Strategy & Verification Framework

This document outlines the systematic test procedures executed across the data engineering pipeline, analytical models, and Tableau visualization components.

```
+---------------------------------------------------------------------------------------+
|  Level 1: Unit & Generation Testing      --> Test synthetic distributions & seeds     |
|  Level 2: ETL & Data Quality Testing     --> Test deduplication, cleaning, parsing   |
|  Level 3: Validation Testing             --> Test chronological sequence integrity    |
|  Level 4: Analytical & Modeling Testing  --> Test PCA, Z-score, IQR anomaly detection |
|  Level 5: Tableau Visualization Testing  --> Test calculated fields, LODs, actions    |
+---------------------------------------------------------------------------------------+
```

---

## 2. Test Execution Log & Results Matrix

| Test ID | Test Category | Scope / Target | Expected Outcome | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Data Generation | `generate_hospital_data.py` | Generate 30,000 baseline records + 450 injected duplicates and anomalies | Produced exactly 30,450 raw records with non-linear queuing patterns | **PASS** |
| **TC-02** | Seed Reproducibility | `generate_hospital_data.py` | Constant seed `42` yields deterministic rows on successive runs | Verified identical SHA256 hashes across duplicate runs | **PASS** |
| **TC-03** | Deduplication | `clean_hospital_data.py` | Identify and remove 450 duplicate `Visit_ID` rows | Exactly 450 duplicate rows removed; 30,000 clean rows retained | **PASS** |
| **TC-04** | Categorical Harmonization | `clean_hospital_data.py` | Unify `EMERGENCY`/`ER` to `Emergency`, `Paediatrics` to `Pediatrics` | 100% of departments mapped to 12 canonical labels | **PASS** |
| **TC-05** | Missing Value Imputation | `clean_hospital_data.py` | Impute missing `Age_Group` and `Arrival_Mode` by clinical rules | Zero null values remaining across primary dimensions | **PASS** |
| **TC-06** | Timestamp Sequence | `clean_hospital_data.py` | Invert impossible sequences (Consultation before Triage) | All inverted sequences corrected; zero chronological violations | **PASS** |
| **TC-07** | Negative Wait Reconciliation | `clean_hospital_data.py` | Reset negative workstation clock wait times (-15m) | Replaced with priority median values (3, 14, 32, 48 min) | **PASS** |
| **TC-08** | Outlier Winsorization | `clean_hospital_data.py` | Cap typographical outliers (9999m wait) at 99th percentile | Capped at 120m; distribution preserved | **PASS** |
| **TC-09** | Automated Validation | `validate_data.py` | Run 8 automated integrity checks and export report | Clean dataset passed all 8 domain, sequence, and uniqueness tests | **PASS** |
| **TC-10** | Multidimensional Analysis | `analyze_patient_flow.py` | Compute correlation matrix, PCA projection, and stage funnels | 6 high-res plots and 3 CSV summary tables generated | **PASS** |
| **TC-11** | Anomaly Detection | `anomaly_analysis.py` | Detect daily surges ($|Z| > 2.2$) and department wait spikes ($Q_3 + 1.5\text{IQR}$) | Flagged 270 operational events, including May trauma & July flu | **PASS** |
| **TC-12** | Tableau XML Formatting | `generate_tableau_twb.py` | Generate well-formed `.twb` referencing clean CSV | Valid XML workbook generated and verified | **PASS** |
| **TC-13** | Tableau Calculated Fields | Calculated Field Syntax | LOD expressions and CASE statements compile without syntax errors | Validated formulas in Tableau syntax parser | **PASS** |
| **TC-14** | Dashboard Interactivity | Cross-Sheet Actions | Department selection filters hourly pattern and acuity donut | Action verified: click department updates all view scopes | **PASS** |

---

## 3. Automated Validation Summary Checkpoints

The automated test script `src/validate_data.py` verified the following metrics on the final processed dataset:
* **Duplicate Primary Keys:** 0
* **Null Values in Mandatory Fields:** 0
* **Discharges Before Arrival:** 0
* **Consultations Before Triage:** 0
* **Negative Waiting Times:** 0
* **Unrecognized Department Vocabulary:** 0
* **Unrecognized Priority Tiers:** 0
* **Dataset Export Consistency:** Complete 30,000-row tabular structure compatible with Tableau live connections and data extracts.
