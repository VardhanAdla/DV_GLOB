# Master Viva Examination Guide: 55 Questions & Answers
## Hospital Patient Flow Intelligence
**Course:** Data Visualization Lab (Course Code: GR24A3144)  
**Academic Level:** III Year I Semester B.Tech GLOB Evaluation  

---

### Category 1: Project Scope, Healthcare Domain & Patient Flow (Q1 - Q8)

#### Q1: What is the primary objective of the "Hospital Patient Flow Intelligence" project?
**Answer:** The primary objective is to analyze and visualize how patients move through a multi-stage hospital care network (Arrival $\to$ Registration $\to$ Triage $\to$ Doctor $\to$ Diagnostics $\to$ Treatment $\to$ Pharmacy $\to$ Discharge) and identify operational bottlenecks, waiting-time disparities, peak congestion hours, and capacity pressure points to support administrative decision-making.

#### Q2: How does this project differ from a typical Hospital Management System (HMS)?
**Answer:** An HMS is an operational transactional system designed for patient check-in, billing, prescription entry, and administrative record-keeping. This project is a visual analytics and business intelligence system that evaluates operational efficiency, waiting delays, queuing bottlenecks, and capacity utilization across multiple care units.

#### Q3: Why is synthetic data used instead of real hospital patient records?
**Answer:** Real electronic health records contain protected health information (PHI) governed by strict privacy laws (such as HIPAA). Synthetic data enables rigorous modeling of clinical queuing, priority tiers, and operational surges without privacy or ethical risks.

#### Q4: What are the 12 clinical care departments modeled in this project?
**Answer:** Emergency, General Medicine, Cardiology, Orthopedics, Neurology, Pediatrics, General Surgery, Radiology, Laboratory, Pharmacy, ICU, and OPD (Outpatient Department).

#### Q5: What is the clinical difference between Outpatient (OPD) and Emergency presentation curves?
**Answer:** Outpatient presentations follow a bi-modal diurnal schedule peaking during clinic hours (09:00–12:00 and 16:00–18:00). In contrast, Emergency presentations operate 24 hours a day with sustained volume during late evening and night shifts (18:00–01:00) and elevated trauma admissions on weekends.

#### Q6: How is clinical triage acuity classified in your dataset?
**Answer:** Triage acuity follows the Manchester Triage System / Emergency Severity Index (ESI) 4-tier model: Critical (immediate attention), High (urgent assessment), Medium (semi-urgent), and Low (non-urgent ambulatory).

#### Q7: What is Left Without Being Seen (LWBS), and why is it an important metric?
**Answer:** LWBS refers to patients who register but walk out before physician examination due to excessive waiting delays. It signifies acute operational failure, represents lost hospital revenue, and carries significant clinical liability if an untreated patient deteriorates.

#### Q8: What care stage was identified as the single largest contributor to total encounter delays?
**Answer:** Doctor consultation waiting time was the largest contributor, accounting for 38.5% of cumulative hospital waiting time, followed by diagnostic imaging and laboratory turnaround (24.2%).

---

### Category 2: Data Engineering, Cleaning & Validation (Q9 - Q16)

#### Q9: What data quality issues were intentionally injected into the raw dataset?
**Answer:** 450 duplicate visits, inconsistent date formats (`YYYY-MM-DD` vs `DD/MM/YYYY`), ISO `T` timestamp delimiters, department and gender acronym mismatches (`EMERGENCY` vs `ER`, `Paediatrics` vs `Pediatrics`), negative wait times (-15m), inverted chronological sequences (consultation before triage), and typographical outliers (9999m wait).

#### Q10: How did your cleaning pipeline handle duplicate visits?
**Answer:** The script `clean_data.py` deduplicated records using primary key `Visit_ID` with `keep='first'`, successfully pruning all 450 redundant records while retaining the original 30,000 unique visits.

#### Q11: How were negative waiting times detected and resolved?
**Answer:** Negative wait times resulting from unsynchronized workstation clocks were identified via conditional filtering (`Wait_Doctor < 0`) and re-anchored to median queue durations stratified by clinical priority (Critical: 3m, High: 14m, Medium: 32m, Low: 48m).

#### Q12: How were chronological timestamp inversions repaired?
**Answer:** When an encounter logged `Doctor_Start_Time < Triage_Time`, the script recalculated `Doctor_Start_Time = Triage_Time + Wait_Doctor` and advanced subsequent treatment timestamps to preserve physical sequence integrity.

#### Q13: What method was used to handle typographical outliers such as a 9999-minute wait?
**Answer:** Outliers exceeding physical operational limits (>500 minutes) were winsorized (capped) at the 99th percentile queue duration (120 minutes), preserving the observation while preventing statistical distortion.

#### Q14: How were missing demographic fields imputed?
**Answer:** Missing `Age` and `Gender` values were imputed using clinical context: missing ages in Pediatrics were assigned to the 0–17 bracket, while missing values in adult clinics were imputed to modal demographic brackets.

#### Q15: What checks were included in the automated validation report?
**Answer:** Uniqueness of `Visit_ID`, missing critical fields, domain vocabulary conformance, non-negative wait times, chronological order (`Arrival <= Triage <= Doctor <= Discharge`), and outlier boundaries.

#### Q16: What is the final certified size and structure of the processed dataset?
**Answer:** Exactly 30,000 encounter rows across 47 operational, demographic, temporal, and clinical attributes.

---

### Category 3: The Bottleneck Model & Operational Metrics (Q17 - Q24)

#### Q17: What is the exact formula for your Bottleneck Score?
**Answer:**
$$\text{Bottleneck Score} = 0.40 \times \text{Wait Pressure} + 0.30 \times \text{Capacity Pressure} + 0.20 \times \text{Volume Pressure} + 0.10 \times \text{Staff Strain}$$
All components are normalized to a 0–100 scale, producing a composite index between 0 and 100.

#### Q18: What mandatory disclaimer must accompany the Bottleneck Score?
**Answer:** *"This is an academic analytical model and is not a clinically validated hospital standard."*

#### Q19: What are the four performance tiers of the Bottleneck Score?
**Answer:**
* **Low (<35.0):** Optimal flow with surplus capacity.
* **Moderate (35.0–49.9):** Manageable queue under standard operations.
* **High (50.0–69.9):** High congestion approaching unit saturation.
* **Critical ($\ge$70.0):** Severe operational bottleneck requiring surge intervention.

#### Q20: How is Department Utilization calculated?
**Answer:**
$$\text{Department Utilization} = \frac{\text{Department Capacity} - \text{Available Beds}}{\text{Department Capacity}}$$
It reflects the proportion of active beds or treatment chairs occupied at the time of patient presentation.

#### Q21: How is Capacity Pressure defined?
**Answer:** Capacity Pressure measures operational strain by evaluating bed utilization against staff density:
$$\text{Capacity Pressure} = \text{Utilization} \times \left(\frac{\text{Capacity}}{\text{Staff Available} \times 4}\right)$$

#### Q22: What is Patient Throughput in your operational framework?
**Answer:** Patient Throughput estimates the encounter completion velocity per clinical chair/bed per hour:
$$\text{Throughput} = \frac{60}{\text{Length of Stay} / 3}$$

#### Q23: Why is Length of Stay (LOS) longer than Total Waiting Time?
**Answer:** Total Waiting Time measures non-value-added delays in waiting queues. Length of Stay includes waiting time PLUS active clinical service time (consultation duration, diagnostic scanning, medical therapy, and administrative discharge processing).

#### Q24: Which department registered the highest average Bottleneck Score in your analysis?
**Answer:** Emergency registered the highest score (68.2), followed closely by General Medicine (61.5).

---

### Category 4: Tableau Architecture, Worksheets & Dashboards (Q25 - Q34)

#### Q25: What are the 4 major Tableau dashboards designed in this project?
**Answer:**
1. **Dashboard 1:** Hospital Flow Overview
2. **Dashboard 2:** Department Bottleneck Analysis
3. **Dashboard 3:** Patient Journey & Waiting Time
4. **Dashboard 4:** Operational Intelligence

#### Q26: What standard canvas dimension was used across all dashboards and why?
**Answer:** A fixed canvas size of 1366 x 800 pixels was selected to guarantee consistent layout alignment, prevent horizontal scrollbars, and ensure legibility across standard evaluation displays.

#### Q27: What is the purpose of Dashboard 1 (Hospital Flow Overview)?
**Answer:** It serves as an executive operational pulse, displaying top-level KPI metric cards, 24-hour diurnal arrival curves (Emergency vs OPD), department volume rankings, and triage priority distribution donuts.

#### Q28: How does the Scatter Plot on Dashboard 2 help identify bottlenecks?
**Answer:** It plots Hourly Volume on the X-axis against Average Doctor Wait on the Y-axis, sizing bubbles by Department Capacity and coloring by Bottleneck Category. This forms a 4-quadrant matrix where the upper-right quadrant isolates high-volume, high-delay bottleneck departments.

#### Q29: What is the 12x24 Congestion Heatmap on Dashboard 2?
**Answer:** It is a matrix plotting 12 clinical departments on rows against 24 arrival hours on columns, colored by average Bottleneck Score using a reversed diverging palette (red indicating severe delays).

#### Q30: What is visualized on Dashboard 3 (Patient Journey)?
**Answer:** A care stage progression funnel showing patient volumes across each stage, a stacked bar chart showing cumulative waiting delays per department, and box plots showing length-of-stay dispersion by priority.

#### Q31: What is the parameter-driven feature on Dashboard 4 (Operational Intelligence)?
**Answer:** The parameter `[Select Analysis Metric]` allows users to dynamically switch the primary time-series chart among Patient Volume, Waiting Time, LOS, Emergency %, Capacity Pressure, Department Utilization, and Bottleneck Score.

#### Q32: What is the difference between a `.twb` and a `.twbx` file in Tableau?
**Answer:** A `.twb` (Tableau Workbook) is an XML file storing dashboard layouts, connections, and metadata without embedding the data. A `.twbx` (Tableau Packaged Workbook) is a compressed ZIP archive bundling the `.twb` along with local data sources (`.hyper` or `.csv`) and custom images, making it fully portable.

#### Q33: Why did the previous programmatically generated `.twb` fail with XML schema errors?
**Answer:** Tableau workbook XML uses proprietary, version-dependent schema definitions. Manually constructing XML without Tableau Desktop's internal serializer risks omitting required child tags or inserting disallowed tags (such as unformatted `<window>` elements), triggering parser errors like `D2E8DA72`.

#### Q34: What is the correct, safe procedure to generate a validated Tableau workbook?
**Answer:** Open Tableau Desktop, connect to the verified dataset `tableau/data/hospital_patient_flow_tableau.csv`, author the calculations and worksheets following the build guide, assemble the dashboards, extract the data, and save natively as a `.twbx` file.

---

### Category 5: Tableau Calculations, LODs & Interactivity (Q35 - Q42)

#### Q35: What is a Level of Detail (LOD) expression in Tableau?
**Answer:** An LOD expression allows users to compute values at a different level of granularity than the visualization view. The three types are `FIXED`, `INCLUDE`, and `EXCLUDE`.

#### Q36: How did you implement the Peak Arrival Hour using a FIXED LOD expression?
**Answer:**
```tableau
{ FIXED : 
    ATTR(
        IF { FIXED [Hour] : COUNTD([Visit_ID]) } = 
           { FIXED : MAX({ FIXED [Hour] : COUNTD([Visit_ID]) }) } 
        THEN [Hour] 
        END
    )
}
```
This isolates the single hour with maximum hospital-wide arrivals regardless of worksheet filtering.

#### Q37: How does a Tableau Parameter differ from a Filter?
**Answer:** A filter removes rows from the underlying query based on dimension or measure values. A parameter is a dynamic workbook variable (string, number, date) that can be referenced in calculated fields, reference lines, and SQL queries to alter visualization logic dynamically.

#### Q38: How does the dynamic metric calculation work in Tableau?
**Answer:** It uses a `CASE` statement evaluating the string parameter `[Select Analysis Metric]` to return the corresponding measure (`COUNTD([Visit_ID])`, `AVG([Wait_Doctor])`, `AVG([Length_of_Stay])`, etc.).

#### Q39: What is a Filter Action in Tableau?
**Answer:** A Filter Action sends data values from a selected mark on a source worksheet to filter data on target worksheets across the dashboard (e.g., clicking on "Emergency" filters all other charts to Emergency cases).

#### Q40: What is a Highlight Action in Tableau?
**Answer:** A Highlight Action dims unselected marks while emphasizing marks matching the selected dimension (e.g., hovering over Hour 10 highlights Hour 10 arrivals across all department curves).

#### Q41: How do you format a dual-axis Donut Chart in Tableau?
**Answer:** Create two dummy measures `MIN(1)` on Columns. Set the first mark to Pie (encoding slice angle by patient count and color by priority). Set the second mark to Circle (colored white, slightly smaller radius). Enable Dual Axis and Synchronize Axis to hollow out the center.

#### Q42: What reference line was added to the Department Wait Time Bar Chart?
**Answer:** A constant reference line at 45 minutes on the X-axis labeled "Hospital SLA Target (45 min)" to highlight departments operating outside standard operational tolerances.

---

### Category 6: Advanced Analytics, PCA & Anomaly Detection (Q43 - Q48)

#### Q43: What is Principal Component Analysis (PCA) and why was it applied?
**Answer:** PCA is an unsupervised dimensionality reduction technique that transforms correlated operational variables into orthogonal, uncorrelated principal components. It was used to reduce 6 operational dimensions down to 2 axes to visualize overall hospital operational states.

#### Q44: What percentage of system variance was explained by the first two principal components?
**Answer:** PC1 explained 43.7% and PC2 explained 24.4%, capturing a cumulative **68.1%** of total system variance.

#### Q45: How were operational states segmented using K-Means Clustering?
**Answer:** K-Means ($k=4$) segmented operations into four distinct regimes:
1. Optimal Balanced Flow
2. Morning Outpatient Queue Surge
3. Severe Emergency & Bed Depletion Overload
4. Ancillary Diagnostic Stagnation

#### Q46: How does Interquartile Range (IQR) outlier detection work in this project?
**Answer:** For consultation wait times, the upper boundary was set at $Q_3 + 1.5 \times \text{IQR}$. Encounters exceeding this threshold represent non-random queue stagnation.

#### Q47: What is Isolation Forest and why was it used for anomaly detection?
**Answer:** Isolation Forest is an unsupervised tree-based ensemble algorithm that isolates anomalies by randomly partitioning feature space. Data points requiring fewer splits are flagged as anomalies. It was applied across 4 multi-dimensional operational metrics.

#### Q48: What specific real-world surge scenarios were flagged by anomaly detection?
**Answer:**
1. **May 10–16 Trauma Outbreak:** Emergency presentations surged to 34.8% (baseline: 20.3%), depleting bed availability to 1.2 beds and expanding average wait times to 56.4 minutes.
2. **July 15–25 Monsoon Epidemic:** Inflow in Pediatrics and General Medicine increased by 78%, generating severe consultation backlogs.

---

### Category 7: Streamlit Application, Plotly & Software Engineering (Q49 - Q55)

#### Q49: What are the 5 pages of your interactive Streamlit application?
**Answer:**
1. **Overview:** Executive KPIs, diurnal arrival curves, department volume bars, and automated insights.
2. **Department Bottlenecks:** Volume vs Wait scatter plot, 12x24 congestion heatmap, and ranking tables.
3. **Patient Journey:** Stage delay funnel and length-of-stay boxplots.
4. **Operational Intelligence:** Parameter-driven dynamic trend viewer and anomaly alert logs.
5. **Data Explorer:** Searchable patient/visit audit tool with filtered CSV export.

#### Q50: What is the role of Plotly in your Streamlit application?
**Answer:** Plotly generates interactive, responsive, web-based JavaScript charts supporting hover tooltips, zoom, pan, and legend toggling.

#### Q51: How does the Automated Insight Engine work in `app.py`?
**Answer:** It evaluates filtered cohort metrics against clinical operational thresholds (e.g., checking if wait times exceed 38 minutes while utilization exceeds 75%) and dynamically renders cautious, evidence-backed narrative observations.

#### Q52: What is the purpose of `@st.cache_data` in Streamlit?
**Answer:** `@st.cache_data` caches the 30,000-record dataset in memory after initial loading, preventing redundant disk reads and ensuring responsive filter execution.

#### Q53: What do the scripts `run_project.bat` and `run_dashboard.bat` do?
**Answer:**
* `run_project.bat` executes the 8-stage data generation, cleaning, validation, and analytics pipeline in sequence.
* `run_dashboard.bat` launches the interactive Streamlit application on `http://localhost:8501`.

#### Q54: What key administrative recommendations emerged from this project?
**Answer:**
1. Implement overlapping 10-hour clinical shifts to maintain staffing during the 10:00–12:00 and 19:00–21:00 arrival peaks.
2. Establish a rapid-assessment fast-track in Emergency for Low/Medium acuity cases.
3. Deploy satellite point-of-care cardiac and imaging testing in Cardiology and Orthopedics.

#### Q55: What are the primary future enhancements planned for this system?
**Answer:** Ingesting live spatial RFID/BLE patient tracking telemetry, training machine learning models (XGBoost/LSTM) to predict queue delays 2 hours in advance, and integrating SimPy discrete-event simulation for real-time "what-if" capacity modeling.
