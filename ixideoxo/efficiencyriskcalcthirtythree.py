import pandas as pd
import json
import os
from datetime import datetime
from faker import Faker

# ... (Previous code remains the same)

# Function to generate fake project execution data
def generate_fake_execution_data(project_name, actual_start_date, actual_finish_date):
    fake_execution_data = []
    num_days = (datetime.strptime(actual_finish_date, '%Y-%m-%d') - datetime.strptime(actual_start_date, '%Y-%m-%d')).days + 1

    for day in range(num_days):
        date = (datetime.strptime(actual_start_date, '%Y-%m-%d') + timedelta(days=day)).strftime('%Y-%m-%d')
        completed = fake.random_element(elements=(True, False))
        fake_execution_data.append({
            "Date": date,
            "Project Name": project_name,
            "Completed": completed,
        })

    return fake_execution_data

# ... (Rest of the code remains the same)

data = []
execution_data = []
teams = {}
fake = Faker()

# ... (Previous code remains the same)

# Function to load execution data from XLSX files in the execution folder
def load_execution_data():
    execution_data = []
    for filename in os.listdir("execution"):
        if filename.endswith(".xlsx"):
            df = pd.read_excel(os.path.join("execution", filename))
            execution_data.append(df)
    if execution_data:
        return pd.concat(execution_data, ignore_index=True)
    return pd.DataFrame()

execution_df = load_execution_data()

if generate_test_data.lower() == 'yes':
    num_projects = int(input("Enter the number of projects to generate: "))
    test_data = []

    for _ in range(num_projects):
        # ... (Rest of the code remains the same)

        project_data = {
            "Project Name": project_name,
            "Risk Level": risk_level,
            "Risk Comment": risk_comment,
            "Dependencies": dependencies,
            "Team": team,
            "Expected Start Date": expected_start_date,
            "Actual Start Date": actual_start_date,
            "Expected Finish Date": expected_finish_date,
            "Actual Finish Date": actual_finish_date,
            "Risk Qualification": risk_qualifications.get(risk_level.lower(), "Unknown"),
        }

        test_data.append(project_data)

    data.extend(test_data)
else:
    while True:
        # ... (Rest of the code remains the same)

        risk_data = {
            "Project Name": project_name,
            "Risk Level": risk_level,
            "Risk Comment": risk_comment,
            "Dependencies": dependencies.split(','),
            "Team": team,
            "Expected Start Date": expected_start_date,
            "Actual Start Date": actual_start_date,
            "Expected Finish Date": expected_finish_date,
            "Actual Finish Date": actual_finish_date,
            "Risk Qualification": risk_qualifications.get(risk_level.lower(), "Unknown"),
        }

        if team not in teams:
            teams[team] = []
        teams[team].append(risk_data)

data.extend(teams.values())

df = pd.DataFrame(data)

# Merge execution data with project data
if not execution_df.empty:
    df = df.merge(execution_df, on="Project Name", how="left")

team_efficiency_data = {}
for team, team_projects in teams.items():
    efficiency = calculate_team_efficiency(team_projects)
    team_efficiency_data[team] = efficiency

team_efficiency = calculate_team_efficiency(df)

print("Team Efficiency:")
print("=" * 40)
for team, efficiency in team_efficiency_data.items():
    print(f"Team: {team}, Efficiency: {efficiency:.2f}%")

print("Entered Data:")
print("=" * 40)
for item in data:
    print(f"Project Name: {item['Project Name']}")
    print(f"Risk Level: {item['Risk Level']}")
    print(f"Risk Qualification: {item['Risk Qualification']}")
    print("=" * 20)

json_filename = save_to_json(data)
print(f"Data saved to {json_filename}")

xlsx_filename = save_to_xlsx(team_efficiency_data)
print(f"Data saved to {xlsx_filename}")
