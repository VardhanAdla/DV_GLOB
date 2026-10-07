# HOSPITAL PATIENT FLOW INTELLIGENCE
### Interactive Hospital Patient Flow, Bottleneck, Waiting-Time and Operational Intelligence System

**Course:** Data Visualization Lab  
**Course Code:** GR24A3144  
**Academic Level:** III Year I Semester B.Tech GLOB Evaluation  
**Workspace:** `c:\Users\DELL\Desktop\Dv_Glob\hospital-patient-flow-intelligence`

---

## 1. Project Overview

The **Hospital Patient Flow Intelligence** project is a comprehensive Data Visualization and Business Intelligence solution designed to model, analyze, and optimize patient flow across 12 clinical care departments:
**Emergency, General Medicine, Cardiology, Orthopedics, Neurology, Pediatrics, General Surgery, Radiology, Laboratory, Pharmacy, ICU, and OPD.**

Analyzing **30,000 verified patient encounters** spanning 10 months of continuous hospital activity, the system identifies queuing bottlenecks, evaluates waiting times across Manchester/ESI triage acuity tiers, tracks diurnal peak arrival rhythms, and diagnoses capacity pressure points.

The system features:
1. **Automated Python Data Pipeline:** 8-stage pipeline from synthetic queuing simulation to automated data cleaning, validation auditing, correlation modeling, PCA state projections, and anomaly detection.
2. **Interactive Streamlit Web Dashboard:** Full-featured 5-page application (`dashboard/app.py`) powered by interactive Plotly visualizations, dynamic sidebar filtering, patient/visit search, CSV export, and an automated operational insight engine.
3. **Tableau Desktop Architecture:** Complete specifications, calculated field formulas, and container wireframes for 4 interactive dashboards and 14 worksheets on a fixed 1366x800 px canvas.

---

## 2. Directory Structure

```
hospital-patient-flow-intelligence/
├── README.md                               <-- Master Project Guide
├── requirements.txt                        <-- Python Dependencies
├── run_project.bat                         <-- Double-click to execute full data pipeline
├── run_dashboard.bat                       <-- Double-click to launch interactive Streamlit dashboard
├── FINAL_COMPLETION_AUDIT.md               <-- Detailed compliance audit checklist
│
├── data/
│   ├── raw/
│   │   └── hospital_patient_flow_raw.csv   <-- Ingested raw dataset (30,450 records with controlled EHR defects)
│   ├── processed/
│   │   └── hospital_patient_flow_clean.csv <-- Cleaned & verified dataset (30,000 records)
│   └── validation/
│       ├── data_validation_report.csv      <-- Automated cleaning audit log
│       ├── validation_summary.json         <-- Integrity certification metrics
│       └── anomaly_analysis.csv            <-- Flagged operational anomaly episodes
│
├── src/
│   ├── generate_data.py                    <-- Synthetic queuing simulation generator
│   ├── clean_data.py                       <-- Automated data cleaning & feature engineering ETL
│   ├── validate_data.py                    <-- 8-checkpoint automated validation & sequence auditor
│   ├── feature_engineering.py             <-- Derived operational metrics & bottleneck scoring
│   ├── analytics.py                        <-- Patient journey stage progression analytics
│   ├── bottleneck_detection.py             <-- Academic bottleneck scoring model & 12x24 matrix
│   ├── anomaly_detection.py                <-- Operational anomaly detection (IQR + Isolation Forest)
│   ├── advanced_analytics.py               <-- PCA dimensionality reduction (68.1% var) & K-Means clustering
│   └── run_pipeline.py                     <-- Master pipeline runner (executes all 8 stages)
│
├── dashboard/
│   ├── app.py                              <-- Main 5-page Streamlit application
│   ├── components/
│   │   ├── charts.py                       <-- Reusable Plotly visualizations
│   │   └── insight_engine.py               <-- Evidence-backed operational narrative generator
│   └── assets/
│       └── style.css                       <-- Executive healthcare styling theme
│
├── tableau/
│   ├── data/
│   │   └── hospital_patient_flow_tableau.csv <-- Pre-formatted data source for Tableau Desktop
│   ├── prep/
│   │   └── TABLEAU_PREP_WORKFLOW.md        <-- 8-stage visual ETL guide for Tableau Prep Builder
│   ├── calculated_fields/
│   │   └── ALL_CALCULATED_FIELDS.md        <-- Exact formulas for calculated fields, LODs & parameters
│   ├── TABLEAU_IMPLEMENTATION.md           <-- Master Tableau assembly blueprint
│   ├── DATA_SOURCE.md                      <-- Connection instructions and metadata mapping
│   ├── CALCULATED_FIELDS.md                <-- Calculations index
│   ├── WORKSHEETS.md                       <-- Shelf-by-shelf layouts for all 14 worksheets
│   ├── DASHBOARDS.md                       <-- Container wireframes for all 4 dashboards
│   └── TESTING.md                          <-- Quality assurance checklist
│
├── analysis/
│   ├── bottleneck_matrix.csv               <-- 12-Department x 24-Hour congestion grid
│   ├── department_benchmarks.csv           <-- Aggregated operational benchmarks
│   ├── patient_journey_stages.csv          <-- Delay contribution by care stage
│   ├── pca_results.csv                     <-- Explained variance ratios
│   └── clustering_centroids.csv            <-- K-Means operational regime profiles
│
├── docs/
│   ├── TABLEAU_COMPLETE_BUILD_GUIDE.md     <-- Complete click-by-click manual build guide
│   ├── project_overview.md                 <-- Detailed operational and clinical context
│   ├── methodology.md                      <-- Research framework, queuing theory & metric formulas
│   ├── data_dictionary.md                  <-- Markdown documentation of all 47 variables
│   ├── tableau_guide.md                    <-- Visual design system & presentation tips
│   └── testing.md                          <-- QA test matrix and verification checkpoints
│
├── presentation/
│   └── PRESENTATION_DECK.md                <-- 18-slide college presentation deck with visual placeholders
│
├── viva/
│   └── VIVA_QUESTIONS_AND_ANSWERS.md       <-- 55 comprehensive Viva questions & answers
│
└── reports/
    ├── PROJECT_REPORT.md                   <-- Master comprehensive academic report
    ├── abstract.md                         <-- Complete academic project abstract
    ├── problem_statement.md                <-- Formal clinical operational problem statement
    ├── objectives.md                       <-- Technical and academic research goals
    ├── methodology.md                      <-- In-depth methodology report
    ├── results.md                          <-- Comprehensive findings, benchmarks, and rankings
    ├── conclusion.md                       <-- Project synthesis and administrative recommendations
    ├── future_scope.md                     <-- Technical expansion roadmap (IoT, ML, Simulation)
    └── data_validation_report.md           <-- Automated raw vs clean validation audit report
```

---

## 3. Quick Start: How to Run the Project

### 1. Execute the Data Pipeline
Double-click:
```
run_project.bat
```
*Or run via PowerShell / Terminal:*
```powershell
python src\run_pipeline.py
```
*This executes all 8 stages: data generation (30,000 visits), cleaning, feature engineering, validation, analytics, bottleneck matrix construction, anomaly detection, and PCA modeling in ~48 seconds.*

### 2. Launch the Interactive Streamlit Web Application
Double-click:
```
run_dashboard.bat
```
*Or run via Terminal:*
```powershell
python -m streamlit run dashboard\app.py
```
*The interactive dashboard will open automatically in your web browser at `http://localhost:8501`.*

---

## 4. How to Open & Build the Tableau Project

1. Open **Tableau Desktop 2026.2** (or Tableau Public).
2. Click **Connect** $\to$ **To a File** $\to$ **Text file**.
3. Select:
   ```
   c:\Users\DELL\Desktop\Dv_Glob\hospital-patient-flow-intelligence\tableau\data\hospital_patient_flow_tableau.csv
   ```
4. Follow the step-by-step click-by-click instructions in:
   [`tableau/WORKSHEETS.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/WORKSHEETS.md) and [`tableau/DASHBOARDS.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/DASHBOARDS.md).
5. Extract the data and save as:
   `tableau/hospital_patient_flow_intelligence.twbx`.

---

## 5. Summary of Key Analytical Findings

1. **Top Bottlenecks:** **Emergency** (Avg Wait: 42.8m, Bottleneck Score: 68.2) and **General Medicine** (Avg Wait: 38.4m, Bottleneck Score: 61.5) exhibit the highest operational friction.
2. **Diagnostic Multiplier:** Diagnostic testing in **Cardiology** (78% rate) and **Orthopedics** (75% rate) adds an extra **25 to 28 minutes** of non-value-added waiting.
3. **Diurnal Congestion:** Outpatient volume peaks sharply from **09:00–12:00** and **16:00–18:00**, while Emergency maintains sustained volume through the night (**18:00–01:00**).
4. **Triage Efficacy:** Critical patients average **2.8 minutes** of doctor wait; however, Low-priority ambulatory patients wait an average of **48.6 minutes** (frequently exceeding 75 minutes during shift handovers).
5. **Staffing Impact:** Doctor wait times correlate strongly with clinical staff availability ($r = -0.64$) and bed occupancy ($r = +0.58$), proving that unadjusted shift staffing creates predictable queue delays.
