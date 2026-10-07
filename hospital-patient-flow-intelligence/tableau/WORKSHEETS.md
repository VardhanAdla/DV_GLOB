# Tableau Worksheets Specification & Shelf-by-Shelf Layout Guide

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

This guide provides the exact shelf placement (Columns, Rows, Marks, Filters, Colors, Sizes, Labels, and Tooltips) for all 14 worksheets across the 4 dashboards.

---

## Worksheet Index

| # | Worksheet Name | Chart Type | Intended Dashboard | Primary Dimensions & Measures |
| :-: | :--- | :--- | :--- | :--- |
| **01** | `KPI_Summary_Cards` | Text / Card | Dashboard 1 (Top Strip) | `COUNTD(Visit_ID)`, `AVG(Wait_Doctor)`, `AVG(Length_of_Stay)`, `[Emergency %]` |
| **02** | `Hourly_Arrivals` | Line Chart | Dashboard 1 (Top Left) | Columns: `[Hour]`, Rows: `COUNTD(Visit_ID)`, Color: `[Emergency_Flag]` |
| **03** | `Department_Volume` | Horizontal Bar | Dashboard 1 (Top Right) | Columns: `COUNTD(Visit_ID)`, Rows: `[Department]`, Color: `[Bottleneck_Category]` |
| **04** | `Department_Wait_Time` | Horizontal Bar | Dashboard 2 (Top Left) | Columns: `AVG(Wait_Doctor)`, Rows: `[Department]`, Ref Line: 45 min |
| **05** | `Priority_Distribution` | Donut / Pie | Dashboard 1 (Bottom Left) | Color: `[Priority_Level]`, Angle: `COUNTD(Visit_ID)` |
| **06** | `Patient_Type_Distribution` | Bar Chart | Dashboard 1 (Bottom Mid) | Columns: `COUNTD(Visit_ID)`, Rows: `[Patient_Type]` |
| **07** | `Daily_Trend` | Line / Area | Dashboard 1 (Bottom Right)| Columns: `DAY(Arrival_Date)`, Rows: `COUNTD(Visit_ID)` |
| **08** | `Emergency_vs_NonEmergency`| Dual Axis Bar | Dashboard 1 (Analytical) | Columns: `[Month]`, Rows: `COUNTD(Visit_ID)`, Color: `[Emergency_Flag]` |
| **09** | `Volume_vs_Wait_Scatter` | Scatter Plot | Dashboard 2 (Top Right) | X: `COUNTD(Visit_ID)`, Y: `AVG(Wait_Doctor)`, Size: `Capacity`, Color: `Bottleneck_Category` |
| **10** | `Bottleneck_Heatmap` | Heatmap (Square)| Dashboard 2 (Bottom Span) | Columns: `[Hour]`, Rows: `[Department]`, Color: `AVG(Bottleneck_Score)` |
| **11** | `Capacity_Pressure_Chart` | Bullet / Bar | Dashboard 2 (Middle) | Columns: `AVG(Capacity_Pressure)`, Rows: `[Department]` |
| **12** | `Staff_vs_Wait_Time` | Scatter / Line | Dashboard 2 (Middle Right)| Columns: `AVG(Staff_Available)`, Rows: `AVG(Wait_Doctor)` |
| **13** | `Patient_Journey_Funnel` | Funnel / Bar | Dashboard 3 (Left Half) | Rows: `[Care_Stage]`, Columns: `[Stage_Completion_Count]` |
| **14** | `Dynamic_Metric_Trend` | Dynamic Area | Dashboard 4 (Top Half) | Columns: `DAY(Arrival_Date)`, Rows: `[Dynamic Selected Metric]` |

---

## Detailed Shelf-by-Shelf Layouts

### Sheet 01: `KPI_Summary_Cards`
* **Rows:** (Empty)
* **Columns:** (Empty)
* **Marks (Text):** `COUNTD([Visit_ID])`, `AVG([Wait_Doctor])`, `AVG([Length_of_Stay])`, `[Emergency Percentage]`
* **Formatting:** Font 24pt Bold, Navy (`#1b6ca8`) and Red (`#d9534f`).

### Sheet 02: `Hourly_Arrivals`
* **Columns:** `[Hour]` (Continuous integer, range 0 to 23).
* **Rows:** `COUNTD([Visit_ID])`
* **Color:** `[Emergency_Flag]` (Yes: Coral `#d9534f`, No: Steel Blue `#1b6ca8`).
* **Mark:** Line chart with markers enabled.
* **Tooltip:**
  ```
  Hour: <Hour>:00
  Emergency Status: <Emergency_Flag>
  Patient Arrivals: <COUNTD(Visit_ID)>
  Average Doctor Wait: <AVG(Wait_Doctor)> min
  ```

### Sheet 03: `Department_Volume`
* **Columns:** `COUNTD([Visit_ID])`
* **Rows:** `[Department]` (Sorted Descending by `COUNTD([Visit_ID])`).
* **Color:** `[Bottleneck_Category]` (Critical: Red, High: Orange, Moderate: Blue, Low: Green).
* **Label:** `COUNTD([Visit_ID])` displayed on bar tips.
* **Mark:** Horizontal Bar.

### Sheet 04: `Department_Wait_Time`
* **Columns:** `AVG([Wait_Doctor])`
* **Rows:** `[Department]` (Sorted Descending by `AVG([Wait_Doctor])`).
* **Color:** `AVG([Wait_Doctor])` (Orange-to-Red diverging).
* **Reference Line:** Constant line at `45` min labeled "Hospital SLA Target (45 min)".
* **Mark:** Horizontal Bar.

### Sheet 05: `Priority_Distribution`
* **Columns:** `MIN(1)`, `MIN(1)` (Dual axis for donut hole).
* **Rows:** (Empty)
* **Marks 1:** Pie -> Color: `[Priority_Level]`, Angle: `COUNTD([Visit_ID])`.
* **Marks 2:** Circle -> Color: White (`#ffffff`), Label: `COUNTD([Visit_ID])` centered.

### Sheet 09: `Volume_vs_Wait_Scatter`
* **Columns:** `COUNTD([Visit_ID])` (Hourly arrivals per unit).
* **Rows:** `AVG([Wait_Doctor])`
* **Detail:** `[Department]`, `[Hour]`
* **Size:** `AVG([Department_Capacity])`
* **Color:** `[Bottleneck_Category]`
* **Reference Lines:** Y-axis constant at `45` min (SLA delay threshold).
* **Mark:** Circle with 75% opacity and subtle grey border.

### Sheet 10: `Bottleneck_Heatmap`
* **Columns:** `[Hour]` (Discrete, 0 to 23).
* **Rows:** `[Department]` (12 clinical units).
* **Color:** `AVG([Bottleneck_Score])` (Palette: Red-Yellow-Green Diverging, Reversed).
* **Label:** `ROUND(AVG([Bottleneck_Score]), 0)`
* **Mark:** Square (Heatmap).

### Sheet 13: `Patient_Journey_Funnel`
* **Rows:** `[Stage_Order]` (Registration, Triage, Doctor, Diagnostics, Treatment, Pharmacy).
* **Columns:** `[Contribution_To_Total_Wait_Pct]` or Patient Count.
* **Color:** Sequential Blue gradient.
* **Mark:** Horizontal Bar / Funnel.

### Sheet 14: `Dynamic_Metric_Trend`
* **Columns:** `[Arrival_Date]` (Continuous Day).
* **Rows:** `[Dynamic Selected Metric]`
* **Color:** Steel Blue (`#1b6ca8`).
* **Mark:** Area chart with 25% opacity fill.
