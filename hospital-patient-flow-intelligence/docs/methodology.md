# Methodology & Analytical Framework

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Research & Data Engineering Framework

This project follows an established CRISP-DM (Cross-Industry Standard Process for Data Mining) and Healthcare Operations Research methodology adapted specifically for visual business intelligence.

```
[ Domain Understanding ] ──> [ Data Generation & Ingestion ] ──> [ Data Quality & Cleaning ]
                                                                             │
[ Interactive Tableau BI ] <── [ Statistical Analysis & Modeling ] <─────────┘
```

---

## 2. Synthetic Data Simulation Mechanics

To ensure clinical and operational validity without risking patient PII/HIPAA violations, synthetic hospital encounter records were generated using structured queuing models and empirical healthcare arrival distributions:

### 2.1 Queuing Theory Implementation
Hospital arrivals follow non-homogeneous Poisson processes:
$$\lambda(t) = \lambda_{\text{base}} \times f_{\text{diurnal}}(t) \times f_{\text{dow}}(t) \times f_{\text{season}}(t)$$

Where:
* Outpatient departments follow bi-modal arrival distributions peaking at morning clinics (09:00–12:00) and late afternoon clinics (16:00–18:00).
* Emergency arrivals operate 24/7 with a broad peak spanning late afternoon into night shifts (17:00–01:00).
* Doctor consultation queue durations approximate an $M/M/c$ queuing system where wait times escalate non-linearly when the ratio of arrivals to active physicians $\rho = \frac{\lambda}{c \mu}$ approaches 1.0.

### 2.2 Triage Acuity Prioritization
Clinical urgency adheres to the Manchester Triage System / Emergency Severity Index (ESI) 4-tier model:
* **Critical (Tier 1):** Immediate clinical attention (Doctor wait target: 0–5 minutes).
* **High (Tier 2):** Urgent assessment (Doctor wait target: 10–25 minutes).
* **Medium (Tier 3):** Semi-urgent assessment (Doctor wait target: 30–60 minutes).
* **Low (Tier 4):** Non-urgent ambulatory presentation (Doctor wait target: 45–90+ minutes).

---

## 3. Data Cleansing & Validation Pipeline

Real-world hospital EHR datasets are notoriously prone to administrative noise. Controlled dirty data patterns were introduced to the raw intake feed and resolved via automated algorithms:

| Issue Category | Injected Raw Defect | Resolution Rule & Imputation Technique |
| :--- | :--- | :--- |
| **Entity Redundancy** | 450 duplicate rows | Deduplication on primary key `Visit_ID` retaining earliest logged record. |
| **Vocabulary Inconsistency** | Mixed casing (`EMERGENCY`, `Emerg`, `ER`, `Paediatrics`) | Canonical standardization mapping to 12 unified clinical departments. |
| **Missing Values** | Null `Age_Group` and `Arrival_Mode` | Department-conditioned modal imputation (Pediatrics $\to$ 0-17; Emergency $\to$ Ambulance). |
| **Temporal Desynchronization** | Negative wait times (-15m) from unsynchronized workstation clocks | Re-anchored using median wait durations conditioned on triage acuity tier. |
| **Chronological Inversions** | Doctor consult timestamp earlier than triage timestamp | Re-anchored: $\text{Consult Start} = \text{Triage End} + \text{Wait Time}$. |
| **Typographical Outliers** | Typo delays of 9999 minutes | Winsorized at the 99th percentile queue duration (120 minutes). |

---

## 4. Derived Operational Metrics & Formulae

### 4.1 Total Waiting Time
$$\text{Total Wait} = W_{\text{reg}} + W_{\text{triage}} + W_{\text{doctor}} + W_{\text{diagnostic}} + W_{\text{treatment}} + W_{\text{pharmacy}}$$

### 4.2 Total Length of Stay (LOS)
$$\text{Total LOS} = \frac{\text{Discharge Time} - \text{Arrival Time}}{60 \text{ seconds}}$$

### 4.3 Bed Occupancy Rate
$$\text{Occupancy Rate} = \frac{\text{Department Capacity} - \text{Available Beds}}{\text{Department Capacity}}$$

### 4.4 Analytical Bottleneck Score (0 to 100 Scale)
A transparent, non-clinical operational score measuring immediate resource strain:
$$\text{Bottleneck Score} = 0.40 \cdot \min\left(100, \frac{W_{\text{doctor}}}{75} \cdot 100\right) + 0.35 \cdot (\text{Occupancy Rate} \cdot 100) + 0.25 \cdot \min\left(100, \frac{\text{Capacity}}{\text{Staff} \times 4} \cdot 50\right)$$

* **Interpretation Tiers:**
  * $\ge 70.0$: **Severe Bottleneck** (Critical delay; requires surge staffing)
  * $50.0 - 69.9$: **Moderate Congestion** (Approaching capacity limits)
  * $35.0 - 49.9$: **Manageable Flow** (Standard operating conditions)
  * $< 35.0$: **Optimal Flow** (Surplus capacity available)

---

## 5. Statistical & Machine Learning Approaches

1. **Correlation Modeling:** Pearson correlation analysis evaluating linear interactions between staff density, capacity limits, and queuing delays.
2. **Principal Component Analysis (PCA):** Unsupervised dimensional reduction projecting the 9-dimensional operational space onto 2 principal orthogonal axes explaining major variance in congestion states.
3. **Operational Anomaly Detection:**
   * **Daily Volume Spikes:** Z-score thresholding ($|Z| > 2.2$) flagging surge dates.
   * **Departmental Delays:** Interquartile Range ($Q_3 + 1.5 \times \text{IQR}$) detecting extreme localized bottlenecks.
