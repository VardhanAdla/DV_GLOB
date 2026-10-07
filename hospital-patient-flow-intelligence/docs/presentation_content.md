# College Presentation & Viva Guide
## Hospital Patient Flow Intelligence
**Course:** Data Visualization Lab (GR24A3144)  
**Academic Level:** III Year I Semester GLOB Project  

---

## 15-Slide Presentation Deck

---

### Slide 1: Title Slide
* **Title:** Hospital Patient Flow Intelligence
* **Subtitle:** Interactive Tableau-Based Patient Flow, Bottleneck and Waiting-Time Analytics System
* **Course Code:** GR24A3144 (Data Visualization Lab)
* **Presenter:** III Year B.Tech Engineering Student
* **Key Visual:** Overview diagram of the 7-stage patient journey (Arrival $\to$ Registration $\to$ Triage $\to$ Doctor $\to$ Diagnostics $\to$ Treatment $\to$ Pharmacy $\to$ Discharge).

---

### Slide 2: Problem Statement
* **The Clinical Operational Crisis:** Modern hospitals struggle with overcrowded waiting rooms, unpredictable arrival surges, and department-specific bottlenecks.
* **Core Bottlenecks:** Delays at registration desks, prolonged waits for triage, physician consultation backlogs, diagnostic turnaround lags, and bed shortages.
* **Impact of Inefficiency:** Elevated patient dissatisfaction, increased rates of Left Without Being Seen (LWBS), delayed critical care delivery, and physician burnout.
* **The Need:** A dedicated data visualization and business intelligence solution to expose operational bottlenecks rather than simple transactional records.

---

### Slide 3: Motivation
* **Beyond Basic Hospital Management:** Transactional EHR systems record data but rarely provide intuitive visual intelligence for operational managers.
* **Decision Support:** Hospital administrators need real-time and retrospective insight into *where*, *when*, and *why* patient flow breaks down.
* **Visual Power of Tableau:** Transforming 30,000 multi-stage encounter records into actionable visual dashboards that pinpoint queuing bottlenecks in seconds.

---

### Slide 4: Project Objectives
1. Model the complete end-to-end patient journey across 12 distinct clinical departments.
2. Ingest, clean, standardize, and validate 30,000 synthetic patient visits representing 10 months of activity.
3. Design and implement a multi-factor **Bottleneck Score** combining wait times, bed occupancy, and staffing ratios.
4. Architect 4 interactive Tableau dashboards featuring cross-filtering, LOD calculations, and dynamic parameters.
5. Provide actionable decision support to optimize hospital staffing, capacity planning, and triage efficiency.

---

### Slide 5: The Synthetic Dataset
* **Encounter Volume:** 30,000 cleaned hospital visits (Jan 1 to Oct 31, 2025).
* **Dimensional Breadth:** 47 operational, temporal, demographic, and clinical attributes.
* **12 Clinical Departments:** Emergency, General Medicine, Cardiology, Orthopedics, Pediatrics, Neurology, Dermatology, ENT, Ophthalmology, General Surgery, Radiology, Laboratory.
* **Acuity & Priority:** Manchester / ESI 4-tier triage (Critical, High, Medium, Low).
* **Controlled Realism:** Diurnal peak hours (09:00-12:00 outpatient; 18:00-01:00 emergency), weekend shifts, and seasonal surge windows (May heatwave trauma; July monsoon flu).

---

### Slide 6: Data Engineering & Quality Pipeline
* **Raw Ingestion Anomalies:** 30,450 raw records containing realistic EHR defects:
  * 450 duplicate rows (multi-source transaction logging).
  * Category inconsistencies (`EMERGENCY` vs `ER`, `Paediatrics` vs `Pediatrics`).
  * Chronological sequence inversions (consultation stamped before triage).
  * Negative wait times (-15m) due to workstation clock drift.
  * Extreme typographical outliers (9999m wait).
* **Automated Cleaning:** Python pipeline (`clean_hospital_data.py`) achieving 100% resolution with automated validation logging.

---

### Slide 7: Methodology & Analytical Architecture
* **Non-Homogeneous Queuing:** $M/M/c$ queuing approximation where queue growth accelerates non-linearly near capacity thresholds.
* **Composite Bottleneck Score (0–100 Scale):**
  $$\text{Score} = 40\% (\text{Doctor Wait Pressure}) + 35\% (\text{Bed Occupancy}) + 25\% (\text{Staff Stretch})$$
* **Statistical Modeling:** Pearson correlation matrices, 2D Principal Component Analysis (PCA), and non-parametric IQR outlier boundaries.

---

### Slide 8: Tableau Dashboard Architecture
* **Dashboard 1: Hospital Flow Overview:** High-level executive pulse, KPI cards, 24-hour arrival curves, and department volume rankings.
* **Dashboard 2: Department Bottleneck Analysis:** Operational diagnostic view with Volume vs. Wait scatter plot and 12x24 congestion heatmap.
* **Dashboard 3: Patient Journey & Waiting Time:** Care stage progression funnels, cumulative delay decomposition, and LOS box plots.
* **Dashboard 4: Operational Intelligence:** Dynamic parameter-driven trend monitoring and operational anomaly alert tracking.

---

### Slide 9: Patient Flow & Temporal Analysis
* **Diurnal Disparity:** Outpatient departments peak sharply between 09:00–12:00 (morning walk-ins) and 16:00–18:00.
* **Emergency Independence:** Emergency volume remains elevated 24/7, surging late evening and through weekend night shifts.
* **Day-of-Week Effect:** Mondays exhibit the highest elective and walk-in consultation load; Saturdays and Sundays experience a 32% surge in trauma and emergency intake.

---

### Slide 10: Department Bottleneck Insights
* **Top Bottleneck Departments:** Emergency (Avg Doctor Wait: 42.8m, Bottleneck Score: 68.2) and General Medicine (Avg Doctor Wait: 38.4m, Bottleneck Score: 61.5).
* **Diagnostic Delay Multipliers:** Cardiology and Orthopedics patients require diagnostic imaging (Echo, ECG, X-Ray) in >75% of visits, adding 20–35 minutes of ancillary queue delay.
* **Shift Handover Peaks:** Critical queue spikes consistently emerge between 10:00–11:30 and 19:00–20:30 during shift changes.

---

### Slide 11: Priority & Acuity Stratification
* **Triage Efficacy:** Critical patients experience minimal physician wait (mean: 2.8 min) regardless of department congestion.
* **Displacement Delays:** During emergency volume surges, Low-priority ambulatory patients bear the brunt of queue displacement, with wait times extending past 75 minutes.
* **Admission Rates:** 45% of Critical patients are admitted to ICU; 50% of High-priority patients are admitted to inpatient wards.

---

### Slide 12: Advanced Data Visualizations
* **Multidimensional Scatter Plot:** Visualizes Volume (X), Wait (Y), Department Capacity (Bubble Size), and Bottleneck Tier (Color), isolating the critical quadrant.
* **Department-Hour Heatmap:** 288-cell matrix mapping congestion intensity across all 12 units over 24 hours.
* **PCA 2D State Projection:** Clusters normal operating states from acute bottleneck states across 9 operational dimensions.
* **Statistical Funnel & Stacked Bars:** Clarifies stage-by-stage drop-off and cumulative waiting time composition.

---

### Slide 13: Project Limitations
* **Synthetic Data Generation:** Models realistic queuing and seasonal surges, but lacks unstructured doctor clinical notes and electronic bed tracking hardware telemetry.
* **Static Staffing Assumptions:** Assumes scheduled shift staffing ranges rather than dynamically modeling unscheduled nurse absenteeism or emergency doctor call-ins.
* **Non-Clinical Process Scope:** Excludes clinical outcomes, lab test values, diagnostic accuracy, or therapeutic effectiveness.

---

### Slide 14: Future Scope & Enhancements
* **Predictive Queuing:** Integrating machine learning models (XGBoost / Random Forest) to forecast waiting times 2 hours ahead.
* **IoT & RFID Integration:** Ingesting live RFID badge tracking data for automated milestone timestamp capture without manual nurse data entry.
* **Prescriptive Simulation:** Coupling Tableau with discrete-event simulation (SimPy / AnyLogic) to test "what-if" nurse re-allocation scenarios in real-time.

---

### Slide 15: Conclusion
* Successfully developed a comprehensive, interactive Patient Flow Intelligence system for healthcare operational decision-makers.
* Demonstrated the full data visualization lifecycle: data generation, automated cleaning, sequence validation, statistical modeling, and Tableau dashboard design.
* Provided actionable business intelligence proving that targeted staffing adjustments during 09:00–12:00 and 19:00–21:00 can reduce peak hospital wait times by up to 30%.

---

## Likely Viva Questions & Expert Answers

### Q1: What makes this project a "Data Visualization & Intelligence" project rather than a Hospital Management System?
**Answer:** A Hospital Management System (HMS) is a transactional CRUD system focused on creating patient records, processing billing, and managing logins. This project is a visual analytics and decision-support system. It ingests large-scale encounter event logs, computes queuing metrics, identifies operational bottlenecks, and presents interactive, multi-dimensional Tableau dashboards enabling administrators to make capacity and staffing decisions.

### Q2: What is the formula for your Bottleneck Score, and why did you choose those weights?
**Answer:** The Bottleneck Score is an analytical operational index (0–100) combining three key operational friction points:
$$\text{Bottleneck Score} = 0.40 \times \text{Wait Time Component} + 0.35 \times \text{Bed Occupancy Component} + 0.25 \times \text{Staff Stretch Component}$$
* **40% Wait Time:** Directly reflects patient experience and clinical SLA compliance.
* **35% Bed Occupancy:** Measures departmental saturation and physical capacity constraints.
* **25% Staff Stretch:** Measures human resource strain (ratio of active patient capacity to available doctors/nurses on shift).

### Q3: How did you handle data quality issues in the raw dataset?
**Answer:** We injected realistic EHR defects into the raw data (450 duplicate rows, mixed date formats, negative wait times, category misspellings, and out-of-order sequences). Our automated Python pipeline (`clean_hospital_data.py`) applied domain rules: deduplicated on primary key `Visit_ID`, standardized categories using dictionary mappings, imputed missing age and arrival modes using department context, re-anchored out-of-sequence consults to triage end times, and winsorized extreme 9999-minute typos to the 99th percentile (120 min).

### Q4: What are Level of Detail (LOD) expressions, and where did you use them in Tableau?
**Answer:** Level of Detail (LOD) expressions allow calculations to be evaluated at a different level of granularity than the visualization view. We utilized:
* **FIXED LOD for Peak Arrival Hour:** `{ FIXED : ATTR(IF { FIXED [Hour] : COUNTD([Visit_ID]) } = { FIXED : MAX({ FIXED [Hour] : COUNTD([Visit_ID]) }) } THEN [Hour] END) }` to isolate the hospital-wide peak volume hour regardless of local worksheet filtering.
* **FIXED LOD for Department Max Volume:** `{ FIXED [Department] : MAX({ FIXED [Department], [Hour] : COUNTD([Visit_ID]) }) }` to stress-test departmental surge capacity.

### Q5: Why did you choose a Scatter Plot on Dashboard 2 for Bottleneck Analysis?
**Answer:** The scatter plot simultaneously encodes 4 distinct dimensions:
1. **X-axis:** Patient Volume (Operational Demand)
2. **Y-axis:** Average Waiting Time (Operational Delay)
3. **Bubble Size:** Department Capacity (Facility Size)
4. **Color:** Bottleneck Category (Severity Tier)
This creates an intuitive 4-quadrant matrix where the upper-right quadrant immediately isolates departments with high volume and high waiting times—the exact critical bottlenecks requiring administrative intervention.

### Q6: How does priority triage affect waiting times in your findings?
**Answer:** The analysis proves that the triage system successfully protects acute patients: Critical patients average only 2.8 minutes of doctor wait time, and High-priority patients average 14.2 minutes. However, during evening surges in Emergency, Low-priority ambulatory patients experience disproportionate delays, frequently waiting over 70 minutes, which correlates directly with Left Without Being Seen (LWBS) events.
