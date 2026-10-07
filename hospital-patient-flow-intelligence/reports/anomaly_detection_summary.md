# Operational Anomaly Detection Summary Report
**Project:** Hospital Patient Flow Intelligence  
**Focus:** Non-clinical Operational Throughput & Waiting-Time Disruption Analytics  

---

## 1. Methodology
Operational anomalies are identified using two non-parametric and parametric statistical baselines:
1. **Daily Volume Surges (Z-Score Thresholding):**
   $$\text{Z-Score} = \frac{\text{Daily Volume} - \mu}{\sigma}$$
   Points exceeding $|Z| > 2.2$ signify abnormal hospital intake events requiring contingency staffing.
2. **Departmental Congestion (IQR Outlier Boundary):**
   $$\text{Delays} > Q_3 + 1.5 \times \text{IQR}$$
   Evaluated per department-hour segment to capture queue stagnation.

---

## 2. Key Findings & Detected Incidents
- **Total Operational Anomalies Detected:** 270 department-hour events and daily surges.
- **Top Overburdened Departments:** Emergency (accounting for 38% of wait anomalies), General Medicine (24%), and Orthopedics (15%).
- **Notable Surge Windows:**
  - **May 10–16 (Trauma & Heat Outbreak):** Emergency intake proportion surged above 34% (baseline 20%), depleting available beds to near-zero levels.
  - **July 15–25 (Monsoon Pediatric & General Medicine Outbreak):** Inflow in General Medicine and Pediatrics increased by 75%, stretching median doctor waits past 55 minutes.
