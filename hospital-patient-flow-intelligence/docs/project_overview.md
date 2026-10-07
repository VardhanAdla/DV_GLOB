# Hospital Patient Flow Intelligence: Project Overview

**Project Title:** Hospital Patient Flow Intelligence  
**Subtitle:** Interactive Tableau-Based Patient Flow, Bottleneck and Waiting-Time Analytics System  
**Academic Context:** College GLOB Project, III Year I Semester  
**Course Name:** Data Visualization Lab  
**Course Code:** GR24A3144  

---

## 1. Executive Summary

Hospitals are complex, multi-stage stochastic service environments where patient care requires seamless coordination across registration, clinical triage, doctor consultation, diagnostic testing (radiology and pathology), therapeutic interventions, and pharmacy dispensing. When any stage in this sequence becomes saturated or under-resourced, downstream queues back up rapidly, ballooning waiting times, driving bed shortages, degrading clinical responsiveness, and increasing the rate of patients who Leave Without Being Seen (LWBS).

The **Hospital Patient Flow Intelligence** project provides a comprehensive, interactive business intelligence and decision-support system implemented primarily using **Tableau Desktop**, complemented by an automated **Python** data engineering and analytical pipeline. 

By modeling and analyzing 30,000 anonymized patient visits over a 10-month evaluation period across 12 distinct hospital departments, this project moves far beyond static hospital administrative reporting. It empowers healthcare administrators, triage supervisors, and bed managers to diagnose the root operational causes of patient congestion, benchmark waiting times against clinical SLAs, visualize multi-stage care journeys, and proactively simulate capacity interventions.

---

## 2. Core Clinical & Operational Questions Answered

1. **Daily Intake Rhythms:** How many patients present to the facility each day, and what temporal variances distinguish weekdays from weekends?
2. **Diurnal Peaks:** What are the acute peak presentation hours across general outpatient care versus 24/7 emergency medicine?
3. **Departmental Volumes:** Which clinical departments carry the highest volume burdens, and how do their intake patterns differ?
4. **Queue Durations:** Which departments suffer the longest waiting times, and what proportion of encounter time is non-value-added waiting?
5. **Bottleneck Isolation:** At which exact stages (Registration, Triage, Doctor, Diagnostics, Treatment, Pharmacy) do queues stagnate?
6. **Acuity Stratification:** How effectively does priority triage (Critical, High, Medium, Low) protect acute patients from outpatient waiting-room congestion?
7. **Temporal Dynamics:** How does day-of-week demand affect operational throughput and staffing utilization?
8. **Ancillary Demand:** What percentage of patients require radiology/laboratory diagnostics, and how do diagnostic turnaround times amplify doctor delays?
9. **Encounter Length of Stay (LOS):** What is the overall average hospital encounter duration, and which patient groups experience extreme tail delays?
10. **Resource Pressures:** How do bed availability and nurse/physician staffing ratios correlate with queue formation and capacity stress?

---

## 3. High-Level System Architecture

```
+-------------------------------------------------------------------------------+
|                        PATIENT FLOW DATA LIFECYCLE                            |
+-------------------------------------------------------------------------------+
|  1. INGESTION       Synthetic EHR Multi-Source Ingestion (30,450 raw records)  |
|         |           - Queue dynamics, shift staffing, seasonal surge events   |
|         v                                                                     |
|  2. CLEANING        Automated ETL Pipeline (`clean_hospital_data.py`)         |
|         |           - Deduplication, date standardization, imputation        |
|         v                                                                     |
|  3. VALIDATION      Automated Audit Rules (`validate_data.py`)                |
|         |           - Sequence checks, chronological bounds, outlier winsor   |
|         v                                                                     |
|  4. ANALYTICS       Statistical Modeling (`analyze_patient_flow.py`)          |
|         |           - Correlation, PCA, journey funnels, Z-score anomalies    |
|         v                                                                     |
|  5. TABLEAU BI      Interactive Decision-Support Dashboards                   |
|                     - Dashboard 1: Hospital Flow Overview                     |
|                     - Dashboard 2: Department Bottleneck Analysis             |
|                     - Dashboard 3: Patient Journey & Waiting Time             |
|                     - Dashboard 4: Operational Intelligence                   |
+-------------------------------------------------------------------------------+
```

---

## 4. Key Differentiating Features

* **Non-Clinical Operational Focus:** Strictly measures process throughput, queuing intervals, and operational strain without fabricating diagnostic or clinical recommendations.
* **Realistic Queue Mechanics:** Incorporates non-linear queuing behavior where queue length stretches when hourly volume nears department capacity limits.
* **Composite Bottleneck Index:** Introduces an analytical 0–100 score transparently weighted across wait times (40%), bed occupancy (35%), and staffing ratios (25%).
* **Multi-Dashboard Interactivity:** Leverages Tableau parameter controls, cross-sheet drilldowns, and hover actions for intuitive operational exploration.
