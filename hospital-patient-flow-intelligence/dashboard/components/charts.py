"""
charts.py
=========
Reusable Plotly charts for Hospital Patient Flow Intelligence Streamlit application.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLOR_MAP = {
    "Critical": "#d9534f",
    "High": "#f0ad4e",
    "Moderate": "#5bc0de",
    "Low": "#5cb85c"
}

def plot_hourly_arrivals(df):
    hourly = df.groupby(["Hour", "Department"]).size().reset_index(name="Visits")
    fig = px.line(
        hourly, x="Hour", y="Visits", color="Department",
        title="Hourly Patient Arrival Pattern Across Clinical Departments",
        labels={"Hour": "Hour of Day (00 to 23)", "Visits": "Total Patient Encounters"},
        template="plotly_white"
    )
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=1), hovermode="x unified")
    return fig

def plot_dept_volume(df):
    dept_vol = df.groupby(["Department", "Bottleneck_Category"]).size().reset_index(name="Volume")
    dept_order = df.groupby("Department").size().sort_values(ascending=False).index.tolist()
    fig = px.bar(
        dept_vol, x="Department", y="Volume", color="Bottleneck_Category",
        color_discrete_map=COLOR_MAP,
        category_orders={"Department": dept_order},
        title="Department Patient Intake Volume Segmented by Bottleneck Severity Tier",
        labels={"Volume": "Patient Visits"},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-30)
    return fig

def plot_volume_vs_wait_scatter(df):
    dept_hour = df.groupby(["Department", "Hour", "Bottleneck_Category"]).agg(
        Patient_Volume=("Visit_ID", "count"),
        Avg_Wait=("Wait_Doctor", "mean"),
        Capacity=("Department_Capacity", "first")
    ).reset_index()

    fig = px.scatter(
        dept_hour, x="Patient_Volume", y="Avg_Wait", size="Capacity",
        color="Bottleneck_Category", color_discrete_map=COLOR_MAP,
        hover_data=["Department", "Hour"],
        title="Department Volume vs. Average Doctor Wait Time (Quadrant Bottleneck Analysis)",
        labels={"Patient_Volume": "Hourly Patient Inflow", "Avg_Wait": "Avg Doctor Wait (min)"},
        template="plotly_white"
    )
    fig.add_hline(y=45, line_dash="dash", line_color="#d9534f", annotation_text="Hospital SLA Target (45 min)")
    return fig

def plot_bottleneck_heatmap(df):
    matrix = df.pivot_table(index="Department", columns="Hour", values="Bottleneck_Score", aggfunc="mean").round(1)
    fig = px.imshow(
        matrix,
        labels=dict(x="Hour of Day", y="Clinical Department", color="Bottleneck Score"),
        x=matrix.columns, y=matrix.index,
        color_continuous_scale="YlOrRd",
        title="12-Department x 24-Hour Congestion Heatmap (Bottleneck Score: 0-100)"
    )
    fig.update_xaxes(tickmode="linear", dtick=1)
    return fig

def plot_journey_funnel(stage_df):
    fig = go.Figure(go.Funnel(
        y=stage_df["Stage_Order"],
        x=stage_df["Contribution_To_Total_Wait_Pct"],
        textinfo="value+percent initial",
        marker={"color": ["#1b6ca8", "#2a80b9", "#3b94ca", "#50a8dc", "#6abced", "#86d0ff"]}
    ))
    fig.update_layout(
        title="Patient Journey Stages: Contribution % to Total Hospital Waiting Delays",
        template="plotly_white"
    )
    return fig

def plot_stage_duration_stacked(df):
    stage_waits = df.groupby("Department").agg(
        Registration=("Wait_Registration", "mean"),
        Triage=("Wait_Triage", "mean"),
        Doctor=("Wait_Doctor", "mean"),
        Diagnostic=("Wait_Diagnostics", "mean"),
        Treatment=("Wait_Treatment", "mean"),
        Pharmacy=("Wait_Pharmacy", "mean")
    ).round(1).reset_index()

    fig = px.bar(
        stage_waits, x="Department",
        y=["Registration", "Triage", "Doctor", "Diagnostic", "Treatment", "Pharmacy"],
        title="Cumulative Queue Waiting Time Decomposition Across Clinical Departments",
        labels={"value": "Mean Delay (Minutes)", "variable": "Care Stage"},
        template="plotly_white"
    )
    fig.update_layout(barmode="stack", xaxis_tickangle=-30)
    return fig

def plot_los_by_priority(df):
    fig = px.box(
        df, x="Priority_Level", y="Length_of_Stay", color="Priority_Level",
        category_orders={"Priority_Level": ["Critical", "High", "Medium", "Low"]},
        color_discrete_map={"Critical": "#d9534f", "High": "#f0ad4e", "Medium": "#5bc0de", "Low": "#5cb85c"},
        title="Hospital Encounter Length of Stay (Minutes) across Triage Acuity Tiers",
        template="plotly_white"
    )
    return fig

def plot_dynamic_metric(df, metric_choice):
    metric_map = {
        "Patient Volume": ("Visit_ID", "count", "Total Patients"),
        "Waiting Time": ("Wait_Doctor", "mean", "Average Doctor Wait (min)"),
        "Length of Stay": ("Length_of_Stay", "mean", "Average LOS (min)"),
        "Emergency Percentage": ("Emergency_Flag", lambda x: (x == "Yes").mean() * 100, "Emergency Inflow %"),
        "Capacity Pressure": ("Capacity_Pressure", "mean", "Mean Capacity Pressure Index"),
        "Department Utilization": ("Department_Utilization", lambda x: x.mean() * 100, "Mean Bed Utilization %"),
        "Bottleneck Score": ("Bottleneck_Score", "mean", "Average Bottleneck Score (0-100)")
    }
    col, agg, title_lbl = metric_map[metric_choice]
    daily = df.groupby("Arrival_Date").agg(Val=(col, agg)).reset_index()

    fig = px.area(
        daily, x="Arrival_Date", y="Val",
        title=f"Dynamic Operational Trend: {metric_choice} (Jan - Oct 2025)",
        labels={"Arrival_Date": "Encounter Date", "Val": title_lbl},
        template="plotly_white"
    )
    fig.update_traces(line_color="#1b6ca8", fillcolor="rgba(27, 108, 168, 0.25)")
    return fig

def plot_day_of_week_heatmap(df):
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_matrix = df.pivot_table(index="Day_of_Week", columns="Hour", values="Visit_ID", aggfunc="count").reindex(day_order)
    fig = px.imshow(
        dow_matrix,
        labels=dict(x="Hour of Day", y="Day of Week", color="Patient Volume"),
        x=dow_matrix.columns, y=dow_matrix.index,
        color_continuous_scale="Viridis",
        title="Patient Arrival Congestion Grid (Day of Week vs. Hour of Day)"
    )
    return fig
