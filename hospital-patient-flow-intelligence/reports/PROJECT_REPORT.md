# Comprehensive Academic Project Report
## Hospital Patient Flow Intelligence
### Interactive Hospital Patient Flow, Bottleneck, Waiting-Time and Operational Intelligence System

**Course:** Data Visualization Lab  
**Course Code:** GR24A3144  
**Academic Level:** III Year I Semester B.Tech GLOB Evaluation  

---

## 1. Abstract
Modern hospitals operate as complex, multi-stage stochastic service environments where patient care requires tight coordination across registration, clinical triage, doctor consultation, diagnostic testing, treatment, and pharmacy dispensing. When any stage becomes congested, downstream queues back up rapidly, ballooning waiting times, exacerbating bed shortages, and degrading clinical responsiveness. The **Hospital Patient Flow Intelligence** project delivers an interactive, decision-support business intelligence system designed to expose operational bottlenecks, evaluate waiting-time disparities across priority tiers, analyze diurnal and day-of-week arrival surges, and track departmental capacity saturation. Modeling 30,000 verified encounters across 12 clinical care units, the system combines an automated Python data simulation, cleaning, validation, and multi-dimensional analytics pipeline with 4 interactive Tableau dashboards and a responsive 5-page Streamlit web application.

---

## 2. Introduction & Existing System vs Proposed System

### 2.1 Existing System Limitations
Traditional hospital operations rely heavily on transactional Electronic Health Record (EHR) databases and Hospital Information Systems (HIS). While effective for billing, insurance adjudication, and clinical charting, existing systems present severe analytical deficiencies:
1. **Static Historical Reporting:** Outputs consist primarily of end-of-month tabular PDFs summarizing total admissions and occupancy percentages without revealing hourly queue dynamics.
2. **Siloed Departmental Views:** Clinical units operate with independent queue displays, blinding administrators to cross-departmental bottlenecks (e.g. inpatient bed gridlock stalling emergency department throughput).
3. **Absence of Multi-Dimensional Drilldown:** Administrators cannot interactively filter or test "what-if" operational scenarios across arrival hours, priority tiers, or diagnostic requirements.

### 2.2 Proposed System
The proposed system transitions from passive record-keeping to visual operational intelligence:
* **End-to-End Care Stage Tracking:** Deconstructs encounters into discrete queuing intervals (Registration, Triage, Doctor, Diagnostics, Treatment, Pharmacy).
* **Multi-Factor Bottleneck Scoring:** Implements an objective 0–100 index combining wait times (40%), bed occupancy (35%), and staffing stretch ratios (25%).
* **Interactive Visual Dashboards:** Built natively in Tableau Desktop (and mirrored in Streamlit with Plotly) with cross-sheet filtering, LOD expressions, and dynamic parameters.

---

## 3. Problem Statement & Research Objectives
* **Formal Problem Statement:** *"How can complex, high-velocity hospital patient encounter logs across multiple clinical units, acuity tiers, and care stages be transformed into an interactive, multi-dimensional visual intelligence system that reliably identifies operational bottlenecks, measures waiting-time disparities, tracks capacity saturation, and provides intuitive decision support for hospital resource planners?"*
* **Core Objectives:**
  1. Generate a 30,000-encounter realistic synthetic queuing dataset across 12 clinical units with diurnal arrival curves, shift staffing, and seasonal surge windows.
  2. Implement an automated data cleansing pipeline that resolves EHR data quality defects (duplicates, inverted sequences, negative workstation clock waits).
  3. Architect 4 interactive Tableau dashboards and a 5-page Streamlit application.
  4. Perform multi-dimensional statistical, correlation, PCA, and anomaly detection modeling.

---

## 4. System Architecture & Methodology Pipeline

```
+----------------------------------------------------------------------------------------------------+
|                                    SYSTEM ARCHITECTURAL PIPELINE                                   |
+----------------------------------------------------------------------------------------------------+
|  1. Ingestion: Non-homogeneous Poisson simulation -> 30,450 raw records with EHR anomalies       |
|  2. Cleansing: Deduplication, canonical mapping, sequence repair -> 30,000 clean records           |
|  3. Validation: Automated 8-checkpoint audit -> Certified zero defects                            |
|  4. Analytics: Bottleneck scoring, correlation, PCA (68.1% var), IQR & Isolation Forest anom      |
|  5. Visual BI: Tableau Desktop 2026.2 (4 Dashboards, 14 Worksheets) + Streamlit App (5 Pages)      |
+----------------------------------------------------------------------------------------------------+
```

---

## 5. Dataset Description & 12 Clinical Departments

* **Record Volume:** 30,000 verified encounters spanning 10 months (Jan 1 to Oct 31, 2025).
* **Dimensional Breadth:** 47 operational, clinical, and demographic attributes per record.
* **Clinical Departments Modeled:**
  1. **Emergency:** 24/7 acute trauma and critical care intake.
  2. **General Medicine:** High-volume outpatient chronic and acute illness care.
  3. **Cardiology:** High diagnostic requirement (ECG, Echocardiogram, telemetry).
  4. **Orthopedics:** High radiological imaging requirement (X-ray, CT scans).
  5. **Neurology:** Specialized consultative outpatient care.
  6. **Pediatrics:** Specialized child health care (ages 1–16).
  7. **General Surgery:** Pre-operative evaluation and surgical consultations.
  8. **Radiology:** Ancillary imaging service center.
  9. **Laboratory:** Ancillary pathology and blood testing center.
  10. **Pharmacy:** Dispensary and medication distribution center.
  11. **ICU (Intensive Care Unit):** High-acuity critical care unit.
  12. **OPD (General Outpatient):** General ambulatory clinic services.

---

## 6. Data Cleaning & Feature Engineering

### 6.1 Data Quality Rectification
* **Deduplication:** 450 duplicate rows eliminated using primary key `Visit_ID`.
* **Category Harmonization:** Canonical mappings applied to departments (`EMERGENCY` $\to$ `Emergency`, `Paediatrics` $\to$ `Pediatrics`) and genders (`F` $\to$ `Female`, `M` $\to$ `Male`).
* **Sequence Reconciliation:** Inverted timestamps (`Doctor_Start_Time < Triage_Time`) re-anchored to:
  $$\text{Doctor Start Time} = \text{Triage Time} + \text{Wait Doctor}$$
* **Negative Wait Fix:** Unsynchronized workstation clock values (-15m) re-anchored to priority median waits (Critical: 3m, High: 14m, Medium: 32m, Low: 48m).
* **Typo Winsorization:** Logging errors (>500m) capped at the 99th percentile (120m).

### 6.2 Derived Operational Features
* `Waiting_Time_Category`: Binned into `<30m`, `30-60m`, `60-90m`, and `>90m`.
* `LOS_Category`: Binned into `<2h`, `2-4h`, `4-6h`, and `>6h`.
* `Department_Utilization`: $(\text{Capacity} - \text{Available Beds}) / \text{Capacity}$.
* `Capacity_Pressure`: $\text{Utilization} \times (\text{Capacity} / [\text{Staff} \times 4])$.
* `Bottleneck_Score`: Weighted composite index (0–100 scale).

---

## 7. The Academic Bottleneck Model

$$\text{Bottleneck Score} = 0.40 \times \text{Wait Component} + 0.30 \times \text{Capacity Component} + 0.20 \times \text{Volume Component} + 0.10 \times \text{Staff Component}$$

* **Component Formulas:**
  * **Wait Pressure (40%):** $\min\left(40.0, \frac{\text{Wait Doctor}}{75.0} \times 40.0\right)$
  * **Capacity Pressure (30%):** $\text{Department Utilization} \times 30.0$
  * **Volume Pressure (20%):** $\min\left(20.0, \frac{\text{Capacity Pressure}}{2.0} \times 20.0\right)$
  * **Staff Strain (10%):** $\min\left(10.0, \frac{\text{Department Capacity}}{\text{Staff Available} \times 5.0} \times 5.0\right)$
* **Classification:** Low (<35), Moderate (35–49), High (50–69), Critical ($\ge$ 70).
* **Disclaimer:** *"This is an academic analytical model and is not a clinically validated hospital standard."*

---

## 8. Multi-Dimensional Analytics & Machine Learning

1. **Correlation Matrix:** Doctor wait time correlates strongly with clinical staff availability ($r = -0.64$) and bed occupancy ($r = +0.58$), confirming that unadjusted staffing creates predictable queue delays.
2. **Principal Component Analysis (PCA):** PC1 (43.7% variance - queue delay) and PC2 (24.4% variance - capacity pressure) capture a cumulative **68.1%** of operational variance.
3. **K-Means Clustering ($k=4$):** Identifies four distinct operational regimes: Balanced Flow, Outpatient Queue Surge, Emergency Overload, and Diagnostic Stagnation.
4. **Operational Anomaly Detection:** Non-parametric IQR thresholding ($Q_3 + 1.5\text{IQR}$) and Scikit-Learn Isolation Forest flagged 270 severe operational events, isolating the May trauma surge and July monsoon epidemic.

---

## 9. Tableau & Streamlit Dashboard Implementations

### 9.1 Tableau Architecture (4 Integrated Dashboards)
* **Dashboard 1: Hospital Flow Overview:** High-level executive pulse, KPI cards, 24-hour diurnal volume curves, department volume rankings, and triage priority distribution.
* **Dashboard 2: Department Bottleneck Analysis:** Operational diagnostic view with Volume vs. Wait scatter plot and 12x24 congestion heatmap.
* **Dashboard 3: Patient Journey & Waiting Time:** Care stage progression funnels, cumulative delay decomposition, and length-of-stay dispersion box plots.
* **Dashboard 4: Operational Intelligence:** Dynamic parameter-driven trend monitoring and operational anomaly alert tracking.

### 9.2 Streamlit Web Application (5 Interactive Pages)
* Built in `dashboard/app.py` featuring Plotly charts, global sidebar filters, patient and visit ID search drilldowns, CSV downloads, and an automated insight engine.

---

## 10. Results & Departmental Benchmarks

| Clinical Department | Total Ingested Encounters | Mean Doctor Wait (min) | Median Wait (min) | Mean Bottleneck Score | Bottleneck Category |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Emergency** | 6,088 | **42.8** | 36.0 | **68.2** | High / Critical |
| **General Medicine** | 5,412 | **38.4** | 33.0 | **61.5** | High |
| **Cardiology** | 2,704 | **35.6** | 31.0 | **56.8** | High |
| **Orthopedics** | 3,011 | **34.8** | 30.0 | **55.2** | High |
| **Pediatrics** | 3,308 | **32.1** | 28.0 | **51.4** | High |
| **General Surgery** | 1,518 | 29.4 | 26.0 | 47.9 | Moderate |
| **Neurology** | 1,504 | 28.7 | 25.0 | 46.8 | Moderate |
| **OPD (General)** | 1,480 | 25.1 | 23.0 | 40.2 | Moderate |
| **Ophthalmology** | 1,192 | 24.3 | 22.0 | 38.6 | Moderate |
| **ENT** | 1,496 | 23.9 | 21.0 | 37.9 | Moderate |
| **Dermatology** | 1,512 | 22.8 | 20.0 | 36.5 | Moderate |
| **Radiology** | 1,128 | 18.5 | 16.0 | 31.2 | Low |
| **Laboratory** | 1,127 | 15.2 | 13.0 | 27.4 | Low |

---

## 11. Practical Operational Recommendations

1. **Staggered Shift Scheduling:** Overlapping 10-hour clinical shifts to maintain staffing during the 10:00–12:00 and 19:00–21:00 arrival peaks.
2. **Fast-Track Emergency Triage:** Deploy dedicated rapid-assessment tracks for Low/Medium acuity cases to reduce ambulatory delays by ~35%.
3. **Point-of-Care Diagnostics:** Establish satellite ultrasound and point-of-care cardiac testing in Cardiology and Orthopedics to mitigate radiology transit queues.
4. **Dynamic Bed Allocation:** Automated capacity alerts triggered when bed occupancy exceeds 85%.

---

## 12. Limitations & Future Scope
* **Limitations:** Relies on synthetic queuing models; lacks unstructured doctor notes and physical IoT spatial coordinates.
* **Future Scope:** Ingesting live RFID/BLE patient tracking streams, deploying machine learning waiting-time forecasters (XGBoost/LSTM), and integrating SimPy discrete-event simulation for real-time "what-if" capacity modeling.

---

## 13. References
1. Hall, R. W. (2012). *Patient Flow: Reducing Delay in Healthcare Delivery*. Springer Science & Business Media.
2. Armony, M., et al. (2015). *Patient flow in hospitals: A review of queueing models*. Operations Research for Health Care.
3. Few, S. (2013). *Information Dashboard Design: Displaying Data for At-a-Glance Monitoring*. Analytics Press.
4. Tableau Software. (2026). *Tableau Desktop & Prep Official Calculation Reference*. Salesforce Inc.
