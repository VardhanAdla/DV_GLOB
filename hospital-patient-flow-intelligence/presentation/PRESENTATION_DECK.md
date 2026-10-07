# Hospital Patient Flow Intelligence: Presentation Deck
## Interactive Hospital Patient Flow, Bottleneck, Waiting-Time and Operational Intelligence System

**Course:** Data Visualization Lab (Course Code: GR24A3144)  
**Academic Level:** III Year I Semester B.Tech  
**Slide Count:** 18 Slides with Visual Placeholders and Speaker Notes  

---

### Slide 1: Title Slide
* **Title:** Hospital Patient Flow Intelligence
* **Subtitle:** Interactive Hospital Patient Flow, Bottleneck, Waiting-Time and Operational Intelligence System
* **Course Code:** GR24A3144 (Data Visualization Lab)
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [VISUAL: Patient Flow Banner Diagram: Arrival -> Triage -> Doctor -> Discharge]|
  +-------------------------------------------------------------------------------+
  ```
* **Speaker Notes:** "Good morning, respected evaluators. Today I present our Data Visualization Lab GLOB project: Hospital Patient Flow Intelligence. Our objective is to transition beyond simple administrative reporting into an actionable visual analytics and decision-support system that models multi-stage patient delays and identifies clinical bottlenecks."

---

### Slide 2: Clinical Operational Problem Statement
* **The Clinical Dilemma:** High-velocity hospital emergency and outpatient units suffer from chronic waiting-room overcrowding, prolonged waiting delays, and mismatched staffing schedules.
* **The Root Cause:** Bottlenecks do not occur uniformly; queue delays compound across dependent care stations—registration, triage, doctor consult, diagnostic imaging, and pharmacy.
* **Impact:** Patient dissatisfaction, increased Left Without Being Seen (LWBS) walkouts, and delayed critical care delivery.
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [VISUAL: Flowchart showing queue accumulation and cascading delays]          |
  +-------------------------------------------------------------------------------+
  ```

---

### Slide 3: Motivation & Project Significance
* **Why Data Visualization?** Electronic Health Record (EHR) databases record millions of transactional timestamps, but clinical directors cannot deduce queue delays from raw tables.
* **Operational Intelligence:** Transforming tabular data into interactive visual dashboards enables instant identification of *"Where is the hospital losing time?"*
* **Decision Support:** Providing administrators with empirical evidence to restructure shift schedules, deploy fast-track triage, and optimize bed allocation.

---

### Slide 4: Project Objectives
1. Simulate a realistic, non-linear healthcare queuing dataset representing 30,000 patient encounters across 12 clinical care units.
2. Build an automated, auditable Python data cleansing pipeline that resolves EHR data quality defects.
3. Formulate a transparent, academic **Bottleneck Score** synthesizing waiting times, bed occupancy, and staffing burdens.
4. Architect 4 interactive Tableau dashboards with cross-filtering, LOD expressions, and dynamic parameters.
5. Deploy a full-featured, multi-page interactive Streamlit web application with Plotly visuals and an automated insight engine.

---

### Slide 5: System Architecture & Data Lifecycle
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [VISUAL ARCHITECTURE DIAGRAM]                                                 |
  | Ingestion (30,450 Raw) -> Clean/Validate (30,000 Clean) -> Analytics (PCA/ML)|
  |                                                              │                |
  |                                        ┌─────────────────────┴───────────────┐|
  |                                        ▼                                     ▼|
  |                            Tableau Desktop (4 Dashboards)       Streamlit App |
  +-------------------------------------------------------------------------------+
  ```
* **Speaker Notes:** "Our architecture maintains a clear separation between data engineering, statistical modeling, and interactive visualization."

---

### Slide 6: Dataset Characteristics & 12 Departments
* **Volume:** 30,000 clean encounters spanning 10 months of continuous hospital activity.
* **Variables:** 47 operational, demographic, and clinical attributes per encounter.
* **12 Departments Modeled:**
  * Emergency, General Medicine, Cardiology, Orthopedics, Neurology, Pediatrics, General Surgery, Radiology, Laboratory, Pharmacy, ICU, OPD.
* **Controlled Seasonality:** Models summer trauma surges (May) and monsoon respiratory/dengue outbreaks (July).

---

### Slide 7: Data Quality & Cleansing Pipeline
* **Injected Raw Defects:** 450 duplicate visits, department/gender acronym mismatches, chronological inversions (consult before triage), negative delays (-15m), and typo outliers (9999m).
* **Automated Python Cleansing:**
  * Deduplicated on primary key `Visit_ID`.
  * Canonical mapping to 12 standard clinical departments.
  * Re-anchoring out-of-order timestamps to triage completion.
  * 100% resolution verified by automated validation scripts.
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [VISUAL: Table comparing Raw Ingestion vs Clean Target Quality Metrics]       |
  +-------------------------------------------------------------------------------+
  ```

---

### Slide 8: The Academic Bottleneck Model
* **Formula:**
  $$\text{Bottleneck Score} = 0.40 \times \text{Wait Pressure} + 0.30 \times \text{Capacity Pressure} + 0.20 \times \text{Volume Pressure} + 0.10 \times \text{Staff Strain}$$
* **Scale:** Bounded 0 to 100 index categorized into Low (<35), Moderate (35-49), High (50-69), and Critical ($\ge$ 70).
* **Academic Disclaimer:** *"This is an academic analytical model and is not a clinically validated hospital standard."*

---

### Slide 9: Tableau Dashboard 1 — Hospital Flow Overview
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [SCREENSHOT PLACEHOLDER: Tableau Dashboard 1 - Hospital Flow Overview]        |
  | Top KPI Banner | 24-Hour Diurnal Curves | Dept Volume Bar | Triage Donut      |
  +-------------------------------------------------------------------------------+
  ```
* **Key Visuals:** KPI Cards (30,000 Visits, 34.2m Avg Wait, 148.5m LOS, 20.3% Emerg), Diurnal Arrival Curves comparing Emergency 24/7 inflow vs OPD morning rush.

---

### Slide 10: Tableau Dashboard 2 — Department Bottleneck Analysis
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [SCREENSHOT PLACEHOLDER: Tableau Dashboard 2 - Department Bottleneck Analysis] |
  | Volume vs Wait Scatter Plot | 12x24 Congestion Heatmap | 45m SLA Bar Chart    |
  +-------------------------------------------------------------------------------+
  ```
* **Key Visuals:** 4-quadrant Volume vs Wait Scatter plot and 12-Department x 24-Hour Congestion Heatmap isolating peak delays.

---

### Slide 11: Tableau Dashboard 3 — Patient Journey & Waiting Time
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [SCREENSHOT PLACEHOLDER: Tableau Dashboard 3 - Patient Journey & Waiting Time] |
  | Care Stage Funnel | Stacked Stage Delay Bars | LOS by Priority Box Plot       |
  +-------------------------------------------------------------------------------+
  ```
* **Key Visuals:** 6-stage delay decomposition showing that physician consults contribute 38.5% of total wait, followed by diagnostics (24.2%).

---

### Slide 12: Tableau Dashboard 4 — Operational Intelligence
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [SCREENSHOT PLACEHOLDER: Tableau Dashboard 4 - Operational Intelligence]      |
  | Parameter Dynamic Trend | Day vs Hour Matrix | Operational Anomaly Alerts Log |
  +-------------------------------------------------------------------------------+
  ```
* **Key Visuals:** Dynamic metric switching driven by parameter `[Select Analysis Metric]` and automated anomaly alert tracking.

---

### Slide 13: Interactive Streamlit Web Application
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [SCREENSHOT PLACEHOLDER: Streamlit Application (5 Interactive Pages)]         |
  | Multi-Page Navigation | Plotly Dynamic Visuals | Automated Insight Engine     |
  +-------------------------------------------------------------------------------+
  ```
* **Core Pages:** Overview, Department Bottlenecks, Patient Journey, Operational Intelligence, and Data Explorer with patient-level search.

---

### Slide 14: Advanced Analytics: PCA & Clustering
* **Principal Component Analysis:** PC1 (43.7% variance - queue delay) and PC2 (24.4% variance - capacity pressure) explain **68.1%** of total system variance.
* **K-Means Operational Clusters:** Segments operations into 4 distinct regimes: Balanced Flow, Outpatient Queue Surge, Emergency Overload, and Diagnostic Stagnation.
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [VISUAL: 2D PCA Cluster Scatter Plot from analysis/correlation/]              |
  +-------------------------------------------------------------------------------+
  ```

---

### Slide 15: Operational Anomaly Detection
* **Methodology:** Non-parametric IQR thresholding ($Q_3 + 1.5\text{IQR}$) and Scikit-Learn Isolation Forest.
* **Findings:** Flagged 270 severe operational events, isolating the May 10–16 Trauma Outbreak (emergency rate surged to 34.8%) and July 15–25 Monsoon Pediatric Surge (inflow +78%).
* **Visual Placeholder:**
  ```
  +-------------------------------------------------------------------------------+
  | [VISUAL: Time-Series Surge Anomaly Plot from analysis/anomalies/]             |
  +-------------------------------------------------------------------------------+
  ```

---

### Slide 16: Practical Administrative Recommendations
1. **Staggered Shift Scheduling:** Replace rigid 8-hour shift handovers with overlapping 10-hour shifts to cover the critical 10:00–12:00 and 19:00–21:00 congestion peaks.
2. **Fast-Track Emergency Triage:** Deploy dedicated rapid-assessment tracks for Low/Medium acuity cases to reduce ambulatory delays by ~35%.
3. **Point-of-Care Diagnostics:** Establish satellite ultrasound and point-of-care cardiac testing in Cardiology and Orthopedics to mitigate radiology transit queues.

---

### Slide 17: Limitations & Future Scope
* **Current Limitations:** Synthetic queuing data lacks unstructured clinician progress notes and physical IoT telemetry.
* **Future Roadmap:**
  * Real-time patient spatial tracking via Bluetooth Low Energy (BLE) and RFID badges.
  * Machine learning forecasting (XGBoost/LSTM) predicting queue delays 2 hours ahead.
  * Digital twin discrete-event simulation (SimPy) for interactive capacity planning.

---

### Slide 18: Conclusion
* Developed a complete, validated Hospital Patient Flow Intelligence system.
* Implemented end-to-end: Python queuing simulation, automated data cleansing, feature engineering, multi-dimensional modeling, 4 Tableau dashboards, and a live Streamlit web application.
* Delivered actionable insights proving that targeted staffing alignment can reduce peak hospital wait times by up to 30%.
* Thank you! Open for questions.
