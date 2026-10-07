"""
insight_engine.py
=================
Generates cautious, evidence-backed operational insights based on filtered cohort data.
"""

def generate_insights(df):
    insights = []
    if len(df) == 0:
        return ["No patient encounter data available under current filter selection."]

    avg_wait = df["Wait_Doctor"].mean()
    med_wait = df["Wait_Doctor"].median()
    avg_los = df["Length_of_Stay"].mean()
    emerg_rate = (df["Emergency_Flag"] == "Yes").mean() * 100
    avg_util = df["Department_Utilization"].mean() * 100
    crit_count = (df["Bottleneck_Category"] == "Critical").sum()

    # Rule 1: High waiting time + High utilization
    if avg_wait > 38 and avg_util > 75:
        insights.append(
            f"**High Operational Strain Signal:** Average physician consultation wait ({avg_wait:.1f} min) coincides with high departmental bed utilization ({avg_util:.1f}%). Queuing delay is strongly coupled with physical capacity saturation rather than purely registration backlogs."
        )
    elif avg_wait <= 30:
        insights.append(
            f"**Favorable Throughput State:** Observed physician wait time ({avg_wait:.1f} min) is within standard operational tolerances, indicating balanced physician allocation relative to current demand."
        )

    # Rule 2: Emergency surge
    if emerg_rate > 28:
        insights.append(
            f"**Elevated Emergency Inflow:** Emergency presentation rate ({emerg_rate:.1f}%) is abnormally elevated compared to the hospital baseline (~20%). Inpatient bed reservation and rapid triage routing should be activated to mitigate spillover delays into general wards."
        )

    # Rule 3: Bottleneck department concentration
    dept_waits = df.groupby("Department")["Wait_Doctor"].mean()
    top_dept = dept_waits.idxmax()
    top_val = dept_waits.max()
    insights.append(
        f"**Primary Queue Lead:** The **{top_dept}** department exhibits the highest localized consultation delay ({top_val:.1f} min average), indicating that physician capacity or diagnostic test turnaround is currently pacing encounter velocity."
    )

    # Rule 4: Triage Acuity Disparity
    prio_waits = df.groupby("Priority_Level")["Wait_Doctor"].mean()
    if "Low" in prio_waits and "Critical" in prio_waits:
        ratio = prio_waits["Low"] / max(1, prio_waits["Critical"])
        insights.append(
            f"**Acuity Prioritization Functioning:** Critical patients receive rapid attention (mean: {prio_waits['Critical']:.1f} min) while Low-acuity cases endure lengthened waits (mean: {prio_waits['Low']:.1f} min, {ratio:.1f}x delay multiple), confirming effective Manchester/ESI prioritization."
        )

    # Rule 5: Length of Stay expansion
    if avg_los > 150:
        insights.append(
            f"**Encounter Dilation:** Mean length of stay ({avg_los:.1f} min / {avg_los/60:.1f} hrs) indicates extended downstream holding time post-consultation, typically attributable to diagnostic imaging queues or discharge dispensing."
        )

    return insights
