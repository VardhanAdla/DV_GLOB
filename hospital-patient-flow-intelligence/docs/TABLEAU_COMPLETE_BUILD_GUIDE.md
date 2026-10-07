# Comprehensive Tableau Manual Build Guide
## Hospital Patient Flow Intelligence
**Course:** Data Visualization Lab (Course Code: GR24A3144)  
**Target Environment:** Tableau Desktop 2021.4+ / Tableau Public  
**Primary Dataset:** `data/processed/hospital_patient_flow_clean.csv` (30,000 records)

---

## Table of Contents
1. [Connecting Data & Setting Up Metadata](#1-connecting-data--setting-up-metadata)
2. [Step-by-Step Creation of Calculated Fields](#2-step-by-step-creation-of-calculated-fields)
3. [Building Worksheets (Exact Click-by-Click Instructions)](#3-building-worksheets)
   - [Sheet 1: KPI - Total Patients](#sheet-1-kpi---total-patients)
   - [Sheet 2: KPI - Average Doctor Wait Time](#sheet-2-kpi---average-doctor-wait-time)
   - [Sheet 3: KPI - Average Length of Stay](#sheet-3-kpi---average-length-of-stay)
   - [Sheet 4: KPI - Emergency Inflow Percentage](#sheet-4-kpi---emergency-inflow-percentage)
   - [Sheet 5: Hourly Patient Arrival Patterns](#sheet-5-hourly-patient-arrival-patterns)
   - [Sheet 6: Department Patient Volume & Bottleneck](#sheet-6-department-patient-volume--bottleneck)
   - [Sheet 7: Priority Level Acuity Distribution](#sheet-7-priority-level-acuity-distribution)
   - [Sheet 8: Department Waiting Time Benchmarking](#sheet-8-department-waiting-time-benchmarking)
   - [Sheet 9: Volume vs Waiting Time Scatter Plot](#sheet-9-volume-vs-waiting-time-scatter-plot)
   - [Sheet 10: Department Hourly Bottleneck Heatmap](#sheet-10-department-hourly-bottleneck-heatmap)
   - [Sheet 11: Patient Journey Progression Funnel](#sheet-11-patient-journey-progression-funnel)
   - [Sheet 12: Stage Duration Decomposition (Stacked Bar)](#sheet-12-stage-duration-decomposition-stacked-bar)
   - [Sheet 13: Length of Stay Distribution by Priority](#sheet-13-length-of-stay-distribution-by-priority)
   - [Sheet 14: Dynamic Operational Trend](#sheet-14-dynamic-operational-trend)
4. [Assembling the 4 Interactive Dashboards](#4-assembling-the-4-interactive-dashboards)
   - [Dashboard 1: Hospital Flow Overview](#dashboard-1-hospital-flow-overview)
   - [Dashboard 2: Department Bottleneck Analysis](#dashboard-2-department-bottleneck-analysis)
   - [Dashboard 3: Patient Journey & Waiting Time](#dashboard-3-patient-journey--waiting-time)
   - [Dashboard 4: Operational Intelligence](#dashboard-4-operational-intelligence)
5. [Configuring Interactive Dashboard Actions & Filters](#5-configuring-interactive-dashboard-actions--filters)
6. [Exporting, Publishing & Presentation Preparation](#6-exporting-publishing--presentation-preparation)

---

# 1. Connecting Data & Setting Up Metadata

1. Launch **Tableau Desktop** (or **Tableau Public**).
2. On the startup blue left pane, under **Connect** -> **To a File**, click **Text file**.
3. In the file explorer, navigate to:
   ```
   c:\Users\DELL\Desktop\Dv_Glob\hospital-patient-flow-intelligence\data\processed\
   ```
4. Select `hospital_patient_flow_clean.csv` and click **Open**.
5. In the **Data Source** tab:
   * Verify the table displays **30,000 rows**.
   * Verify data types in the column headers:
     * `Arrival_Date`: Calendar icon (**Date**)
     * `Arrival_Time`: Globe or text (**String**)
     * `Hour`: `#` (**Number - Whole**)
     * `Department`, `Patient_Type`, `Priority_Level`, `Age_Group`, `Gender`: `Abc` (**String**)
     * `Registration_Wait_Time`, `Triage_Wait_Time`, `Doctor_Wait_Time`, `Total_Waiting_Time`, `Total_Length_of_Stay`: `#` (**Number - Whole**)
     * `Bed_Occupancy_Rate`, `Bottleneck_Score`: `#` (**Number - Decimal**)
6. Click the orange tab **Sheet 1** at the bottom left to enter the worksheet canvas.

---

# 2. Step-by-Step Creation of Calculated Fields

In the left **Data** pane, click the small down arrow next to the search bar (or right-click any blank space in the Data pane) and select **Create Calculated Field...**

### Calculation 1: `Emergency Patient Inflow %`
* **Name:** `Emergency Patient Inflow %`
* **Formula:**
  ```tableau
  SUM(IIF([Patient_Type] = 'Emergency', 1, 0)) / COUNTD([Visit_ID])
  ```
* **Format:** Right-click the newly created field in the Data pane -> **Default Properties** -> **Number Format...** -> Select **Percentage**, set decimal places to `1`.

### Calculation 2: `Diagnostic Utilization Rate`
* **Name:** `Diagnostic Utilization Rate`
* **Formula:**
  ```tableau
  SUM(IIF([Diagnostic_Required] = 'Yes', 1, 0)) / COUNTD([Visit_ID])
  ```
* **Format:** Default Number Format -> **Percentage**, decimal places `1`.

### Calculation 3: `Bottleneck Score (Analytical)`
* **Name:** `Bottleneck Score (Analytical)`
* **Formula:**
  ```tableau
  MIN(40.0, (AVG([Doctor_Wait_Time]) / 75.0) * 40.0)
  +
  (AVG([Bed_Occupancy_Rate]) * 35.0)
  +
  MIN(25.0, (AVG([Department_Capacity]) / (AVG([Staff_Availability]) * 4.0)) * 12.5)
  ```
* **Format:** Default Number Format -> **Number (Custom)** -> Decimal places `1`.

### Calculation 4: `Bottleneck Severity Tier`
* **Name:** `Bottleneck Severity Tier`
* **Formula:**
  ```tableau
  IF [Bottleneck_Score] >= 70.0 THEN 'Severe Bottleneck'
  ELSEIF [Bottleneck_Score] >= 50.0 THEN 'Moderate Congestion'
  ELSEIF [Bottleneck_Score] >= 35.0 THEN 'Manageable Flow'
  ELSE 'Optimal Flow'
  END
  ```

### Calculation 5: Parameter `[Select Analysis Metric]`
* Click the down arrow next to Data Search -> **Create Parameter...**
* **Name:** `Select Analysis Metric`
* **Data Type:** `String`
* **Allowable values:** `List`
* Add values to the list:
  1. `Patient Volume`
  2. `Average Waiting Time`
  3. `Average Length of Stay`
  4. `Emergency Inflow %`
  5. `Capacity Pressure`
* Click **OK**. Right-click the parameter and select **Show Parameter**.

### Calculation 6: `Dynamic Selected Metric`
* **Name:** `Dynamic Selected Metric`
* **Formula:**
  ```tableau
  CASE [Select Analysis Metric]
      WHEN 'Patient Volume' THEN COUNTD([Visit_ID])
      WHEN 'Average Waiting Time' THEN AVG([Doctor_Wait_Time])
      WHEN 'Average Length of Stay' THEN AVG([Total_Length_of_Stay])
      WHEN 'Emergency Inflow %' THEN SUM(IIF([Patient_Type] = 'Emergency', 1, 0)) / COUNTD([Visit_ID]) * 100
      WHEN 'Capacity Pressure' THEN AVG([Bed_Occupancy_Rate]) * 100
  END
  ```

---

# 3. Building Worksheets

---

### Sheet 1: KPI - Total Patients
* **Worksheet Name:** `KPI_Total_Patients`
* **Purpose:** High-level metric card displaying total patient volume.
* **Columns:** *(Leave empty)*
* **Rows:** *(Leave empty)*
* **Marks Card:**
  * Drag `Visit_ID` to **Text**.
  * Click the pill on Text -> Select **Measure** -> **Count (Distinct)** (`COUNTD`).
* **Text Formatting:**
  * Click **Text** on Marks -> Click the `...` button.
  * In the editor, type:
    ```
    <Distinct count of Visit_ID>
    TOTAL PATIENT VISITS
    ```
  * Select the top number: Font **Segoe UI / Tableau Bold**, Size **26pt**, Color **#1b6ca8** (Navy Blue).
  * Select the label below: Font Size **9pt**, Bold, Color **#777777**.
* **Dashboard Placement:** Dashboard 1 (KPI Row, Column 1).

---

### Sheet 2: KPI - Average Doctor Wait Time
* **Worksheet Name:** `KPI_Avg_Wait_Time`
* **Purpose:** Display average doctor consultation wait time in minutes.
* **Columns:** *(Leave empty)*
* **Rows:** *(Leave empty)*
* **Marks Card:**
  * Drag `Doctor_Wait_Time` to **Text**.
  * Change aggregation to **Average** (`AVG`).
* **Text Formatting:**
  * Edit Text:
    ```
    <AVG(Doctor_Wait_Time)> min
    AVERAGE DOCTOR WAIT
    ```
  * Number size **26pt**, Color **#d9534f** (Alert Red), label size **9pt**.
* **Dashboard Placement:** Dashboard 1 (KPI Row, Column 2).

---

### Sheet 3: KPI - Average Length of Stay
* **Worksheet Name:** `KPI_Avg_LOS`
* **Purpose:** Display overall hospital encounter duration.
* **Columns:** *(Leave empty)*
* **Rows:** *(Leave empty)*
* **Marks Card:**
  * Drag `Total_Length_of_Stay` to **Text** -> Change aggregation to **Average**.
* **Text Formatting:**
  ```
  <AVG(Total_Length_of_Stay)> min
  AVG LENGTH OF STAY
  ```
  * Number size **26pt**, Color **#2ca02c** (Green), label size **9pt**.
* **Dashboard Placement:** Dashboard 1 (KPI Row, Column 3).

---

### Sheet 4: KPI - Emergency Inflow Percentage
* **Worksheet Name:** `KPI_Emergency_Inflow`
* **Purpose:** Track proportion of acute unscheduled intake.
* **Columns:** *(Leave empty)*
* **Rows:** *(Leave empty)*
* **Marks Card:**
  * Drag `Emergency Patient Inflow %` to **Text**.
* **Text Formatting:**
  ```
  <AGG(Emergency Patient Inflow %)>
  EMERGENCY INTAKE %
  ```
  * Number size **26pt**, Color **#f28e2b** (Orange).
* **Dashboard Placement:** Dashboard 1 (KPI Row, Column 4).

---

### Sheet 5: Hourly Patient Arrival Patterns
* **Worksheet Name:** `Hourly_Arrival_Pattern`
* **Purpose:** 24-hour diurnal curve showing arrival surges.
* **Columns:** Drag `Hour` to Columns.
  * Right-click `Hour` pill -> Select **Dimension** (or **Continuous** integer).
* **Rows:** Drag `Visit_ID` to Rows -> Change to `COUNTD([Visit_ID])`.
* **Color:** Drag `Patient_Type` to **Color** (or create a flag for Emergency vs Other).
* **Chart Type:** In Marks dropdown, select **Line**.
* **Markers:** Click **Color** on Marks -> Under **Effects**, set **Markers** to All (small circle on each hour).
* **Tooltip Configuration:**
  ```
  Hour: <Hour>:00
  Patient Classification: <Patient_Type>
  Total Arrivals: <COUNTD(Visit_ID)>
  ```
* **Dashboard Placement:** Dashboard 1 (Top Left).

---

### Sheet 6: Department Patient Volume & Bottleneck
* **Worksheet Name:** `Department_Volume_Bar`
* **Purpose:** Compare patient intake across clinical departments.
* **Columns:** Drag `Visit_ID` to Columns -> Select `COUNTD([Visit_ID])`.
* **Rows:** Drag `Department` to Rows.
  * Click the sort icon on the axis or right-click `Department` -> **Sort...** -> Sort by **Field: Visit_ID**, Aggregation: **Count (Distinct)**, Order: **Descending**.
* **Color:** Drag `Bottleneck_Category` to **Color**.
  * Edit Colors:
    * `Optimal Flow`: Green (`#5cb85c`)
    * `Manageable Flow`: Light Blue (`#5bc0de`)
    * `Moderate Congestion`: Amber (`#f0ad4e`)
    * `Severe Bottleneck`: Red (`#d9534f`)
* **Label:** Drag `COUNTD([Visit_ID])` to **Label**.
* **Chart Type:** Horizontal Bar.
* **Dashboard Placement:** Dashboard 1 (Top Right).

---

### Sheet 7: Priority Level Acuity Distribution
* **Worksheet Name:** `Priority_Distribution_Donut`
* **Purpose:** Acuity mix breakdown (Critical, High, Medium, Low).
* **Columns:** Double-click Columns and type `MIN(1)`. Repeat to create a second `MIN(1)` pill.
* **Dual Axis:** Right-click the second `MIN(1)` pill -> Check **Dual Axis**.
* **Marks Card 1 (First MIN(1)):**
  * Select **Pie** chart.
  * Drag `Priority_Level` to **Color**.
  * Drag `COUNTD([Visit_ID])` to **Angle**.
  * Set size large.
* **Marks Card 2 (Second MIN(1)):**
  * Select **Circle**.
  * Set color to **White** (`#FFFFFF`).
  * Set size slightly smaller than the outer pie (creating the donut hole).
  * Drag `COUNTD([Visit_ID])` to **Label** -> Centered text.
* **Dashboard Placement:** Dashboard 1 (Bottom Left).

---

### Sheet 8: Department Waiting Time Benchmarking
* **Worksheet Name:** `Department_Wait_Time_Bar`
* **Purpose:** Bar chart ranking departments by doctor waiting time with SLA reference line.
* **Columns:** Drag `Doctor_Wait_Time` to Columns -> Change to `AVG([Doctor_Wait_Time])`.
* **Rows:** Drag `Department` to Rows -> Sort Descending by `AVG([Doctor_Wait_Time])`.
* **Color:** Drag `AVG([Doctor_Wait_Time])` to **Color** (Palette: Orange-Red Diverging).
* **Reference Line:**
  * In the top Analytics pane (left of Data pane), drag **Reference Line** onto **Table**.
  * Line Value: **Constant** = `45`.
  * Label: Custom -> `Hospital SLA (45 min)`.
  * Formatting: Red dashed line.
* **Dashboard Placement:** Dashboard 2 (Top Left).

---

### Sheet 9: Volume vs Waiting Time Scatter Plot
* **Worksheet Name:** `Volume_vs_Wait_Scatter`
* **Purpose:** Multi-dimensional quadrant scatter isolating operational bottleneck units.
* **Columns:** Drag `Visit_ID` to Columns -> `COUNTD([Visit_ID])`.
* **Rows:** Drag `Doctor_Wait_Time` to Rows -> `AVG([Doctor_Wait_Time])`.
* **Detail (Marks):**
  * Drag `Department` to **Detail**.
  * Drag `Hour` to **Detail**.
* **Size:** Drag `Department_Capacity` to **Size** -> `AVG([Department_Capacity])`.
* **Color:** Drag `Bottleneck_Category` to **Color**.
* **Chart Type:** **Circle**.
* **Opacity:** Click **Color** on Marks -> Set opacity to `75%`, Border: Dark grey.
* **Reference Lines:**
  * Add reference line on Y-axis at `45` min (SLA delay line).
* **Dashboard Placement:** Dashboard 2 (Top Right).

---

### Sheet 10: Department Hourly Bottleneck Heatmap
* **Worksheet Name:** `Department_Bottleneck_Heatmap`
* **Purpose:** Granular 12x24 congestion matrix identifying exact peak bottleneck windows.
* **Columns:** Drag `Hour` to Columns -> Set to Discrete (0, 1, ..., 23).
* **Rows:** Drag `Department` to Rows.
* **Marks Card:** Select **Square**.
* **Color:** Drag `Bottleneck_Score` to **Color** -> Change aggregation to `AVG([Bottleneck_Score])`.
  * Palette: **Red-Yellow-Green Diverging** (Check **Reversed** so High score is Dark Red).
* **Label:** Drag `Bottleneck_Score` to **Label** -> `AVG` -> Format to 0 decimals.
* **Dashboard Placement:** Dashboard 2 (Bottom Full Width).

---

### Sheet 11: Patient Journey Progression Funnel
* **Worksheet Name:** `Patient_Journey_Funnel`
* **Purpose:** Progression of patient volume through clinical care stages.
* **Data / Pivot:** Use stage completion counts or load `analysis/patient_flow/stage_funnel_summary.csv`.
* **Columns:** `Count` (Patient Volume).
* **Rows:** `Stage` (1. Arrival, 2. Registration, 3. Triage, 4. Doctor Consult, 5. Diagnostics, 6. Treatment, 7. Pharmacy, 8. Discharge).
* **Color:** `Stage` (Sequential Blue palette).
* **Chart Type:** Horizontal Bar.
* **Label:** `Completion_Pct` displayed on bar tips (e.g. `100%`, `45.2%`).
* **Dashboard Placement:** Dashboard 3 (Left Half).

---

### Sheet 12: Stage Duration Decomposition (Stacked Bar)
* **Worksheet Name:** `Stage_Duration_Breakdown`
* **Purpose:** Break down cumulative waiting delays across stages per department.
* **Columns:** Drag `Department` to Columns.
* **Rows:** Drag `Measure Values` to Rows.
* **Measure Values Filter Shelf:** Keep only:
  * `AVG(Registration_Wait_Time)`
  * `AVG(Triage_Wait_Time)`
  * `AVG(Doctor_Wait_Time)`
  * `AVG(Diagnostic_Wait_Time)`
  * `AVG(Treatment_Wait_Time)`
  * `AVG(Pharmacy_Wait_Time)`
* **Color:** Drag `Measure Names` to **Color**.
* **Chart Type:** **Bar** (Stacked).
* **Dashboard Placement:** Dashboard 3 (Right Top).

---

### Sheet 13: Length of Stay Distribution by Priority
* **Worksheet Name:** `LOS_by_Priority_Boxplot`
* **Purpose:** Dispersion and IQR outlier analysis of encounter length of stay.
* **Columns:** Drag `Priority_Level` to Columns (Order: Critical, High, Medium, Low).
* **Rows:** Drag `Total_Length_of_Stay` to Rows.
* **Detail:** Drag `Visit_ID` to **Detail** (or uncheck Aggregate Measures under Analysis menu).
* **Chart Type:** In **Show Me**, select **Box-and-Whisker Plot**.
* **Color:** Drag `Priority_Level` to **Color**.
* **Dashboard Placement:** Dashboard 3 (Right Bottom).

---

### Sheet 14: Dynamic Operational Trend
* **Worksheet Name:** `Dynamic_Operational_Trend`
* **Purpose:** Parameter-driven time-series reflecting administrator metric selection.
* **Columns:** Drag `Arrival_Date` to Columns -> Right-click -> Select **Day** (Continuous date).
* **Rows:** Drag `Dynamic Selected Metric` to Rows.
* **Chart Type:** **Area** or **Line**.
* **Color:** Solid Steel Blue (`#1b6ca8`).
* **Dashboard Placement:** Dashboard 4 (Top Half).

---

# 4. Assembling the 4 Interactive Dashboards

### Setting Canvas Size
For each dashboard created, in the left **Dashboard** pane under **Size**, click the dropdown and select **Fixed size** -> Set **Width: 1366 px**, **Height: 800 px**.

---

### Dashboard 1: Hospital Flow Overview
1. Click **New Dashboard** icon at the bottom. Rename to `1. Hospital Flow Overview`.
2. Drag a **Vertical Layout Container** into the canvas.
3. **Header:** Drag a **Text Object** to the top:
   * Text: `HOSPITAL PATIENT FLOW INTELLIGENCE | EXECUTIVE OVERVIEW`
   * Font: Tableau Bold, 18pt, White on Dark Blue background (`#0f2e4d`).
4. **KPI Strip:** Drag a **Horizontal Layout Container** below the header.
   * Drag sheets into this container in order:
     1. `KPI_Total_Patients`
     2. `KPI_Avg_Wait_Time`
     3. `KPI_Avg_LOS`
     4. `KPI_Emergency_Inflow`
   * Ensure container is set to **Distribute Contents Evenly**.
5. **Main Visualizations:** Drag a **Horizontal Layout Container** below the KPI strip.
   * Left: Drag `Hourly_Arrival_Pattern`.
   * Right: Drag `Department_Volume_Bar`.
6. **Bottom Row:** Drag a **Horizontal Layout Container** below.
   * Left: Drag `Priority_Distribution_Donut`.
   * Right: Filter panel container containing:
     * Date Slider (`Arrival_Date`)
     * Department Dropdown
     * Priority Level Dropdown

---

### Dashboard 2: Department Bottleneck Analysis
1. Create new dashboard named `2. Department Bottleneck Analysis`.
2. Header: `DEPARTMENT BOTTLENECK & WAITING-TIME ANALYTICS`.
3. Top Half (Horizontal Container):
   * Left (45% width): `Department_Wait_Time_Bar`.
   * Right (55% width): `Volume_vs_Wait_Scatter`.
4. Bottom Half (Vertical Container):
   * Full width: `Department_Bottleneck_Heatmap`.
   * Add text annotation: *"Peak congestion clusters in Emergency and General Medicine during shift handovers (10:00-12:00 and 19:00-21:00)."*

---

### Dashboard 3: Patient Journey & Waiting Time
1. Create new dashboard named `3. Patient Journey & Waiting Time`.
2. Header: `END-TO-END PATIENT JOURNEY & STAGE DELAY DECOMPOSITION`.
3. Left Half (45% width):
   * Drag `Patient_Journey_Funnel`.
4. Right Half (55% width, Vertical Container):
   * Top: `Stage_Duration_Breakdown`.
   * Bottom: `LOS_by_Priority_Boxplot`.

---

### Dashboard 4: Operational Intelligence
1. Create new dashboard named `4. Operational Intelligence`.
2. Header: `HOSPITAL OPERATIONAL INTELLIGENCE & CAPACITY STRESS TESTING`.
3. Sub-header / Parameter Control: Drag Parameter `[Select Analysis Metric]` to the top right.
4. Top Section: `Dynamic_Operational_Trend` (Occupies 50% height).
5. Bottom Section (Horizontal Container):
   * Left: `Hourly_Arrival_Pattern` (with Bed Occupancy overlay).
   * Right: Department Staff Availability vs Bed Depletion table.

---

# 5. Configuring Interactive Dashboard Actions & Filters

To make the workbook interactive and responsive:

### Action 1: Department Cross-Filtering
1. On Dashboard 1, click top menu **Dashboard** -> **Actions...**
2. Click **Add Action** -> **Filter...**
3. Configure:
   * **Name:** `Filter_By_Department`
   * **Source Sheets:** `Department_Volume_Bar`
   * **Run action on:** `Select`
   * **Target Sheets:** Check `Hourly_Arrival_Pattern` and `Priority_Distribution_Donut`.
   * **Clearing the selection will:** `Show all values`.
4. Click **OK**. Now clicking any department bar instantly isolates that department across the dashboard!

### Action 2: Hour Hover Highlight
1. Under **Dashboard** -> **Actions...** -> **Add Action** -> **Highlight...**
2. **Name:** `Highlight_Hour`
3. **Source Sheets:** `Hourly_Arrival_Pattern`
4. **Run action on:** `Hover`
5. **Target Fields:** Selected Fields -> `Hour`.

### Action 3: Scatter Plot Quadrant Drilldown
1. On Dashboard 2, add a **Filter Action**:
   * **Source Sheet:** `Volume_vs_Wait_Scatter`
   * **Run on:** `Select`
   * **Target Sheet:** `Department_Bottleneck_Heatmap`
2. Clicking any dot in the scatter plot highlights the exact department and hour row in the bottleneck heatmap.

---

# 6. Exporting, Publishing & Presentation Preparation

1. **Extract Data (Crucial for Tableau Reader / Public):**
   * Go to **Data Source** tab -> Under top right **Connection**, change from **Live** to **Extract**.
   * Click any sheet tab to create and save the `.hyper` extract.
2. **Save as Packaged Workbook:**
   * Click **File** -> **Save As...** -> Select **Tableau Packaged Workbook (*.twbx)**.
   * This bundles the data extract and workbook together into a single portable file.
3. **Publishing to Tableau Public:**
   * Click **Server** -> **Tableau Public** -> **Save to Tableau Public As...**
   * Log into your free Tableau Public account.
   * Provide title: `Hospital Patient Flow Intelligence - GR24A3144`.
4. **Exporting Presentation Images / PDF:**
   * Click **File** -> **Print to PDF...** -> Under Print, select **Entire Workbook** -> Layout: **Landscape**.
   * Generates a presentation-ready high-resolution PDF for viva submission.
