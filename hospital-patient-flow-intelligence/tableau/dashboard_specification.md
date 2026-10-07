# Tableau Dashboard Architecture & Specifications

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  
**Standard Canvas Size:** Fixed 1366 x 800 px (Optimized for desktop presentation & evaluation)  
**Visual Style:** Clean Executive Healthcare Analytics (Slate Blue, Forest Green, Coral Red, Off-White `#F8F9FA`)  

---

## 1. Dashboard 1: "Hospital Flow Overview"

### 1.1 Objective
Provide clinical leadership and executive managers with an instantaneous high-level pulse of hospital operations, throughput volume, arrival rhythms, and emergency pressure.

### 1.2 Layout Wireframe
```
+---------------------------------------------------------------------------------------------------+
|  HOSPITAL PATIENT FLOW INTELLIGENCE: EXECUTIVE OVERVIEW                                          |
+---------------------------------------------------------------------------------------------------+
| [KPI: 30,000 Pts]  | [KPI: 34.2m Wait]  | [KPI: 148.5m LOS]  | [KPI: 20.3% Emerg]  | [Bottleneck] |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: Hourly_Arrival_Pattern                     | Sheet: Department_Volume_Bar                  |
| (Line Chart: 24-Hour Inflow Emergency vs OPD)     | (Horizontal Bar: Sorted by Volume & Acuity)   |
|                                                   |                                               |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: Priority_Distribution_Donut                | Interactive Filter Panel                      |
| (Acuity Mix: Critical, High, Medium, Low)         | - Date Range Slider (Jan - Oct 2025)          |
|                                                   | - Department Multi-Select                     |
|                                                   | - Priority Level & Day Type                   |
+---------------------------------------------------------------------------------------------------+
```

### 1.3 Interactivity & Actions
1. **Filter Action (`Act_Dept_Filter`):** Clicking any department bar in `Department_Volume_Bar` filters `Hourly_Arrival_Pattern` and `Priority_Distribution_Donut` to that department.
2. **Highlight Action (`Act_Hour_Highlight`):** Hovering over an hour node highlights the corresponding arrival volume across other charts.
3. **Reset Button:** A custom text button executing `Clear All Filters`.

---

## 2. Dashboard 2: "Department Bottleneck Analysis"

### 2.1 Objective
Answer the fundamental clinical inquiry: *"Where is the hospital losing time?"* Pinpoint which departments and shift hours generate unmanageable queues.

### 2.2 Layout Wireframe
```
+---------------------------------------------------------------------------------------------------+
|  DEPARTMENT BOTTLENECK & WAITING-TIME ANALYTICS                                                  |
+---------------------------------------------------------------------------------------------------+
| Sheet: Department_Wait_Time_Bar                   | Sheet: Volume_vs_Wait_Scatter                 |
| (Avg Doctor Wait with 45m SLA Reference Line)     | (X: Volume, Y: Wait, Size: Capacity,          |
|                                                   |  Color: Bottleneck Severity Tier)             |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: Department_Bottleneck_Heatmap                                                              |
| (Granular 12-Department x 24-Hour Congestion Grid with Diverging Orange-to-Red Color Heat)        |
+---------------------------------------------------------------------------------------------------+
```

### 2.3 Interactivity & Actions
1. **Scatter Quadrant Drill-Down:** Clicking the `High Volume + High Wait` quadrant filters the heatmap below, isolating the exact surge hours.
2. **Heatmap Cross-Filter:** Clicking an individual cell (e.g. `Emergency at 21:00`) displays detailed visit counts and median waits in the tooltip.

---

## 3. Dashboard 3: "Patient Journey & Waiting Time"

### 3.1 Objective
Map the entire sequence of hospital transit from physical arrival through triage, diagnostic testing, procedure/observation, pharmacy collection, and discharge.

### 3.2 Layout Wireframe
```
+---------------------------------------------------------------------------------------------------+
|  END-TO-END PATIENT JOURNEY & STAGE WAITING-TIME DECOMPOSITION                                    |
+---------------------------------------------------------------------------------------------------+
| Sheet: Patient_Journey_Funnel                     | Sheet: Stage_Duration_Breakdown               |
| (Progression from Arrival -> Discharge)           | (Stacked Bar: Reg, Triage, Doctor,            |
|                                                   |  Diagnostics, Treatment, Pharmacy)            |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: LOS_by_Priority_Boxplot                    | Parameter & Metric Controller                 |
| (Statistical Distribution across Urgency Tiers)   | - Parameter: SLA Threshold (15 - 120 min)     |
|                                                   | - Outcome Category Breakdown                  |
+---------------------------------------------------------------------------------------------------+
```

### 3.3 Interactivity & Actions
1. **Stage Focus Action:** Selecting a segment in the stacked bar filters the box plot to observe if that specific stage contributes disproportionately to outliers.
2. **Dynamic SLA Parameter:** Changing `[Wait Time Threshold]` recalculates and updates SLA breach flags across the view in real-time.

---

## 4. Dashboard 4: "Operational Intelligence"

### 4.1 Objective
Provide real-time operational decision support for hospital resource planners, bed coordinators, and staffing supervisors.

### 4.2 Layout Wireframe
```
+---------------------------------------------------------------------------------------------------+
|  HOSPITAL OPERATIONAL INTELLIGENCE & CAPACITY STRESS TESTING                                      |
+---------------------------------------------------------------------------------------------------+
| Parameter Controller: [Select Analysis Metric] (Volume | Wait Time | LOS | Emerg % | Capacity)    |
+---------------------------------------------------------------------------------------------------+
| Sheet: Dynamic_Operational_Trend                                                                  |
| (Dynamic Area Chart updating dynamically to Parameter Selection over the 10-Month Timeline)       |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: Day_of_Week_Arrival_Heatmap                | Sheet: Operational_Anomaly_Alerts             |
| (Congestion Matrix: Day of Week vs Hour)          | (Table of Statistical Surges & Bed Depletions)|
+---------------------------------------------------------------------------------------------------+
```

### 4.3 Interactivity & Actions
1. **Parameter Change Reaction:** When `[Select Analysis Metric]` is altered, the main time-series chart changes its Y-axis, title, and color scheme dynamically.
2. **Anomaly Click-through:** Selecting an alert row from the anomaly table sets the dashboard timeline filter directly to that surge date (e.g. May 12 or July 18).
