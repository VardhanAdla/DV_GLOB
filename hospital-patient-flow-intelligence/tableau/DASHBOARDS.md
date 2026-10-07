# Tableau Dashboards Assembly & Interactive Action Guide

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  
**Standard Dimensions:** Fixed 1366 x 800 px  

---

## 1. Dashboard 1: Hospital Flow Overview

### Visual Layout Architecture
```
+---------------------------------------------------------------------------------------------------+
|  HOSPITAL PATIENT FLOW INTELLIGENCE: EXECUTIVE FLOW OVERVIEW                                      |
+---------------------------------------------------------------------------------------------------+
| [KPI: 30,000 Pts]  | [KPI: 34.2m Wait]  | [KPI: 148.5m LOS]  | [KPI: 20.3% Emerg]  | [Bottleneck] |
+---------------------------------------------------+-----------------------------------------------+
| Sheet 02: Hourly_Arrivals                         | Sheet 03: Department_Volume                   |
| (24-Hour Diurnal Inflow: Emergency vs OPD)        | (Sorted Horizontal Bar colored by Bottleneck) |
+---------------------------------------------------+-----------------------------------------------+
| Sheet 05: Priority_Distribution                   | Global Interactive Filter Container           |
| (Manchester/ESI Triage Acuity Donut)              | - Date Range Slider (Jan - Oct 2025)          |
|                                                   | - Department Multi-Select Dropdown            |
|                                                   | - Shift & Emergency Flag Selectors            |
+---------------------------------------------------------------------------------------------------+
```

### Dashboard Interactivity & Action Configuration
1. **Filter Action (`Act_Dept_Filter`):**
   * **Source Sheet:** `Department_Volume`
   * **Run on:** `Select`
   * **Target Sheets:** `Hourly_Arrivals`, `Priority_Distribution`, `KPI_Summary_Cards`
   * **Clearing Selection:** `Show all values`
2. **Highlight Action (`Act_Hour_Highlight`):**
   * **Source Sheet:** `Hourly_Arrivals`
   * **Run on:** `Hover`
   * **Target Fields:** `[Hour]`

---

## 2. Dashboard 2: Department Bottleneck Analysis

### Visual Layout Architecture
```
+---------------------------------------------------------------------------------------------------+
|  DEPARTMENT BOTTLENECK & WAITING-TIME ANALYTICS                                                  |
+---------------------------------------------------------------------------------------------------+
| Sheet 04: Department_Wait_Time                    | Sheet 09: Volume_vs_Wait_Scatter              |
| (Average Doctor Wait with 45m SLA Target Line)    | (X: Volume, Y: Wait, Size: Capacity,          |
|                                                   |  Color: Bottleneck Severity Tier)             |
+---------------------------------------------------+-----------------------------------------------+
| Sheet 10: Bottleneck_Heatmap                                                                      |
| (Full Width 12-Department x 24-Hour Congestion Grid with Diverging Orange-to-Red Color Heat)      |
+---------------------------------------------------------------------------------------------------+
```

### Dashboard Actions
1. **Quadrant Filter Action (`Act_Scatter_To_Heatmap`):**
   * **Source Sheet:** `Volume_vs_Wait_Scatter`
   * **Run on:** `Select`
   * **Target Sheet:** `Bottleneck_Heatmap`
   * Selecting any bubble zooms the heatmap to that specific department and hour.

---

## 3. Dashboard 3: Patient Journey & Waiting Time

### Visual Layout Architecture
```
+---------------------------------------------------------------------------------------------------+
|  END-TO-END PATIENT JOURNEY & STAGE WAITING-TIME DECOMPOSITION                                    |
+---------------------------------------------------------------------------------------------------+
| Sheet 13: Patient_Journey_Funnel                  | Sheet: Stage_Duration_Stacked                 |
| (Progression from Arrival to Discharge)           | (Decomposed wait delays across 6 stages)      |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: LOS_by_Priority_Boxplot                    | Encounter Drilldown Inspector                 |
| (Statistical Dispersion across Urgency Tiers)     | Parameter: [Select Patient / Visit]           |
|                                                   | Displays individual encounter milestones      |
+---------------------------------------------------------------------------------------------------+
```

---

## 4. Dashboard 4: Operational Intelligence

### Visual Layout Architecture
```
+---------------------------------------------------------------------------------------------------+
|  HOSPITAL OPERATIONAL INTELLIGENCE & CAPACITY STRESS TESTING                                      |
+---------------------------------------------------------------------------------------------------+
| Parameter Controller: [Select Analysis Metric] (Volume | Wait | LOS | Emerg % | Capacity | Score)  |
+---------------------------------------------------------------------------------------------------+
| Sheet 14: Dynamic_Metric_Trend                                                                    |
| (Dynamic Area Chart adapting dynamically to Parameter Selection across the 10-Month Timeline)     |
+---------------------------------------------------+-----------------------------------------------+
| Sheet: Day_of_Week_Arrival_Heatmap                | Operational Anomaly Alerts Log                |
| (Congestion Matrix: Day of Week vs Hour)          | (Interactive table of surge dates & alerts)   |
+---------------------------------------------------------------------------------------------------+
```
