# Tableau Calculated Fields & Parameters Reference

**Project:** Hospital Patient Flow Intelligence  
**Course Code:** GR24A3144 (Data Visualization Lab)  

---

## 1. Parameters

### 1.1 `[Select Analysis Metric]`
* **Purpose:** Drives dynamic switching of the primary time-series chart and KPI summaries in Dashboard 4 (Operational Intelligence).
* **Data Type:** String
* **Allowable Values (List):**
  1. `Patient Volume`
  2. `Waiting Time`
  3. `Length of Stay`
  4. `Emergency Percentage`
  5. `Capacity Pressure`
  6. `Department Utilization`
  7. `Bottleneck Score`
* **Current Value:** `Patient Volume`

### 1.2 `[Select Department]`
* **Purpose:** Enables focused departmental drilldown across worksheets in Dashboard 2.
* **Data Type:** String
* **Allowable Values (List):** `(All)` plus the 12 clinical units: Emergency, General Medicine, Cardiology, Orthopedics, Neurology, Pediatrics, General Surgery, Radiology, Laboratory, Pharmacy, ICU, OPD.
* **Current Value:** `(All)`

### 1.3 `[Select Patient / Visit]`
* **Purpose:** Allows singular encounter inspection in Dashboard 3 and Data Explorer.
* **Data Type:** String
* **Allowable Values:** All (Type-in / Search parameter)
* **Current Value:** `V-2025-00001`

---

## 2. Calculated Fields & Level of Detail (LOD) Expressions

### 2.1 `[Total Waiting Time]`
* **Purpose:** Computes cumulative encounter waiting delay.
* **Data Type:** Number (Whole)
* **Formula:**
```tableau
ZN([Wait_Registration]) + ZN([Wait_Triage]) + ZN([Wait_Doctor]) +
ZN([Wait_Diagnostics]) + ZN([Wait_Treatment]) + ZN([Wait_Pharmacy])
```

### 2.2 `[Average Waiting Time]`
* **Purpose:** Aggregated physician wait time benchmark.
* **Data Type:** Number (Decimal)
* **Formula:**
```tableau
AVG([Wait_Doctor])
```

### 2.3 `[Median Waiting Time]`
* **Purpose:** Median consultation delay resistant to tail outlier skew.
* **Data Type:** Number (Decimal)
* **Formula:**
```tableau
MEDIAN([Wait_Doctor])
```

### 2.4 `[Length of Stay]`
* **Purpose:** Total encounter duration in minutes.
* **Data Type:** Number (Whole)
* **Formula:**
```tableau
DATEDIFF('minute', [Arrival_DateTime], [Discharge_DateTime])
```

### 2.5 `[Department Utilization]`
* **Purpose:** Proportion of departmental capacity occupied.
* **Data Type:** Number (Decimal - Percentage)
* **Formula:**
```tableau
([Department_Capacity] - [Bed_Available]) / [Department_Capacity]
```

### 2.6 `[Capacity Pressure]`
* **Purpose:** Operational strain ratio evaluating bed utilization against staff density.
* **Data Type:** Number (Decimal)
* **Formula:**
```tableau
[Department_Utilization] * (ATTR([Department_Capacity]) / (ATTR([Staff_Available]) * 4.0))
```

### 2.7 `[Patient Throughput]`
* **Purpose:** Encounter completion rate per hour.
* **Data Type:** Number (Decimal)
* **Formula:**
```tableau
60.0 / AVG([Length_of_Stay] / 3.0)
```

### 2.8 `[Emergency Percentage]`
* **Purpose:** Proportion of presentations categorized as acute emergency.
* **Data Type:** Number (Decimal - Percentage)
* **Formula:**
```tableau
SUM(IIF([Emergency_Flag] = 'Yes', 1, 0)) / COUNTD([Visit_ID])
```

### 2.9 `[Peak Hour (LOD)]`
* **Purpose:** Fixed LOD identifying the hospital-wide peak arrival hour.
* **Data Type:** Integer
* **Formula:**
```tableau
{ FIXED : 
    ATTR(
        IF { FIXED [Hour] : COUNTD([Visit_ID]) } = 
           { FIXED : MAX({ FIXED [Hour] : COUNTD([Visit_ID]) }) } 
        THEN [Hour] 
        END
    )
}
```

### 2.10 `[Bottleneck Score]`
* **Purpose:** Transparent academic operational bottleneck model (0 to 100 scale).
* **Data Type:** Number (Decimal)
* **Formula:**
```tableau
MIN(40.0, (AVG([Wait_Doctor]) / 75.0) * 40.0) +
(AVG([Department_Utilization]) * 30.0) +
MIN(20.0, (AVG([Capacity_Pressure]) / 2.0) * 20.0) +
MIN(10.0, (AVG([Department_Capacity]) / (AVG([Staff_Available]) * 5.0)) * 5.0)
```

### 2.11 `[Bottleneck Category]`
* **Purpose:** Categorical classification based on Bottleneck Score.
* **Data Type:** String
* **Formula:**
```tableau
IF [Bottleneck Score] >= 70.0 THEN 'Critical'
ELSEIF [Bottleneck Score] >= 50.0 THEN 'High'
ELSEIF [Bottleneck Score] >= 35.0 THEN 'Moderate'
ELSE 'Low'
END
```

### 2.12 `[Waiting Time Category]`
* **Purpose:** Operational delay segmentation.
* **Data Type:** String
* **Formula:**
```tableau
IF [Total Waiting Time] < 30 THEN 'Low Wait (<30m)'
ELSEIF [Total Waiting Time] <= 60 THEN 'Moderate Wait (30-60m)'
ELSEIF [Total Waiting Time] <= 90 THEN 'High Wait (60-90m)'
ELSE 'Severe Delay (>90m)'
END
```

### 2.13 `[LOS Category]`
* **Purpose:** Encounter duration segmentation.
* **Data Type:** String
* **Formula:**
```tableau
IF [Length of Stay] < 120 THEN 'Under 2 Hours'
ELSEIF [Length of Stay] <= 240 THEN '2 - 4 Hours'
ELSEIF [Length of Stay] <= 360 THEN '4 - 6 Hours'
ELSE 'Over 6 Hours'
END
```

### 2.14 `[Dynamic Selected Metric]`
* **Purpose:** Dynamic measure evaluator driven by parameter `[Select Analysis Metric]`.
* **Data Type:** Number (Decimal)
* **Formula:**
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
