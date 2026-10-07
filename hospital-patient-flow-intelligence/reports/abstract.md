# Project Abstract

**Project Title:** Hospital Patient Flow Intelligence  
**Subtitle:** Interactive Tableau-Based Patient Flow, Bottleneck and Waiting-Time Analytics System  
**Academic Context:** College GLOB Project, III Year I Semester  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

Modern healthcare delivery systems function as high-velocity, multi-stage stochastic service networks where operational bottlenecks at any juncture—from administrative registration and clinical triage to physician consultation, diagnostic testing, inpatient admission, and pharmacy dispensing—rapidly compound into system-wide delays, overcrowding, and compromised patient care. Traditional electronic health record (EHR) systems excel at transactional recording but remain ill-suited for real-time visual process mining and operational decision support. 

This project presents **Hospital Patient Flow Intelligence**, a comprehensive, interactive business intelligence platform engineered primarily in **Tableau Desktop**, underpinned by an automated **Python** data simulation, cleaning, and multidimensional analytics pipeline. The system investigates an anonymized, synthetic cohort of 30,000 patient encounters spanning 10 months of operations across 12 clinical departments (Emergency, General Medicine, Cardiology, Orthopedics, Pediatrics, Neurology, Dermatology, ENT, Ophthalmology, General Surgery, Radiology, and Laboratory). 

A non-homogeneous queuing simulation models realistic diurnal arrival surges (morning outpatient peaks from 09:00–12:00 versus 24/7 emergency dynamics), Manchester/ESI 4-tier triage priority rules, ancillary diagnostic routing, bed occupancy constraints, and staffing availability. Controlled real-world data quality anomalies—including duplicate visits, timestamp inversions, clock-drift negative delays, and category inconsistencies—are introduced into a 30,450-row raw feed and systematically rectified using an automated, auditable data cleansing pipeline.

The analytical architecture formulates a novel, transparent **Bottleneck Score (0–100)** synthesizing doctor consultation delays (40%), bed occupancy saturation (35%), and staffing stretch ratios (25%). Four integrated Tableau dashboards are developed: (1) **Hospital Flow Overview**, (2) **Department Bottleneck Analysis**, (3) **Patient Journey & Waiting Time**, and (4) **Operational Intelligence**. These dashboards feature dynamic parameter metric switching, Level of Detail (LOD) benchmark expressions, and multi-sheet cross-filtering. 

Multidimensional evaluation reveals that Emergency and General Medicine suffer the most acute operational friction, with peak waiting times concentrating during shift changeover intervals (10:00–12:00 and 19:00–21:00). Diagnostic testing in Cardiology and Orthopedics introduces an additional 20–35 minute delay multiplier. The interactive dashboards empower hospital administrators and triage supervisors to pinpoint queue stagnation, forecast surge pressure, and optimize clinical workforce scheduling, demonstrating the transformative capacity of visual analytics in healthcare operations.
