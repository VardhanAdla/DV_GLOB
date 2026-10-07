"""
app.py
======
Hospital Patient Flow Intelligence - Interactive Multi-Page Streamlit Dashboard
Course Code: GR24A3144 (Data Visualization Lab)

Pages:
    1. Overview (Executive Flow Overview)
    2. Department Bottlenecks (Bottleneck & Waiting Time Analytics)
    3. Patient Journey (Stage Decomposition & Funnel)
    4. Operational Intelligence (Parameter-driven dynamic monitoring & anomalies)
    5. Data Explorer (Patient & Visit ID drilldown, raw inspection, downloads)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from components.charts import (
    plot_hourly_arrivals, plot_dept_volume, plot_volume_vs_wait_scatter,
    plot_bottleneck_heatmap, plot_journey_funnel, plot_stage_duration_stacked,
    plot_los_by_priority, plot_dynamic_metric, plot_day_of_week_heatmap
)
from components.insight_engine import generate_insights

st.set_page_config(
    page_title="Hospital Patient Flow Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    csv_path = os.path.join(base_dir, "data", "processed", "hospital_patient_flow_clean.csv")
    df = pd.read_csv(csv_path, low_memory=False)
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"])
    return df

@st.cache_data
def load_stage_data():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    csv_path = os.path.join(base_dir, "analysis", "patient_journey_stages.csv")
    return pd.read_csv(csv_path)

df_raw = load_data()
stage_df = load_stage_data()

# Sidebar Navigation & Global Filters
st.sidebar.title("🏥 Patient Flow Intelligence")
st.sidebar.caption("Course: GR24A3144 (Data Visualization Lab)")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Department Bottlenecks", "Patient Journey", "Operational Intelligence", "Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Pipeline")

# Date range
min_date = df_raw["Arrival_Date"].min().date()
max_date = df_raw["Arrival_Date"].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Department
all_depts = sorted(df_raw["Department"].unique().tolist())
selected_depts = st.sidebar.multiselect("Department(s)", all_depts, default=all_depts)

# Priority
all_prios = ["Critical", "High", "Medium", "Low"]
selected_prios = st.sidebar.multiselect("Priority Tier", all_prios, default=all_prios)

# Shift
all_shifts = ["Morning", "Afternoon", "Night"]
selected_shifts = st.sidebar.multiselect("Operational Shift", all_shifts, default=all_shifts)

# Emergency Flag
emerg_filter = st.sidebar.selectbox("Emergency Presentation", ["All", "Emergency Only (Yes)", "Elective / OPD Only (No)"])

# Apply Filters
mask = (
    (df_raw["Department"].isin(selected_depts)) &
    (df_raw["Priority_Level"].isin(selected_prios)) &
    (df_raw["Shift"].isin(selected_shifts))
)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = date_range
    mask &= (df_raw["Arrival_Date"].dt.date >= start_d) & (df_raw["Arrival_Date"].dt.date <= end_d)

if emerg_filter == "Emergency Only (Yes)":
    mask &= (df_raw["Emergency_Flag"] == "Yes")
elif emerg_filter == "Elective / OPD Only (No)":
    mask &= (df_raw["Emergency_Flag"] == "No")

df = df_raw[mask].copy()

# ==============================================================================
# PAGE 1: OVERVIEW
# ==============================================================================
if page == "Overview":
    st.markdown('<div class="main-header">Hospital Flow Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive Healthcare Operations Pulse & Patient Volume Trends</div>', unsafe_allow_html=True)

    # Top KPI Strip
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Patients", f"{len(df):,}")
    with k2:
        st.metric("Avg Doctor Wait", f"{df['Wait_Doctor'].mean():.1f} min", delta=f"{df['Wait_Doctor'].mean()-30.0:.1f}m vs SLA", delta_color="inverse")
    with k3:
        st.metric("Median Wait Time", f"{df['Wait_Doctor'].median():.1f} min")
    with k4:
        st.metric("Avg Length of Stay", f"{df['Length_of_Stay'].mean():.1f} min")
    with k5:
        em_pct = (df['Emergency_Flag'] == 'Yes').mean() * 100 if len(df) > 0 else 0
        st.metric("Emergency Inflow", f"{em_pct:.1f}%")

    st.markdown("---")

    # Visualizations
    c1, c2 = st.columns([6, 5])
    with c1:
        st.plotly_chart(plot_hourly_arrivals(df), use_container_width=True)
    with c2:
        st.plotly_chart(plot_dept_volume(df), use_container_width=True)

    # Automated Operational Insights
    st.subheader("💡 Operational Observations")
    insights = generate_insights(df)
    for ins in insights:
        st.markdown(f'<div class="insight-box">{ins}</div>', unsafe_allow_html=True)

# ==============================================================================
# PAGE 2: DEPARTMENT BOTTLENECKS
# ==============================================================================
elif page == "Department Bottlenecks":
    st.markdown('<div class="main-header">Department Bottleneck Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Pinpoint Queue Stagnation, Volume-Wait Quadrants, and Capacity Pressure</div>', unsafe_allow_html=True)

    st.info("Academic Model Disclaimer: Bottleneck scoring is an academic analytical model and is not a clinically validated hospital standard.")

    b1, b2 = st.columns([6, 5])
    with b1:
        st.plotly_chart(plot_volume_vs_wait_scatter(df), use_container_width=True)
    with b2:
        st.plotly_chart(plot_stage_duration_stacked(df), use_container_width=True)

    st.plotly_chart(plot_bottleneck_heatmap(df), use_container_width=True)

    # Ranking Table
    st.subheader("Department Bottleneck Performance Ranking")
    ranking_df = df.groupby("Department").agg(
        Visits=("Visit_ID", "count"),
        Avg_Doctor_Wait=("Wait_Doctor", "mean"),
        Median_Wait=("Wait_Doctor", "median"),
        Avg_Bottleneck_Score=("Bottleneck_Score", "mean"),
        Bed_Utilization=("Department_Utilization", lambda x: f"{x.mean()*100:.1f}%")
    ).round(1).sort_values(by="Avg_Bottleneck_Score", ascending=False).reset_index()
    st.dataframe(ranking_df, use_container_width=True)

# ==============================================================================
# PAGE 3: PATIENT JOURNEY
# ==============================================================================
elif page == "Patient Journey":
    st.markdown('<div class="main-header">Patient Journey & Waiting-Time Decomposition</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Track Stage-by-Stage Care Transitions from Arrival to Discharge</div>', unsafe_allow_html=True)

    j1, j2 = st.columns([5, 6])
    with j1:
        st.plotly_chart(plot_journey_funnel(stage_df), use_container_width=True)
    with j2:
        st.plotly_chart(plot_los_by_priority(df), use_container_width=True)

    st.subheader("Stage Breakdown Metrics")
    st.dataframe(stage_df, use_container_width=True)

# ==============================================================================
# PAGE 4: OPERATIONAL INTELLIGENCE
# ==============================================================================
elif page == "Operational Intelligence":
    st.markdown('<div class="main-header">Operational Intelligence & Capacity Stress Testing</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Parameter-Driven Dynamic Trends, Heatmaps, and Operational Anomaly Alerts</div>', unsafe_allow_html=True)

    # Parameter Controller
    metric_choice = st.selectbox(
        "SELECT ANALYSIS METRIC",
        ["Patient Volume", "Waiting Time", "Length of Stay", "Emergency Percentage", "Capacity Pressure", "Department Utilization", "Bottleneck Score"]
    )

    st.plotly_chart(plot_dynamic_metric(df, metric_choice), use_container_width=True)

    o1, o2 = st.columns([6, 5])
    with o1:
        st.plotly_chart(plot_day_of_week_heatmap(df), use_container_width=True)
    with o2:
        st.subheader("🚨 Operational Anomaly Alerts")
        anom_records = df[df["Anomaly_Flag"] == "Yes"][["Visit_ID", "Arrival_Date", "Department", "Shift", "Wait_Doctor", "Anomaly_Type"]].head(25)
        st.write(f"Total Anomalous Episodes Flagged: **{(df['Anomaly_Flag'] == 'Yes').sum():,}**")
        st.dataframe(anom_records, use_container_width=True)

# ==============================================================================
# PAGE 5: DATA EXPLORER
# ==============================================================================
elif page == "Data Explorer":
    st.markdown('<div class="main-header">Patient & Visit Data Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Deep-Dive Encounter Audit, Primary Key Search, and Export</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    with s1:
        search_visit = st.text_input("Search by Visit_ID (e.g. V-2025-00100):").strip()
    with s2:
        search_patient = st.text_input("Search by Patient_ID (e.g. P-10025):").strip()

    filtered_view = df
    if search_visit:
        filtered_view = df_raw[df_raw["Visit_ID"].str.contains(search_visit, case=False, na=False)]
    elif search_patient:
        filtered_view = df_raw[df_raw["Patient_ID"].str.contains(search_patient, case=False, na=False)]

    st.write(f"Displaying **{len(filtered_view):,}** matched records:")
    st.dataframe(filtered_view.head(100), use_container_width=True)

    # CSV Download Button
    csv_bytes = filtered_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="hospital_patient_flow_filtered.csv",
        mime="text/csv"
    )
