import pandas as pd
import json
from datetime import datetime
from faker import Faker

# Function to validate and get a valid date input
def get_valid_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            if date_str.lower() == 'exit':
                return None
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date.strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format or 'exit' to quit.")

# Function to calculate team efficiency
def calculate_team_efficiency(team_projects):
    completed_projects = 0
    total_projects = len(team_projects)

    for project in team_projects:
        if project["Risk Level"].lower() == "low" and project["Actual Finish Date"]:
            completed_projects += 1

    efficiency = (completed_projects / total_projects) * 100 if total_projects > 0 else 0
    return efficiency

# Function to save data to JSON
def save_to_json(data):
    timestamp = datetime.now().strftime('%Y%m%d-%I%M%p')
    filename = f'{timestamp}-project_data.json'
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return filename

# Function to save data to XLSX
def save_to_xlsx(data):
    timestamp = datetime.now().strftime('%Y%m%d-%I%M%p')
    filename = f'{timestamp}-project_efficiency.xlsx'
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Efficiency'])

    # Filter out rows with NaN values
    df = df.dropna()

    # Save data to XLSX
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Efficiency Data')
    return filename

data = []
teams = {}  # Dictionary to store teams and their associated projects
fake = Faker()  # Initialize the Faker instance

while True:
    project_name = input("Enter project name (or 'exit' to quit): ")
    if project_name.lower() == 'exit':
        break

    risk_level = input("Enter risk level (Low, High, Moderate): ")
    risk_comment = input("Enter risk comment: ")
    dependencies = input("Enter project dependencies (comma-separated): ")
    team = input("Enter testing team (group): ")

    # Collect additional data with validation
    expected_start_date = get_valid_date_input("Enter expected start date (YYYY-MM-DD): ")
    if not expected_start_date:
        break

    actual_start_date = get_valid_date_input("Enter actual start date (YYYY-MM-DD): ")
    if not actual_start_date:
        break

    expected_finish_date = get_valid_date_input("Enter expected finish date (YYYY-MM-DD): ")
    if not expected_finish_date:
        break

    actual_finish_date = get_valid_date_input("Enter actual finish date (YYYY-MM-DD): ")
    if not actual_finish_date:
        break

    project_data = {
        "Project Name": project_name,
        "Risk Level": risk_level,
        "Risk Comment": risk_comment,
        "Dependencies": dependencies,
        "Expected Start Date": expected_start_date,
        "Actual Start Date": actual_start_date,
        "Expected Finish Date": expected_finish_date,
        "Actual Finish Date": actual_finish_date,
    }

    # Add the project to the team's list of projects
    if team not in teams:
        teams[team] = []
    teams[team].append(project_data)

# Create a DataFrame from input data
df = pd.DataFrame(data)

# Calculate team efficiency for each team and store it in a dictionary
team_efficiency_data = {}
for team, team_projects in teams.items():
    efficiency = calculate_team_efficiency(team_projects)
    team_efficiency_data[team] = efficiency

# Display team efficiency
print("Team Efficiency:")
print("=" * 40)
for team, efficiency in team_efficiency_data.items():
    print(f"Team: {team}, Efficiency: {efficiency:.2f}%")

# Save data to JSON
json_filename = save_to_json(data)
print(f"Data saved to {json_filename}")

# Save data to XLSX
xlsx_filename = save_to_xlsx(team_efficiency_data)
print(f"Data saved to {xlsx_filename}")
