# Tableau Workbook Testing & Quality Assurance Plan

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Testing Objectives & Verification Scope

This document details the quality assurance verification protocol for confirming that the Tableau Desktop implementation functions reliably, free of calculation broken links, orphaned dimensions, or cross-filter rendering lags.

---

## 2. Test Cases & Verification Checklist

| Test ID | Testing Dimension | Test Procedure | Expected Result | Verification Checkpoint |
| :--- | :--- | :--- | :--- | :---: |
| **TB-01** | Data Source Ingestion | Connect to `tableau/data/hospital_patient_flow_tableau.csv` | Exactly 30,000 records detected with correct data types | Verified in Data Source tab |
| **TB-02** | Calculation Syntax | Create 14 calculated fields and LODs | "The calculation is valid" message displayed for all formulas | Zero syntax errors |
| **TB-03** | Parameter Functionality | Create parameter `[Select Analysis Metric]` | Dropdown switches values among 7 operational measures | Parameter active |
| **TB-04** | Dynamic Measure Switching | Link `[Dynamic Selected Metric]` to Sheet 14 | Area chart Y-axis updates dynamically on parameter selection | Dynamic rendering verified |
| **TB-05** | Scatter Quadrant Rendering | Build Sheet 09 Volume vs Wait Scatter | Displays bubbles sized by capacity and colored by bottleneck tier | Reference line at 45m active |
| **TB-06** | Heatmap Matrix Encoding | Build Sheet 10 12x24 Congestion Grid | Correctly displays 288 colored cells with visible bottleneck score labels | Palette reversed (Red=High) |
| **TB-07** | Dashboard Layout Containers | Assemble Dashboards 1 through 4 | Fixed canvas 1366x800 with zero horizontal scrollbars | Layout containers aligned |
| **TB-08** | Cross-Filtering Actions | Click on "Emergency" bar in Dashboard 1 | All other sheets isolate Emergency encounters in real-time | Cross-filter verified |
| **TB-09** | Scatter to Heatmap Zoom | Select a high-wait bubble in Dashboard 2 | Highlights corresponding department and hour in the heatmap below | Quadrant drilldown verified |
| **TB-10** | Tooltip Data Integrity | Hover over clinical department bars | Displays clean, customized metrics without default clutter | Formatted tooltips verified |
| **TB-11** | Packaged Workbook Portability | Save as `.twbx` and reopen | Workbook opens cleanly on any machine without missing file prompts | Verified `.twbx` integrity |

---

## 3. Troubleshooting Common Tableau Issues

1. **Error: "The field does not exist":** Ensure that `tableau/data/hospital_patient_flow_tableau.csv` is selected rather than an older raw file with legacy column headers.
2. **Numbers display without decimals:** Right-click the calculated field in the Data pane $\to$ **Default Properties** $\to$ **Number Format...** $\to$ Set to **Number (Custom)** with 1 decimal place.
3. **Reference Line not visible:** On the Analytics tab, drag **Reference Line** onto **Table** (not Pane or Cell), select **Constant**, and input `45`.
