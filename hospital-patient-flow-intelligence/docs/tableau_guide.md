# Tableau Implementation Guide & Architecture

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Visual Hierarchy & Design System

The Tableau dashboards are engineered with an intentional, restrained executive healthcare aesthetic:
* **Palette:**
  * Primary Corporate Navy: `#1B6CA8` (Clean headers, baseline lines, structure)
  * Alert / Severe Bottleneck: `#D9534F` (Critical queues, SLA breaches, Emergency markers)
  * Moderate Congestion: `#F0AD4E` (Pre-bottleneck warnings)
  * Optimal Flow: `#5CB85C` (Capacity surplus, compliant queues)
  * Backgrounds: Light Slate `#F8F9FA` with clean `#E2E8F0` separation lines.
* **Typography:** Segoe UI / Tableau Standard (Clean legibility across high-density charts).
* **Grid Discipline:** Fixed 1366 x 800 pixel layout container architecture preventing overlapping charts on display monitors.

---

## 2. Dashboard Breakdown

### Dashboard 1: Executive Hospital Flow Overview
* **Primary Role:** High-level executive monitoring.
* **Key Components:**
  * Top KPI Banner: Patient Volume, Avg Wait, Avg LOS, Emergency Intake %.
  * Hourly Arrival Pattern (Line Chart comparing Emergency 24/7 inflow vs Outpatient peak curves).
  * Department Patient Volume (Horizontal Bar sorted descending, colored by Bottleneck Category).
  * Priority Acuity Donut (Dual-axis donut visualizing Critical, High, Medium, Low split).
* **Filters:** Multi-value dropdowns for Department, Priority Level, Gender, and Date range slider.

### Dashboard 2: Department Bottleneck Analysis
* **Primary Role:** Operational bottleneck diagnosis answering *"Where is the hospital losing time?"*
* **Key Components:**
  * Department Waiting Time Bar (Bar chart with constant 45-minute SLA target line).
  * Volume vs. Waiting Time Scatter Plot (X: Volume, Y: Wait, Size: Capacity, Color: Bottleneck Category).
  * Granular Department-Hour Congestion Heatmap (12x24 grid mapping exact shift bottlenecks).
* **Interactivity:** Scatter circle selection highlights exact department-hour in the heatmap.

### Dashboard 3: Patient Journey & Waiting Time
* **Primary Role:** End-to-end patient transit tracking across clinical milestones.
* **Key Components:**
  * Patient Journey Progression Funnel (Horizontal funnel from Arrival to Discharge).
  * Cumulative Stage Duration Breakdown (Stacked bar showing wait times for Reg, Triage, Consult, Diag, Treat, Pharm).
  * Length of Stay by Priority Box Plot (IQR and statistical dispersion across acuity tiers).
* **Parameter Action:** Slider parameter adjusting SLA wait thresholds dynamically.

### Dashboard 4: Operational Intelligence
* **Primary Role:** Dynamic capacity stress testing and anomaly decision support.
* **Key Components:**
  * Dynamic Trend Chart driven by parameter `[Select Analysis Metric]`.
  * Day of Week vs. Hour Arrival Heatmap.
  * Operational Anomaly Alerts log (Flagging surge dates and extreme bed depletion).

---

## 3. Best Practices for Lab Viva & Presentation
1. **Always lead with the data story:** Start with the 30,000 patient encounters, point out the morning outpatient peak (09:00–12:00) vs evening emergency surge, and then drill into the bottleneck departments (Emergency, General Medicine, Orthopedics).
2. **Demonstrate cross-filtering live:** Click on `Emergency` in Dashboard 1 to show how all other sheets dynamically filter to display the 24/7 curve, high ambulance rate, and critical priority distribution.
3. **Showcase the Bottleneck Scatter Plot:** Explain the 4-quadrant view in Dashboard 2 showing high-volume, high-wait units as the priority targets for administrative intervention.
