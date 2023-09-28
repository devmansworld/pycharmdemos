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
    "Team": ["Team 1", "Team 2", "Team 3", "Team 2", "Team 4", "Team 1", "Team 3"],  # Testing teams
}

df = pd.DataFrame(data)

# Function to calculate team efficiency
def calculate_team_efficiency(df):
    team_efficiency = {}

    for team in df["Team"].unique():
        team_data = df[df["Team"] == team]
        total_projects = len(team_data)
        completed_projects = len(team_data[team_data["Risk Level"] == "Low"])

        efficiency = (completed_projects / total_projects) * 100 if total_projects > 0 else 0
        team_efficiency[team] = efficiency

    return team_efficiency

# Calculate team efficiency
team_efficiency = calculate_team_efficiency(df)

# Display team efficiency
print("Team Efficiency:")
print("=" * 40)
for team, efficiency in team_efficiency.items():
    print(f"Team: {team}, Efficiency: {efficiency:.2f}%")
