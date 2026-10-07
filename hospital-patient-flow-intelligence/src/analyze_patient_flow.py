"""
analyze_patient_flow.py
=======================
Project: Hospital Patient Flow Intelligence
Course: Data Visualization Lab (GR24A3144)

Performs comprehensive multi-dimensional statistical analysis, correlation modeling,
PCA feature projection, and patient flow journey analytics.

Generates:
    - analysis/statistical_analysis/*.png, *.csv
    - analysis/correlation/*.png, *.csv
    - analysis/patient_flow/*.png, *.csv
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Set aesthetic style for professional publication
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

def run_analysis():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    clean_csv = os.path.join(base_dir, "data", "processed", "hospital_patient_flow_clean.csv")
    
    stat_dir = os.path.join(base_dir, "analysis", "statistical_analysis")
    corr_dir = os.path.join(base_dir, "analysis", "correlation")
    flow_dir = os.path.join(base_dir, "analysis", "patient_flow")
    
    for d in [stat_dir, corr_dir, flow_dir]:
        os.makedirs(d, exist_ok=True)
        
    print(f"[1/4] Loading cleaned dataset from {clean_csv}...")
    df = pd.read_csv(clean_csv, low_memory=False)
    print(f"   -> Loaded {len(df)} records across {len(df.columns)} dimensions.")

    # -------------------------------------------------------------
    # 1. Statistical Analysis
    # -------------------------------------------------------------
    print("[2/4] Generating statistical benchmarks and distribution charts...")
    
    # Department-level aggregation
    dept_stats = df.groupby("Department").agg(
        Total_Patients=("Visit_ID", "count"),
        Avg_Doctor_Wait=("Doctor_Wait_Time", "mean"),
        Median_Doctor_Wait=("Doctor_Wait_Time", "median"),
        P90_Doctor_Wait=("Doctor_Wait_Time", lambda x: np.percentile(x, 90)),
        Avg_Total_Wait=("Total_Waiting_Time", "mean"),
        Avg_LOS=("Total_Length_of_Stay", "mean"),
        Avg_Bed_Occupancy=("Bed_Occupancy_Rate", "mean"),
        Avg_Bottleneck_Score=("Bottleneck_Score", "mean"),
        Emergency_Rate=("Patient_Type", lambda x: (x == "Emergency").mean() * 100),
        Diagnostic_Rate=("Diagnostic_Required", lambda x: (x == "Yes").mean() * 100)
    ).round(2).reset_index()

    dept_stats.sort_values(by="Avg_Doctor_Wait", ascending=False).to_csv(
        os.path.join(stat_dir, "department_summary_statistics.csv"), index=False
    )

    # Chart 1: Department Waiting Time Comparison (Horizontal bar with error bars)
    plt.figure(figsize=(10, 6), dpi=300)
    dept_order = dept_stats.sort_values(by="Avg_Doctor_Wait", ascending=True)
    colors = ["#d9534f" if score >= 60 else "#f0ad4e" if score >= 45 else "#337ab7" for score in dept_order["Avg_Bottleneck_Score"]]
    bars = plt.barh(dept_order["Department"], dept_order["Avg_Doctor_Wait"], color=colors, height=0.65, edgecolor="none")
    plt.title("Average Doctor Waiting Time by Clinical Department (Minutes)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Waiting Time (Minutes)", fontsize=11, labelpad=8)
    plt.ylabel("Department", fontsize=11)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"{w:.1f}m", va="center", fontsize=9, color="#333333")
    plt.xlim(0, max(dept_order["Avg_Doctor_Wait"]) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(stat_dir, "department_waiting_time_comparison.png"))
    plt.close()

    # Chart 2: Hourly Arrival Pattern (Emergency vs Outpatient)
    plt.figure(figsize=(10, 5), dpi=300)
    hourly_em = df[df["Department"] == "Emergency"].groupby("Hour")["Visit_ID"].count()
    hourly_op = df[df["Department"] != "Emergency"].groupby("Hour")["Visit_ID"].count()
    
    plt.plot(hourly_em.index, hourly_em.values, marker="o", color="#d9534f", linewidth=2.5, label="Emergency Department (24/7 Flow)")
    plt.plot(hourly_op.index, hourly_op.values, marker="s", color="#1b6ca8", linewidth=2.5, label="Outpatient Departments (Scheduled + Walk-in)")
    plt.title("Hourly Patient Arrival Distribution: Emergency vs Outpatient", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Hour of Arrival (00:00 to 23:00)", fontsize=11, labelpad=8)
    plt.ylabel("Total Patient Visits", fontsize=11, labelpad=8)
    plt.xticks(range(0, 24))
    plt.legend(frameon=True, facecolor="white", edgecolor="#e0e0e0")
    plt.tight_layout()
    plt.savefig(os.path.join(stat_dir, "hourly_arrival_patterns.png"))
    plt.close()

    # Chart 3: Length of Stay Distribution by Priority Level
    plt.figure(figsize=(9, 5), dpi=300)
    sns.boxplot(
        data=df, x="Priority_Level", y="Total_Length_of_Stay",
        order=["Critical", "High", "Medium", "Low"],
        palette=["#d9534f", "#f0ad4e", "#5bc0de", "#5cb85c"],
        showfliers=False, width=0.5
    )
    plt.title("Hospital Length of Stay (Minutes) across Patient Priority Tiers", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Triage Priority Level", fontsize=11, labelpad=8)
    plt.ylabel("Total Length of Stay (Minutes)", fontsize=11, labelpad=8)
    plt.tight_layout()
    plt.savefig(os.path.join(stat_dir, "los_distribution_by_priority.png"))
    plt.close()

    # -------------------------------------------------------------
    # 2. Correlation & Multidimensional Analysis
    # -------------------------------------------------------------
    print("[3/4] Calculating correlation matrix and multidimensional PCA projections...")
    
    corr_cols = [
        "Doctor_Wait_Time", "Total_Waiting_Time", "Total_Length_of_Stay",
        "Department_Capacity", "Staff_Availability", "Bed_Availability",
        "Bed_Occupancy_Rate", "Bottleneck_Score", "Hour"
    ]
    corr_matrix = df[corr_cols].corr().round(3)
    corr_matrix.to_csv(os.path.join(corr_dir, "correlation_matrix.csv"))

    # Chart 4: Correlation Heatmap
    plt.figure(figsize=(8, 7), dpi=300)
    sns.heatmap(
        corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True,
        square=True, linewidths=0.5, annot_kws={"size": 9}
    )
    plt.title("Correlation Matrix: Operational & Waiting Time Variables", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(corr_dir, "correlation_matrix.png"))
    plt.close()

    # Chart 5: Volume vs Waiting Time Scatter Plot
    # Aggregate by Department and Hour to visualize operational pressure points
    dept_hour = df.groupby(["Department", "Hour"]).agg(
        Patient_Volume=("Visit_ID", "count"),
        Avg_Wait=("Doctor_Wait_Time", "mean"),
        Avg_Capacity=("Department_Capacity", "first"),
        Bottleneck_Score=("Bottleneck_Score", "mean")
    ).reset_index()

    plt.figure(figsize=(10, 6), dpi=300)
    scatter = plt.scatter(
        dept_hour["Patient_Volume"], dept_hour["Avg_Wait"],
        s=dept_hour["Avg_Capacity"] * 4,
        c=dept_hour["Bottleneck_Score"],
        cmap="YlOrRd", alpha=0.8, edgecolors="#444444", linewidths=0.5
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("Bottleneck Score (0-100)", fontsize=10)
    plt.title("Patient Volume vs. Doctor Waiting Time (Department-Hour Clusters)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Hourly Patient Volume (Visits per Hour)", fontsize=11, labelpad=8)
    plt.ylabel("Average Doctor Waiting Time (Minutes)", fontsize=11, labelpad=8)
    
    # Annotate critical bottleneck quadrants
    plt.axvline(x=25, color="#888888", linestyle="--", alpha=0.6)
    plt.axhline(y=45, color="#888888", linestyle="--", alpha=0.6)
    plt.text(26, max(dept_hour["Avg_Wait"]) * 0.92, "High Volume + High Wait\n(Critical Bottleneck Quadrant)",
             fontsize=9, color="#b30000", fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc="#ffeeee", ec="#b30000", lw=0.8))
    plt.tight_layout()
    plt.savefig(os.path.join(corr_dir, "volume_vs_wait_scatter.png"))
    plt.close()

    # Chart 6: PCA 2D Dimensionality Reduction
    pca_features = df[corr_cols].dropna()
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pca_features)
    pca = PCA(n_components=2, random_state=42)
    pca_proj = pca.fit_transform(scaled_data)
    
    plt.figure(figsize=(9, 6), dpi=300)
    plt.scatter(
        pca_proj[:, 0], pca_proj[:, 1],
        c=df["Bottleneck_Score"], cmap="viridis", alpha=0.4, s=12
    )
    plt.colorbar(label="Bottleneck Score")
    plt.title(f"PCA 2D Operational State Projection (Explains {sum(pca.explained_variance_ratio_)*100:.1f}% Variance)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)", fontsize=11)
    plt.ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(corr_dir, "pca_multidimensional_projection.png"))
    plt.close()

    # -------------------------------------------------------------
    # 3. Patient Flow & Network Journey Analysis
    # -------------------------------------------------------------
    print("[4/4] Mapping patient journey stages, transition funnels, and congestion heatmaps...")

    # Stage completion metrics
    total_arrivals = len(df)
    total_registered = (df["Registration_Time"] != "").sum()
    total_triaged = (df["Triage_Start_Time"] != "").sum()
    total_consulted = (df["Doctor_Consultation_Start"] != "").sum()
    total_diagnostics = (df["Diagnostic_Required"] == "Yes").sum()
    total_treated = (df["Treatment_Start"] != "").sum()
    total_pharmacy = (df["Pharmacy_Required"] == "Yes").sum()
    total_discharged = (df["Discharge_Time"] != "").sum()

    stage_funnel_df = pd.DataFrame([
        {"Stage": "1. Arrival", "Count": total_arrivals, "Completion_Pct": 100.0},
        {"Stage": "2. Registration", "Count": total_registered, "Completion_Pct": round(total_registered/total_arrivals * 100, 1)},
        {"Stage": "3. Triage", "Count": total_triaged, "Completion_Pct": round(total_triaged/total_arrivals * 100, 1)},
        {"Stage": "4. Doctor Consult", "Count": total_consulted, "Completion_Pct": round(total_consulted/total_arrivals * 100, 1)},
        {"Stage": "5. Diagnostics (Conditional)", "Count": total_diagnostics, "Completion_Pct": round(total_diagnostics/total_arrivals * 100, 1)},
        {"Stage": "6. Treatment (Conditional)", "Count": total_treated, "Completion_Pct": round(total_treated/total_arrivals * 100, 1)},
        {"Stage": "7. Pharmacy (Conditional)", "Count": total_pharmacy, "Completion_Pct": round(total_pharmacy/total_arrivals * 100, 1)},
        {"Stage": "8. Discharge", "Count": total_discharged, "Completion_Pct": round(total_discharged/total_arrivals * 100, 1)}
    ])
    stage_funnel_df.to_csv(os.path.join(flow_dir, "stage_funnel_summary.csv"), index=False)

    # Chart 7: Patient Journey Funnel
    plt.figure(figsize=(9, 5), dpi=300)
    bars = plt.barh(stage_funnel_df["Stage"][::-1], stage_funnel_df["Count"][::-1], color="#2c7bb6", height=0.6)
    plt.title("Patient Progression Funnel Across Clinical Stages", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Patient Volume", fontsize=11, labelpad=8)
    for bar in bars:
        w = bar.get_width()
        pct = (w / total_arrivals) * 100
        plt.text(w + 400, bar.get_y() + bar.get_height()/2, f"{w:,} ({pct:.1f}%)", va="center", fontsize=9)
    plt.xlim(0, total_arrivals * 1.18)
    plt.tight_layout()
    plt.savefig(os.path.join(flow_dir, "patient_journey_funnel.png"))
    plt.close()

    # Chart 8: Stage Duration Breakdown by Department
    stage_waits = df.groupby("Department").agg(
        Registration=("Registration_Wait_Time", "mean"),
        Triage=("Triage_Wait_Time", "mean"),
        Doctor=("Doctor_Wait_Time", "mean"),
        Diagnostic=("Diagnostic_Wait_Time", "mean"),
        Treatment=("Treatment_Wait_Time", "mean"),
        Pharmacy=("Pharmacy_Wait_Time", "mean")
    ).round(1)
    stage_waits.to_csv(os.path.join(flow_dir, "stage_wait_by_department.csv"))

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    stage_waits.plot(
        kind="bar", stacked=True, ax=ax,
        color=["#6baed6", "#fd8d3c", "#e6550d", "#74c476", "#9e9ac8", "#969696"],
        width=0.75, edgecolor="none"
    )
    plt.title("Cumulative Waiting Time Composition by Stage Across Departments", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Clinical Department", fontsize=11, labelpad=8)
    plt.ylabel("Cumulative Waiting Time (Minutes)", fontsize=11, labelpad=8)
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Stage Component", frameon=True, facecolor="white", edgecolor="#e0e0e0")
    plt.tight_layout()
    plt.savefig(os.path.join(flow_dir, "stage_duration_breakdown.png"))
    plt.close()

    # Chart 9: Heatmap of Arrivals (Day of Week vs Hour)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = df.pivot_table(index="Day_of_Week", columns="Hour", values="Visit_ID", aggfunc="count").reindex(day_order)
    
    plt.figure(figsize=(12, 5), dpi=300)
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False, cbar_kws={"label": "Total Patient Visits"})
    plt.title("Hospital Patient Arrival Heatmap (Day of Week vs. Hour of Day)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Hour of Day (00 to 23)", fontsize=11, labelpad=8)
    plt.ylabel("Day of Week", fontsize=11, labelpad=8)
    plt.tight_layout()
    plt.savefig(os.path.join(flow_dir, "hourly_day_heatmap.png"))
    plt.close()

    print("[DONE] Patient flow, correlation, and statistical analysis completed successfully.")

if __name__ == "__main__":
    run_analysis()
