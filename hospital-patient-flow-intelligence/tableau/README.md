# Tableau Resources & Workbook Architecture
## Hospital Patient Flow Intelligence (GR24A3144)

This directory houses the complete Tableau analytical architecture, calculated fields, dashboard wireframes, and workbook specifications for the **Hospital Patient Flow Intelligence** project.

---

## Directory Contents

| File | Description | Target Use |
| :--- | :--- | :--- |
| [`dashboard_specification.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/dashboard_specification.md) | Wireframes, container layout hierarchies, and cross-filter action rules for all 4 dashboards. | Visual arrangement & dashboard composition |
| [`sheet_specification.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/sheet_specification.md) | Detailed shelf layout (Rows, Columns, Marks, Detail, Color, Filters) for all 14 worksheets. | Worksheet design in Tableau Desktop |
| [`calculated_fields.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/calculated_fields.md) | Complete list of Tableau calculated fields, LOD expressions, and parameters with exact formulas. | Data pane calculation authoring |
| [`tableau_prep_workflow.md`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/tableau_prep_workflow.md) | 8-step visual ETL pipeline instructions for Tableau Prep Builder. | Data preparation & ETL execution |
| [`hospital_patient_flow_intelligence.twb`](file:///c:/Users/DELL/Desktop/Dv_Glob/hospital-patient-flow-intelligence/tableau/hospital_patient_flow_intelligence.twb) | Tableau Workbook XML configured for instant connection to the clean CSV dataset. | Direct opening in Tableau Desktop / Public |

---

## Primary Data Source Connection
* **File:** `../data/processed/hospital_patient_flow_clean.csv`
* **Record Count:** 30,000 verified encounters
* **Dimensions:** 47 operational, clinical, and demographic attributes
* **Connection Mode:** Live Text File / Tableau Data Extract (`.hyper`)
