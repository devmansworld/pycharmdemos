import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime

# Function to calculate team efficiency
def calculate_team_efficiency(df):
    team_efficiency = {}

    for team in df["Team"].unique():
        team_data = df[df["Team"] == team]
        total_projects = len(team_data)

        # Count completed projects without NaN values
        completed_projects = len(team_data[(team_data["Risk Level"].fillna("Unknown") == "Low") & ~team_data["Actual Finish Date"].isna()])

        efficiency = (completed_projects / total_projects) * 100 if total_projects > 0 else 0
        team_efficiency[team] = efficiency

    return team_efficiency

# Function to save data to JSON
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to save data to XLSX and generate a pie chart
def save_to_xlsx_and_pie(data, filename):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Efficiency'])

    # Filter out rows with NaN values
    df = df.dropna()

    # Check if there is valid data to create the pie chart
    if not df.empty:
        # Save data to XLSX
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Efficiency Data')

            if not df.empty:
                # Create a pie chart
                pie_chart = plt.figure(figsize=(6, 6))
                ax = pie_chart.add_subplot(111)
                ax.pie(df['Efficiency'], labels=df.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                pie_chart.savefig(writer, sheet_name='Efficiency Pie Chart')
                plt.close(pie_chart)
    else:
        print("No valid data available for the pie chart.")

data = []
while True:
    project_name = input("Enter project name (or 'exit' to quit): ")
    if project_name.lower() == 'exit':
        break

    risk_level = input("Enter risk level (Low, High, Moderate): ")
    risk_comment = input("Enter risk comment: ")
    dependencies = input("Enter project dependencies (comma-separated): ")
    team = input("Enter testing team: ")

    # Collect additional data
    expected_start_date = input("Enter expected start date (YYYY-MM-DD): ")
    actual_start_date = input("Enter actual start date (YYYY-MM-DD): ")
    expected_finish_date = input("Enter expected finish date (YYYY-MM-DD): ")
    actual_finish_date = input("Enter actual finish date (YYYY-MM-DD): ")

    data.append({
        "Project Name": project_name,
        "Risk Level": risk_level,
        "Risk Comment": risk_comment,
        "Dependencies": dependencies,
        "Team": team,
        "Expected Start Date": expected_start_date,
        "Actual Start Date": actual_start_date,
        "Expected Finish Date": expected_finish_date,
        "Actual Finish Date": actual_finish_date,
    })

# Create a DataFrame from input data
df = pd.DataFrame(data)

# Calculate team efficiency
team_efficiency = calculate_team_efficiency(df)

# Display team efficiency
print("Team Efficiency:")
print("=" * 40)
for team, efficiency in team_efficiency.items():
    print(f"Team: {team}, Efficiency: {efficiency:.2f}%")

# Save data to JSON
json_filename = 'project_data.json'
save_to_json(data, json_filename)
print(f"Data saved to {json_filename}")

# Save data to XLSX and generate a pie chart
xlsx_filename = 'project_efficiency.xlsx'
save_to_xlsx_and_pie(team_efficiency, xlsx_filename)
print(f"Data saved to {xlsx_filename}")
