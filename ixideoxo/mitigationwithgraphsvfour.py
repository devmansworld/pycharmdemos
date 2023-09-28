import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Sample project data with dependencies (replace with your actual data)
data = {
    "Project Name": ["Project A", "Project B", "Project C", "Project D", "Project E", "Project F", "Project G"],
    "Risk Level": ["Low", "High", "Moderate", "High", "Moderate", "Low", "Moderate"],
    "Risk Comment": [
        "Testing completed within the expected time.",
        "Testing took longer than expected.",
        "No risk identified.",
        "Testing took longer than expected.",
        "No risk identified.",
        "Testing completed within the expected time.",
        "No risk identified.",
    ],
    "Dependencies": ["", "", "A", "C", "", "B", "A"],
}

df = pd.DataFrame(data)

# Function to generate mitigation strategies based on risk level
def generate_mitigation_strategy(row):
    risk_level = row["Risk Level"]
    risk_comment = row["Risk Comment"]

    if risk_level == "Low":
        return "No specific mitigation strategy required."
    elif risk_level == "Moderate":
        return f"Mitigation strategy: {risk_comment}"
    else:
        return f"Mitigation strategy: {risk_comment}. Consider allocating additional resources."

# Apply mitigation strategy generation to each row
df["Mitigation Strategy"] = df.apply(generate_mitigation_strategy, axis=1)

# Create a dictionary to track project start dates based on dependencies
project_start_dates = {}
start_date = datetime.now()

for _, row in df.iterrows():
    project_name = row["Project Name"]
    dependencies = row["Dependencies"].split(", ") if row["Dependencies"] else []

    if not dependencies:
        project_start_dates[project_name] = start_date
    else:
        max_dependency_end_date = max(project_start_dates.get(dep, start_date) for dep in dependencies)
        project_start_dates[project_name] = max_dependency_end_date + timedelta(days=1)

# Convert start dates to a DataFrame
start_dates_df = pd.DataFrame(list(project_start_dates.items()), columns=["Project Name", "Start Date"])

# Merge the start dates DataFrame with the original data
df = df.merge(start_dates_df, on="Project Name")

# Convert risk comment to end dates for the Gantt chart
df["End Date"] = df["Start Date"] + pd.to_timedelta(7, unit="d")  # 7-day duration for each mitigation

# Define unique colors for each project
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

# Create a Gantt chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

for i, row in df.iterrows():
    project_name = row["Project Name"]
    color = colors[i % len(colors)]

    ax.barh(
        project_name,
        left=row["Start Date"],
        width=row["End Date"] - row["Start Date"],
        color=color,
        label=project_name
    )

ax.set_xlabel("Timeline")
ax.set_ylabel("Project Name")
ax.set_title("Mitigation Strategy Gantt Chart")

# Display the Gantt chart with a legend
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

plt.show()
