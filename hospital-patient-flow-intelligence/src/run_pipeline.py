"""
run_pipeline.py
===============
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Master orchestrator executing the full end-to-end data engineering, validation,
and analytics pipeline in sequence:
    1. generate_data.py
    2. clean_data.py
    3. feature_engineering.py
    4. validate_data.py
    5. analytics.py
    6. bottleneck_detection.py
    7. anomaly_detection.py
    8. advanced_analytics.py
"""

import time
import sys
import os

def run_step(step_num, title, func):
    print(f"\n========================================================")
    print(f" STEP {step_num}: {title.upper()}")
    print(f"========================================================")
    t0 = time.time()
    func()
    dt = time.time() - t0
    print(f"-> Step {step_num} finished in {dt:.2f} seconds.")

def main():
    print("****************************************************************")
    print("  HOSPITAL PATIENT FLOW INTELLIGENCE: AUTOMATED PIPELINE")
    print("  Course: Data Visualization Lab (Course Code: GR24A3144)")
    print("****************************************************************")

    from generate_data import generate_dataset
    from clean_data import clean_data
    from feature_engineering import engineer_features
    from validate_data import run_validation
    from analytics import run_analytics
    from bottleneck_detection import run_bottleneck_detection
    from anomaly_detection import run_anomaly_detection
    from advanced_analytics import run_advanced_analytics

    total_start = time.time()

    run_step(1, "Synthetic Data Generation (30,000 visits)", lambda: generate_dataset(30000))
    run_step(2, "Data Cleaning & Deduplication", clean_data)
    run_step(3, "Feature Engineering & Bottleneck Modeling", engineer_features)
    run_step(4, "Data Validation & Quality Auditing", run_validation)
    run_step(5, "Patient Journey & Operational Analytics", run_analytics)
    run_step(6, "Bottleneck Matrix & Department Ranking", run_bottleneck_detection)
    run_step(7, "Operational Anomaly Detection (IQR + Isolation Forest)", run_anomaly_detection)
    run_step(8, "Advanced Analytics (PCA & K-Means Clustering)", run_advanced_analytics)

    total_dt = time.time() - total_start
    print("\n****************************************************************")
    print(f"  ALL PIPELINE STAGES COMPLETED SUCCESSFULLY IN {total_dt:.2f}s")
    print("****************************************************************")

if __name__ == "__main__":
    main()
