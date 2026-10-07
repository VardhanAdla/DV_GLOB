# Tableau Calculated Fields Reference

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

This reference outlines all Tableau calculated fields, Level of Detail (LOD) formulas, data types, and dashboard usage locations.

| Field Name | Purpose | Tableau Formula | Data Type | Where It Is Used |
| :--- | :--- | :--- | :--- | :--- |
| **Total Patients** | Quantifies total distinct patient encounters | `COUNTD([Visit_ID])` | Integer | Dashboard 1, 2, 3 KPI Cards & Volume Bars |
| **Average Doctor Wait Time** | Mean waiting duration from triage completion to physician consultation | `AVG([Doctor_Wait_Time])` | Decimal | Dashboard 1 KPI, Dashboard 2 Scatter, Bottleneck Matrix |
| **Median Doctor Wait Time** | Median waiting duration resistant to extreme tail outliers | `MEDIAN([Doctor_Wait_Time])` | Decimal | Dashboard 1 KPI, Department Comparison tooltips |
| **Average Length of Stay** | Mean total elapsed hospital encounter duration in minutes | `AVG([Total_Length_of_Stay])` | Decimal | Dashboard 1 KPI, Dashboard 3 LOS Distribution |
| **Emergency Patient Rate** | Percentage of arrivals admitted via emergency triage | `SUM(IIF([Patient_Type] = 'Emergency', 1, 0)) / COUNTD([Visit_ID])` | Percentage | Dashboard 1 KPI Banner, Weekly surge analysis |
| **Diagnostic Utilization Rate** | Percentage of patients requiring radiology or laboratory testing | `SUM(IIF([Diagnostic_Required] = 'Yes', 1, 0)) / COUNTD([Visit_ID])` | Percentage | Dashboard 3 Patient Journey Funnel |
| **Pharmacy Utilization Rate** | Percentage of patients routed to the dispensary | `SUM(IIF([Pharmacy_Required] = 'Yes', 1, 0)) / COUNTD([Visit_ID])` | Percentage | Dashboard 3 Patient Journey Funnel |
| **Bottleneck Score** | Multi-factor index (0-100) scoring operational queue pressure | `MIN(40.0, (AVG([Doctor_Wait_Time]) / 75.0) * 40.0) + (AVG([Bed_Occupancy_Rate]) * 35.0) + MIN(25.0, (AVG([Department_Capacity]) / (AVG([Staff_Availability]) * 4.0)) * 12.5)` | Decimal | Dashboard 2 Scatter & Matrix, Heatmap coloring |
| **Bottleneck Tier** | Categorical tier based on Bottleneck Score | `IF [Bottleneck Score] >= 70.0 THEN 'Severe Bottleneck' ELSEIF [Bottleneck Score] >= 50.0 THEN 'Moderate Congestion' ELSEIF [Bottleneck Score] >= 35.0 THEN 'Manageable Flow' ELSE 'Optimal Flow' END` | String | Color palette dimension across Dashboards 1 & 2 |
| **Peak Arrival Hour (LOD)** | Fixed LOD expression computing highest volume arrival hour | `{ FIXED : ATTR(IF { FIXED [Hour] : COUNTD([Visit_ID]) } = { FIXED : MAX({ FIXED [Hour] : COUNTD([Visit_ID]) }) } THEN [Hour] END) }` | Integer | Operational planning tooltips |
| **Capacity Pressure Tier** | Classifies bed occupancy into stress categories | `IF [Bed_Occupancy_Rate] >= 0.90 THEN 'Critical Overload' ELSEIF [Bed_Occupancy_Rate] >= 0.75 THEN 'High Demand' ELSE 'Normal' END` | String | Dashboard 4 Operational Intelligence |
| **SLA Breach Indicator** | Evaluates if wait time exceeds administrator threshold parameter | `IF [Doctor_Wait_Time] > [Wait Time Threshold (Minutes)] THEN 'Breached SLA' ELSE 'Compliant' END` | String | Dashboard 2 & 3 Compliance Filters |
| **Dynamic Selected Metric** | Dynamic metric evaluator driven by user parameter selection | `CASE [Select Analysis Metric] WHEN 'Patient Volume' THEN COUNTD([Visit_ID]) WHEN 'Average Waiting Time' THEN AVG([Doctor_Wait_Time]) WHEN 'Average Length of Stay' THEN AVG([Total_Length_of_Stay]) WHEN 'Emergency Inflow %' THEN SUM(IIF([Patient_Type] = 'Emergency', 1, 0)) / COUNTD([Visit_ID]) * 100 WHEN 'Capacity Pressure' THEN AVG([Bed_Occupancy_Rate]) * 100 END` | Decimal | Dashboard 4 Parameter-driven operational view |
