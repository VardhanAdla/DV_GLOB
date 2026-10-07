# Project Objectives & Research Goals

**Project Title:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Primary Academic & Technical Objectives

The core goal of this project is to develop an end-to-end Data Visualization and Operational Intelligence system that bridges the gap between raw healthcare event logs and executive decision-making.

### Objective 1: Realistic Healthcare Queuing Data Simulation
* Synthesize an anonymized cohort of 30,000 distinct patient encounters spanning 10 continuous months of hospital operations.
* Model 12 clinical care units with distinct capacity limits, baseline staffing profiles, and consultation durations.
* Simulate non-linear queuing dynamics ($M/M/c$ queuing theory), diurnal arrival rhythms (morning OPD spikes vs 24/7 emergency dynamics), weekday/weekend demand swings, and seasonal surge windows (monsoon epidemics and summer trauma surges).

### Objective 2: Automated Data Engineering & Quality Auditing
* Inject realistic Electronic Health Record (EHR) data imperfections into a 30,450-record raw ingestion feed.
* Build an automated Python data cleansing pipeline (`clean_hospital_data.py`) to eliminate duplicates, harmonize vocabulary, impute missing values, reconcile inverted timestamps, and winsorize logging typos.
* Implement automated data validation (`validate_data.py`) certifying 100% integrity across primary keys, domain vocabularies, and chronological stage sequences.

### Objective 3: Quantitative Bottleneck Modeling
* Formulate an objective, bounded 0–100 **Bottleneck Score** that synthesizes physician waiting delays (40%), bed occupancy saturation (35%), and clinical staffing stretch ratios (25%).
* Segment clinical encounters and department-hour shifts into 4 operational performance tiers: *Optimal Flow*, *Manageable Flow*, *Moderate Congestion*, and *Severe Bottleneck*.

### Objective 4: Interactive Tableau Business Intelligence System
* Architect 4 publication-quality, interactive Tableau dashboards:
  1. **Dashboard 1 (Executive Flow Overview):** Summary KPI cards, 24-hour diurnal volume curves, department volume bars, and acuity mix donuts.
  2. **Dashboard 2 (Department Bottleneck Analysis):** Department waiting-time ranking bars with SLA targets, volume-versus-wait scatter plots, and granular 12x24 congestion heatmaps.
  3. **Dashboard 3 (Patient Journey & Waiting Time):** Care stage progression funnels, cumulative delay decomposition, and length-of-stay dispersion box plots.
  4. **Dashboard 4 (Operational Intelligence):** Parameter-driven dynamic trend exploration, day-of-week arrival grids, and operational surge anomaly tracking.
* Implement advanced Tableau interactivity: Level of Detail (LOD) benchmark expressions, dynamic parameter switching, cross-sheet drilldowns, and hover highlight actions.

### Objective 5: Multi-Dimensional Exploratory Analysis
* Conduct supplementary statistical and machine learning analyses in Python, including Pearson correlation matrices, 2D Principal Component Analysis (PCA) projections, and statistical anomaly detection using Z-score and Interquartile Range (IQR) boundaries.
* Deliver an exhaustive manual build guide, presentation slides, and academic report documentation suitable for university laboratory evaluation and viva examination.
