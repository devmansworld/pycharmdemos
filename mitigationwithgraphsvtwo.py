import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

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

# Display project data with dependencies and mitigation strategies
print("Project Data with Dependencies and Mitigation Strategies")
print("=" * 55)
print(df)

# Convert risk comment to start and end dates for the Gantt chart
df["Start Date"] = datetime.now()
df["End Date"] = df["Start Date"] + pd.to_timedelta(7, unit="d")  # Assume a 7-day duration for each mitigation

# Create a Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.barh(df["Project Name"], left=df["Start Date"], width=df["End Date"] - df["Start Date"], color="lightblue")
ax.set_xlabel("Timeline")
ax.set_ylabel("Project Name")
ax.set_title("Mitigation Strategy Gantt Chart")

# Display the Gantt chart
plt.show()
