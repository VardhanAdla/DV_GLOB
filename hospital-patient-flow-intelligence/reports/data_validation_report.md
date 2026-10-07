# Automated Data Quality & Validation Report
**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  
**Execution Timestamp:** 2026-10-01 00:25:24  

---

## 1. Quality Matrix: Raw Ingestion vs Clean Processed

| Quality Metric | Raw Dataset (hospital_patient_flow_raw.csv) | Clean Dataset (hospital_patient_flow_clean.csv) | Status |
| :--- | :---: | :---: | :---: |
| **Total Record Count** | 30,450 | 30,000 | 450 Duplicates Removed |
| **Duplicate Visit IDs** | 450 | 0 | **100% Resolved** |
| **Department Domain Errors** | 4 (Emerg, Paediatrics, EMERGENCY, ER) | 0 | **100% Harmonized** |
| **Priority Level Domain Errors**| 3 (HIGH, critical, CRITICAL) | 0 | **100% Standardized** |
| **Negative Waiting Times** | 35 | 0 | **100% Reconciled** |
| **Consultation Before Triage** | 25 | 0 | **100% Corrected** |
| **Discharge Before Arrival** | 0 | 0 | **Zero Violations** |
| **Extreme Outliers (>500m)** | 15 | 0 | **Winsorized at P99 (120m)** |

---

## 2. Tableau Certification
The clean dataset satisfies all Tableau Desktop and Streamlit ingestion requirements:
* Strong entity integrity on primary key `Visit_ID`.
* Zero null values across critical dimensions.
* Validated chronological stage sequencing.
