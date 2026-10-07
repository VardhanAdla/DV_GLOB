# Problem Statement: Healthcare Operational Delays & Inefficient Patient Flow

**Course Code:** GR24A3144 (Data Visualization Lab)  
**Project:** Hospital Patient Flow Intelligence  

---

## 1. Context & Clinical Operational Background

In tertiary healthcare institutions, hospital departments do not operate in clinical isolation. A single patient encounter frequently transitions through a chain of dependent care stages:
$$\text{Arrival} \longrightarrow \text{Registration} \longrightarrow \text{Triage} \longrightarrow \text{Doctor Consultation} \longrightarrow \text{Diagnostics} \longrightarrow \text{Treatment} \longrightarrow \text{Pharmacy} \longrightarrow \text{Discharge}$$

Despite massive investments in Electronic Health Record (EHR) software and Hospital Information Systems (HIS), healthcare administrators consistently grapple with acute operational failures:
1. **Waiting Room Overcrowding:** Outpatient departments and emergency intake areas frequently face unmanageable patient pileups during morning and evening rush hours.
2. **Invisible Bottlenecks:** Hospital managers lack intuitive tools to answer the question: *"Is a patient waiting because the physician is busy, because the lab results are pending, or because there are no available inpatient beds?"*
3. **Mismatched Staffing Schedules:** Clinician and nursing shifts frequently follow static timetables (e.g. 08:00 to 16:00 and 16:00 to 00:00) that fail to align with real-time arrival peaks.
4. **Left Without Being Seen (LWBS) Attrition:** When waiting times exceed patient tolerance thresholds (typically >60–90 minutes for non-critical cases), ambulatory patients walk out without receiving clinical care, creating severe medico-legal liabilities and lost revenue.
5. **Static, Non-Interactive Reporting:** Traditional hospital reports consist of static tabular printouts (PDF/Excel) summarizing historical bed counts and billing figures, offering zero interactive drilldown, parameter simulation, or cross-departmental correlation.

---

## 2. Formal Problem Statement

> *"How can complex, high-velocity hospital patient encounter logs across multiple clinical units, acuity tiers, and care stages be transformed into an interactive, multi-dimensional visual intelligence system that reliably identifies operational bottlenecks, measures waiting-time disparities, tracks capacity saturation, and provides intuitive decision support for hospital resource planners?"*

---

## 3. Scope & Operational Boundaries

* **In Scope:**
  * Modeling the complete patient transit journey across 12 distinct clinical departments.
  * Ingesting, cleaning, validating, and structuring 30,000 patient encounter records.
  * Developing an automated data engineering pipeline that resolves dirty data, timestamp inversions, and missing values.
  * Formulating an analytical, non-clinical **Bottleneck Score**.
  * Designing 4 comprehensive, interactive Tableau dashboards with cross-filtering, LOD calculations, and parameter-driven views.
  * Performing multi-dimensional statistical, correlation, and anomaly detection analyses.
* **Out of Scope (Explicit Limitations):**
  * Automated medical diagnosis, clinical pharmacology, or treatment effectiveness prediction.
  * Personal Identifiable Information (PII) or real patient records (synthetic anonymized data only).
  * Transactional EHR database CRUD operations or user authentication login portals.
