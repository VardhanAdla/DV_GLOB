"""
advanced_analytics.py
=====================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Performs advanced statistical machine learning:
    1. Principal Component Analysis (PCA) across 6 operational dimensions:
       [Wait_Doctor, Total_Waiting_Time, Length_of_Stay, Department_Utilization, Capacity_Pressure, Staff_Available]
    2. K-Means Clustering segmenting hospital operational states into 4 distinct operational regimes:
       - Cluster 0: Optimal Balanced Flow
       - Cluster 1: Morning Outpatient Volume Peak
       - Cluster 2: Severe Emergency & Bed Depletion Overload
       - Cluster 3: Ancillary Diagnostic & Treatment Stagnation

Outputs:
    - analysis/pca_results.csv
    - analysis/clustering_centroids.csv
    - analysis/correlation/pca_multidimensional_projection.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

def run_advanced_analytics():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    clean_csv = os.path.join(base_dir, "data", "processed", "hospital_patient_flow_clean.csv")
    out_dir = os.path.join(base_dir, "analysis")
    corr_dir = os.path.join(out_dir, "correlation")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(corr_dir, exist_ok=True)

    print(f"[1/4] Loading clean data from {clean_csv} for advanced analytics...")
    df = pd.read_csv(clean_csv, low_memory=False)

    feature_cols = [
        "Wait_Doctor", "Total_Waiting_Time", "Length_of_Stay",
        "Department_Utilization", "Capacity_Pressure", "Staff_Available"
    ]
    X = df[feature_cols].copy()

    # Standardize
    print("[2/4] Standardizing operational features and fitting PCA...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 1. PCA
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_scaled)
    df["PCA1"] = pca_coords[:, 0]
    df["PCA2"] = pca_coords[:, 1]

    exp_var = pca.explained_variance_ratio_
    print(f"   -> PCA Explained Variance: PC1={exp_var[0]*100:.1f}%, PC2={exp_var[1]*100:.1f}% (Total={sum(exp_var)*100:.1f}%)")

    pca_summary = pd.DataFrame({
        "Component": ["PC1", "PC2"],
        "Explained_Variance_Ratio": [round(v, 4) for v in exp_var],
        "Cumulative_Variance": [round(exp_var[0], 4), round(sum(exp_var), 4)]
    })
    pca_summary.to_csv(os.path.join(out_dir, "pca_results.csv"), index=False)

    # 2. K-Means Clustering (k=4 operational regimes)
    print("[3/4] Performing K-Means Clustering (k=4 operational states)...")
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    cluster_names = {
        0: "Optimal Balanced Flow",
        1: "Outpatient Queue Surge",
        2: "Severe Emergency Overload",
        3: "Ancillary Diagnostic Stagnation"
    }
    df["Cluster_Name"] = df["Cluster"].map(cluster_names)

    # Compute unscaled centroids
    centroids = df.groupby("Cluster_Name")[feature_cols].mean().round(2).reset_index()
    centroids.to_csv(os.path.join(out_dir, "clustering_centroids.csv"), index=False)
    print("   -> Cluster centroids exported.")

    # 3. Visualization
    print("[4/4] Rendering 2D PCA & Cluster projection chart...")
    plt.figure(figsize=(10, 6), dpi=300)
    scatter = plt.scatter(
        df["PCA1"], df["PCA2"],
        c=df["Cluster"], cmap="Set2", alpha=0.35, s=15
    )
    plt.title(f"PCA 2D State Projection: Hospital Operational Regimes (Variance: {sum(exp_var)*100:.1f}%)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel(f"Principal Component 1 ({exp_var[0]*100:.1f}% Variance - Queue & Delay Axis)", fontsize=11)
    plt.ylabel(f"Principal Component 2 ({exp_var[1]*100:.1f}% Variance - Capacity & Staff Pressure)", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(corr_dir, "pca_multidimensional_projection.png"))
    plt.close()

    print("-> Advanced analytics completed successfully.")

if __name__ == "__main__":
    run_advanced_analytics()
