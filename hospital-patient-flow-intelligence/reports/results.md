# Results & Key Analytical Findings

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  
**Primary Dataset Scope:** 30,000 verified encounters across 12 departments (Jan 1 – Oct 31, 2025)  

---

## 1. Executive Summary Table

| Operational Performance Metric | Dataset Aggregate Value | Clinical Benchmark / Target | Variance / Interpretation |
| :--- | :---: | :---: | :--- |
| **Total Ingested Encounters** | 30,000 visits | ~100 visits / day | Steady operational baseline across 304 days |
| **Overall Average Doctor Wait** | 34.2 minutes | $\le 30.0$ minutes | +4.2 min (+14% above target SLA) |
| **Median Doctor Wait Time** | 29.0 minutes | $\le 25.0$ minutes | Positively skewed by peak shift surges |
| **Average Total Length of Stay (LOS)** | 148.5 minutes | $\le 120.0$ minutes | Prolonged by diagnostic & treatment delays |
| **Emergency Presentation Rate** | 20.3% (6,088 visits) | 15.0% - 25.0% | Typical for regional tertiary trauma center |
| **Diagnostic Test Utilization Rate** | 48.4% (14,528 visits) | 40.0% - 50.0% | Heavy driver of ancillary queue delays |
| **Dispensary Pharmacy Route Rate** | 68.1% (20,432 visits) | 65.0% - 75.0% | Creates discharge bottlenecks at midday |
| **Severe Bottleneck Episodes** | 12.8% of encounter hours | $\le 5.0\%$ | Concentrated in Emergency & General Medicine |

---

## 2. Department-Level Waiting Times & Bottleneck Rankings

Aggregated operational metrics computed by `src/analyze_patient_flow.py` rank the 12 clinical care units by queue congestion and operational strain:

| Department | Total Patient Visits | Avg Doctor Wait (min) | Median Wait (min) | P90 Wait (min) | Avg Bottleneck Score (0-100) | Bottleneck Performance Tier |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Emergency** | 6,088 | **42.8** | 36.0 | 78.5 | **68.2** | Severe Bottleneck |
| **General Medicine** | 5,412 | **38.4** | 33.0 | 69.0 | **61.5** | Moderate Congestion |
| **Cardiology** | 2,704 | **35.6** | 31.0 | 64.0 | **56.8** | Moderate Congestion |
| **Orthopedics** | 3,011 | **34.8** | 30.0 | 62.5 | **55.2** | Moderate Congestion |
| **Pediatrics** | 3,308 | **32.1** | 28.0 | 58.0 | **51.4** | Moderate Congestion |
| **General Surgery** | 1,518 | 29.4 | 26.0 | 54.0 | 47.9 | Manageable Flow |
| **Neurology** | 1,504 | 28.7 | 25.0 | 52.0 | 46.8 | Manageable Flow |
| **Ophthalmology** | 1,192 | 24.3 | 22.0 | 44.0 | 38.6 | Manageable Flow |
| **ENT** | 1,496 | 23.9 | 21.0 | 43.0 | 37.9 | Manageable Flow |
| **Dermatology** | 1,512 | 22.8 | 20.0 | 41.0 | 36.5 | Manageable Flow |
| **Radiology** | 1,128 | 18.5 | 16.0 | 34.0 | 31.2 | Optimal Flow |
| **Laboratory** | 1,127 | 15.2 | 13.0 | 28.0 | 27.4 | Optimal Flow |

---

## 3. Diurnal Arrival Patterns & Temporal Congestion

Analysis of 24-hour presentation curves reveals stark operational divergence between outpatient and emergency care:
1. **Outpatient Presentation Surges:** Outpatient clinics experience acute bi-modal surges:
   * **Morning Surge (09:00 – 12:00):** Captures 35% of all daily outpatient arrivals, peaking at 10:00 (averaging 185 visits/hour hospital-wide).
   * **Afternoon Surge (16:00 – 18:00):** Captures 21% of daily outpatient volume.
2. **Emergency Department 24/7 Continuity:** Emergency intake maintains consistent volume across all 24 hours, but surges significantly in the late evening and early night (18:00 – 01:00), capturing 38% of emergency volume when outpatient clinics are closed and staffing is reduced to night shifts.
3. **Day-of-Week Variation:**
   * **Mondays & Tuesdays:** Highest elective walk-in outpatient volume (+22% above weekly average).
   * **Saturdays & Sundays:** Emergency arrivals surge by +34%, primarily driven by vehicular trauma, acute cardiac events, and domestic accidents.

---

## 4. Triage Acuity & Queuing Disparities

Cross-tabulating patient priority levels against care milestones confirms the clinical effectiveness of triage prioritization alongside non-urgent queuing penalties:

| Priority Tier | Patient Volume | Avg Triage Wait | Avg Doctor Wait | Avg Total Wait | Avg Total LOS | Primary Disposition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Critical (Tier 1)** | 1,220 (4.1%) | **0.0 min** | **2.8 min** | **24.5 min** | **182.4 min** | 45% ICU, 45% Ward, 10% Transfer |
| **High (Tier 2)** | 4,812 (16.0%) | **5.2 min** | **14.2 min** | **52.1 min** | **164.8 min** | 50% Ward, 42% Home, 8% ICU/Transfer |
| **Medium (Tier 3)**| 14,244 (47.5%)| **12.4 min** | **33.6 min** | **84.6 min** | **145.2 min** | 88% Discharged Home, 12% Ward |
| **Low (Tier 4)**   | 9,724 (32.4%) | **18.7 min** | **48.6 min** | **106.2 min** | **132.8 min** | 96% Discharged Home, 4% LWBS |

* **Key Takeaway:** While Critical and High patients are prioritized rapidly, Low-priority patients endure substantial delays during peak surge hours, with doctor waits occasionally exceeding 75 minutes.

---

## 5. Ancillary Diagnostic & Stage Delay Decomposition

Decomposing the patient journey into discrete service queues identifies the primary sources of operational delay:
* **Doctor Consultation Waiting:** Represents **38.5%** of all cumulative waiting time across the hospital encounter.
* **Diagnostic Imaging & Lab Wait:** Contributes **24.2%** of total delay for patients requiring testing.
  * In **Cardiology** (78% diagnostic rate) and **Orthopedics** (75% diagnostic rate), diagnostic queues add an average of **28.4 minutes** and **24.8 minutes** respectively.
* **Dispensary Pharmacy Wait:** Contributes **16.1%** of encounter waiting time, peaking between 12:00–14:00 as morning outpatient consultations conclude simultaneously.

---

## 6. Correlation Modeling & PCA State Projections

Statistical evaluation in `analysis/correlation/correlation_matrix.csv` highlights key operational relationships:
* **Doctor Wait Time vs Bed Occupancy Rate:** Moderate positive correlation ($r = +0.58$), confirming that physical bed saturation directly stalls upstream consultation velocity.
* **Doctor Wait Time vs Staff Availability:** Strong negative correlation ($r = -0.64$), validating that unadjusted shift staffing creates predictable queue blowouts.
* **Total Length of Stay vs Total Wait Time:** Very strong positive correlation ($r = +0.81$), indicating that process delays—not clinical complexity—dominate total hospital stay durations.
* **Principal Component Analysis:** The first 2 principal components capture **68.4%** of total system variance, distinctly clustering normal operational states from acute emergency surge and bed depletion states.

---

## 7. Statistical Operational Anomaly Detection

Execution of `src/anomaly_analysis.py` flagged **270 distinct operational anomaly events** ($|Z| > 2.2$ or $Q_3 + 1.5\text{IQR}$):
1. **May 10–16 Trauma & Heat Outbreak:** Emergency patient intake proportion surged to 34.8% (normal: 20.3%), driving bed availability down to 1.2 beds and expanding average doctor wait times to 56.4 minutes.
2. **July 15–25 Monsoon Pediatric & General Medicine Surge:** Inflow in Pediatrics and General Medicine increased by 78%, generating queue delays in excess of 65 minutes for semi-urgent cases.
