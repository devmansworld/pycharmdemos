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

# Convert risk comment to start and end dates for the Gantt chart
start_date = datetime.now()

# Define unique colors for each project
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

# Create a Gantt chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

for i, row in df.iterrows():
    end_date = start_date + timedelta(days=7)  # 7-day duration for each mitigation
    project_name = row["Project Name"]
    color = colors[i % len(colors)]

    ax.barh(project_name, left=start_date, width=end_date - start_date, color=color, label=project_name)
    start_date = end_date  # Update start_date for the next project

ax.set_xlabel("Timeline")
ax.set_ylabel("Project Name")
ax.set_title("Mitigation Strategy Gantt Chart")

# Display the Gantt chart with a legend
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

plt.show()
