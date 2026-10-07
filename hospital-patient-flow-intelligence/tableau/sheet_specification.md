# Tableau Worksheet Specifications

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

This document specifies the construction of all 14 individual Tableau worksheets across the 4 dashboards.

---

### Sheet 1: `KPI_Total_Patients`
* **Purpose:** Display overall patient volume with contextual subtitle.
* **Rows:** (Empty)
* **Columns:** (Empty)
* **Text / Mark:** `COUNTD([Visit_ID])`
* **Label Format:** Font 28pt Bold, Color `#1b6ca8`. Subtitle: "Total Patient Encounters (Jan - Oct 2025)"
* **Filters:** All global filters (Date, Department, Priority).

---

### Sheet 2: `KPI_Avg_Wait_Time`
* **Purpose:** Display overall average doctor consultation wait time.
* **Rows:** (Empty)
* **Columns:** (Empty)
* **Text / Mark:** `AVG([Doctor_Wait_Time])`
* **Label Format:** Font 28pt Bold, Color `#d9534f` (if > 40m) or `#333333`. Unit: "Minutes"

---

### Sheet 3: `KPI_Avg_LOS`
* **Purpose:** Display average hospital length of stay across all episodes.
* **Rows:** (Empty)
* **Columns:** (Empty)
* **Text / Mark:** `AVG([Total_Length_of_Stay])`
* **Label Format:** Font 28pt Bold, Color `#2ca02c`. Unit: "Minutes"

---

### Sheet 4: `KPI_Emergency_Inflow`
* **Purpose:** Display percentage of high-acuity emergency presentations.
* **Rows:** (Empty)
* **Columns:** (Empty)
* **Text / Mark:** `[Emergency Patient Inflow %]` (Format as Percentage `0.0%`).
* **Label Format:** Font 28pt Bold, Color `#f28e2b`.

---

### Sheet 5: `Hourly_Arrival_Pattern`
* **Purpose:** Reveal hourly arrival surges and distinguish Emergency from Outpatient flow.
* **Columns:** `[Hour]` (Continuous dimension, range 0 to 23).
* **Rows:** `COUNTD([Visit_ID])`
* **Color:** `[Department = 'Emergency']` or `[Patient_Type]`
* **Mark Type:** Line chart (size medium, markers enabled).
* **Tooltip:**
  ```
  Hour of Day: <Hour>:00
  Patient Type / Department: <Patient_Type>
  Patient Inflow: <COUNTD(Visit_ID)>
  Average Wait: <AVG(Doctor_Wait_Time)> min
  ```
* **Dashboard Placement:** Dashboard 1 (Top Left).

---

### Sheet 6: `Department_Volume_Bar`
* **Purpose:** Compare patient volumes across 12 clinical departments sorted descending.
* **Columns:** `COUNTD([Visit_ID])`
* **Rows:** `[Department]` (Sorted Descending by `COUNTD([Visit_ID])`).
* **Color:** `[Bottleneck_Category]` (Palette: Green, Blue, Orange, Red).
* **Mark Type:** Horizontal Bar.
* **Label:** `COUNTD([Visit_ID])` displayed on end of bars.
* **Dashboard Placement:** Dashboard 1 (Top Right).

---

### Sheet 7: `Priority_Distribution_Donut`
* **Purpose:** Illustrate case-mix acuity distribution (Critical, High, Medium, Low).
* **Columns:** `MIN(1)` (Dual axis for donut hole).
* **Rows:** (Empty)
* **Color:** `[Priority_Level]` (Critical: Red `#d9534f`, High: Orange `#f0ad4e`, Medium: Blue `#5bc0de`, Low: Green `#5cb85c`).
* **Angle:** `COUNTD([Visit_ID])`
* **Mark Type:** Pie / Dual Axis.
* **Dashboard Placement:** Dashboard 1 (Bottom Left).

---

### Sheet 8: `Department_Wait_Time_Bar`
* **Purpose:** Direct comparison of physician waiting times per department with benchmark reference line.
* **Columns:** `AVG([Doctor_Wait_Time])`
* **Rows:** `[Department]` (Sorted Descending by Average Doctor Wait).
* **Color:** `AVG([Doctor_Wait_Time])` (Diverging Red-Blue).
* **Mark Type:** Horizontal Bar.
* **Reference Line:** Constant line at `45 Minutes` labeled "Hospital SLA Target (45 min)".
* **Dashboard Placement:** Dashboard 2 (Top Left).

---

### Sheet 9: `Volume_vs_Wait_Scatter`
* **Purpose:** Core analytical quadrant view identifying high-volume / high-delay bottleneck units.
* **Columns:** `COUNTD([Visit_ID])` (Hourly volume per department).
* **Rows:** `AVG([Doctor_Wait_Time])`
* **Detail:** `[Department]`, `[Hour]`
* **Size:** `AVG([Department_Capacity])`
* **Color:** `[Bottleneck_Category]`
* **Mark Type:** Circle / Shape.
* **Reference Lines:**
  * Average Volume line (X-axis)
  * SLA Wait Threshold line (Y-axis: 45 min)
* **Dashboard Placement:** Dashboard 2 (Top Right).

---

### Sheet 10: `Department_Bottleneck_Heatmap`
* **Purpose:** Granular matrix revealing the exact hours each department encounters severe congestion.
* **Columns:** `[Hour]` (Discrete, 0 to 23).
* **Rows:** `[Department]`
* **Color:** `AVG([Bottleneck_Score])` (Continuous Orange-Red diverging palette).
* **Mark Type:** Square (Heatmap).
* **Label:** `ROUND(AVG([Bottleneck_Score]), 0)`
* **Dashboard Placement:** Dashboard 2 (Bottom Span).

---

### Sheet 11: `Patient_Journey_Funnel`
* **Purpose:** Track progression drop-offs and branch points through hospital stages.
* **Columns:** `[Stage_Completion_Count]` or calculated stage progression metrics.
* **Rows:** `[Encounter_Stage]`
* **Color:** `[Encounter_Stage]`
* **Mark Type:** Horizontal Bar / Funnel.
* **Dashboard Placement:** Dashboard 3 (Left).

---

### Sheet 12: `Stage_Duration_Breakdown`
* **Purpose:** Decompose the patient experience into discrete queue stages across departments.
* **Columns:** `[Department]`
* **Rows:** `Measure Values` (`AVG([Registration_Wait_Time])`, `AVG([Triage_Wait_Time])`, `AVG([Doctor_Wait_Time])`, `AVG([Diagnostic_Wait_Time])`, `AVG([Treatment_Wait_Time])`, `AVG([Pharmacy_Wait_Time])`).
* **Color:** `Measure Names`
* **Mark Type:** Stacked Bar.
* **Dashboard Placement:** Dashboard 3 (Right Top).

---

### Sheet 13: `LOS_by_Priority_Boxplot`
* **Purpose:** Statistical dispersion of total length of stay by clinical priority.
* **Columns:** `[Priority_Level]`
* **Rows:** `[Total_Length_of_Stay]`
* **Mark Type:** Circle / Box Plot.
* **Dashboard Placement:** Dashboard 3 (Right Bottom).

---

### Sheet 14: `Dynamic_Operational_Trend`
* **Purpose:** Parameter-driven interactive time-series adapting to the administrator's selection.
* **Columns:** `[Arrival_Date]` (Daily or Weekly continuous).
* **Rows:** `[Dynamic Selected Metric]`
* **Color:** `[Bottleneck_Category]` or single executive navy `#1b6ca8`.
* **Mark Type:** Line chart with area fill underneath.
* **Dashboard Placement:** Dashboard 4 (Top Half).
