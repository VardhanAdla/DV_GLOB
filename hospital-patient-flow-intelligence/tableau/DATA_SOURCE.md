# Tableau Data Source Specification & Connection Guide

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  
**Primary Data File:** `tableau/data/hospital_patient_flow_tableau.csv`  
**Alternative Data File:** `data/processed/hospital_patient_flow_clean.csv`  
**Record Count:** Exactly 30,000 verified encounters  

---

## 1. How to Connect in Tableau Desktop

1. Open **Tableau Desktop** (or **Tableau Public**).
2. On the left navigation pane under **Connect** -> **To a File**, click **Text file**.
3. In the file dialogue, navigate to:
   ```
   c:\Users\DELL\Desktop\Dv_Glob\hospital-patient-flow-intelligence\tableau\data\hospital_patient_flow_tableau.csv
   ```
4. Click **Open**.

---

## 2. Ingestion Settings & Encoding

* **Field Separator:** Comma (`,`)
* **Text Qualifier:** Automatic (`"`)
* **Character Set:** UTF-8
* **Locale:** English (United States)

---

## 3. Data Type Metadata Audit

Verify in Tableau's Data Source grid that the following data types are automatically assigned:

| Column Name | Tableau Remote Type | Tableau Role | Purpose |
| :--- | :--- | :--- | :--- |
| `Patient_ID` | String (`Abc`) | Dimension | Demographic tracking across repeat visits |
| `Visit_ID` | String (`Abc`) | Dimension (Primary Key) | Unique encounter identifier |
| `Arrival_Date` | Date (`📅`) | Dimension (Date) | Daily / monthly temporal slicing |
| `Arrival_Time` | String (`Abc`) | Dimension | Time of presentation |
| `Arrival_DateTime` | Date & Time (`📅🕒`) | Dimension | Exact timestamp anchor |
| `Age` | Number (Whole) (`#`) | Dimension / Measure | Patient age |
| `Gender` | String (`Abc`) | Dimension | Male / Female / Other |
| `Patient_Type` | String (`Abc`) | Dimension | Emergency, Walk-in, Appointment, Referral, Follow-up |
| `Priority_Level` | String (`Abc`) | Dimension | Critical, High, Medium, Low |
| `Department` | String (`Abc`) | Dimension | 12 clinical care units |
| `Wait_Doctor` | Number (Whole) (`#`) | Measure | Doctor consultation wait in minutes |
| `Total_Waiting_Time`| Number (Whole) (`#`) | Measure | Cumulative encounter delay |
| `Length_of_Stay` | Number (Whole) (`#`) | Measure | Encounter duration in minutes |
| `Department_Capacity`| Number (Whole) (`#`) | Measure | Maximum concurrent bed capacity |
| `Department_Utilization` | Number (Decimal) (`#`) | Measure | Occupancy proportion (0.0 to 1.0) |
| `Capacity_Pressure` | Number (Decimal) (`#`) | Measure | Strain ratio |
| `Bottleneck_Score` | Number (Decimal) (`#`) | Measure | Composite 0 to 100 operational score |
| `Bottleneck_Category` | String (`Abc`) | Dimension | Low, Moderate, High, Critical |
| `Anomaly_Flag` | String (`Abc`) | Dimension | Yes / No |
| `Anomaly_Type` | String (`Abc`) | Dimension | Operational anomaly classification |
