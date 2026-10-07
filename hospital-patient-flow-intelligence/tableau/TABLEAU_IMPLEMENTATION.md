# Complete Tableau Implementation Master Guide

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Executive Implementation Overview

This document provides the master blueprint for assembling the complete interactive visual analytics system in **Tableau Desktop 2026.2** / **Tableau Public** using the verified dataset `tableau/data/hospital_patient_flow_tableau.csv` (30,000 records).

---

## 2. Phase-by-Phase Build Workflow

```
[ Phase 1: Ingestion ]    --> Connect to hospital_patient_flow_tableau.csv
        │
[ Phase 2: Calculations] --> Create 14 Calculated Fields, 3 Parameters, and LODs
        │
[ Phase 3: Worksheets ]   --> Build 14 specialized worksheets
        │
[ Phase 4: Dashboards ]   --> Assemble 4 fixed 1366x800 dashboards in layout containers
        │
[ Phase 5: Actions ]      --> Configure cross-filtering, highlight, and parameter actions
        │
[ Phase 6: Export ]       --> Save as Tableau Packaged Workbook (.twbx)
```

---

## 3. Creating Key Tableau Calculations

In Tableau's Data pane, click the down arrow next to the Search bar $\to$ **Create Calculated Field...**

### 1. `Emergency Percentage`
```tableau
SUM(IIF([Emergency_Flag] = 'Yes', 1, 0)) / COUNTD([Visit_ID])
```
*Default Format: Percentage with 1 decimal.*

### 2. `Bottleneck Score`
```tableau
MIN(40.0, (AVG([Wait_Doctor]) / 75.0) * 40.0) +
(AVG([Department_Utilization]) * 30.0) +
MIN(20.0, (AVG([Capacity_Pressure]) / 2.0) * 20.0) +
MIN(10.0, (AVG([Department_Capacity]) / (AVG([Staff_Available]) * 5.0)) * 5.0)
```
*Default Format: Number (Custom), 1 decimal.*

### 3. `Bottleneck Severity Tier`
```tableau
IF [Bottleneck Score] >= 70.0 THEN 'Critical'
ELSEIF [Bottleneck Score] >= 50.0 THEN 'High'
ELSEIF [Bottleneck Score] >= 35.0 THEN 'Moderate'
ELSE 'Low'
END
```

### 4. Parameter `[Select Analysis Metric]`
* Data Type: `String`
* Allowable Values: `List`
* Values: `Patient Volume`, `Waiting Time`, `Length of Stay`, `Emergency Percentage`, `Capacity Pressure`, `Department Utilization`, `Bottleneck Score`.

### 5. `Dynamic Selected Metric`
```tableau
CASE [Select Analysis Metric]
    WHEN 'Patient Volume' THEN COUNTD([Visit_ID])
    WHEN 'Waiting Time' THEN AVG([Wait_Doctor])
    WHEN 'Length of Stay' THEN AVG([Length_of_Stay])
    WHEN 'Emergency Percentage' THEN SUM(IIF([Emergency_Flag] = 'Yes', 1, 0)) / COUNTD([Visit_ID]) * 100
    WHEN 'Capacity Pressure' THEN AVG([Capacity_Pressure])
    WHEN 'Department Utilization' THEN AVG([Department_Utilization]) * 100
    WHEN 'Bottleneck Score' THEN [Bottleneck Score]
END
```

---

## 4. Saving & Packaging the Workbook

1. **Extract Data (Crucial for Portability):**
   * Navigate to the **Data Source** tab.
   * Under Connection in the upper right, toggle from **Live** to **Extract**.
   * Click any worksheet tab to allow Tableau to create the `.hyper` extract.
2. **Save as Packaged Workbook:**
   * Go to **File** $\to$ **Save As...**
   * Change file type dropdown to **Tableau Packaged Workbook (*.twbx)**.
   * Save as: `tableau/hospital_patient_flow_intelligence.twbx`.
3. **Verify:**
   * Close Tableau Desktop.
   * Double-click the saved `.twbx` file to ensure it opens instantly with all data, calculations, and dashboards intact.
