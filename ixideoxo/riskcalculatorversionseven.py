import pandas as pd
import json
from datetime import datetime
from faker import Faker
import os

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

# Function to load data from JSON files in a folder
def load_data_from_json_folder(folder_path):
    json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
    loaded_data = []

    for file in json_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            loaded_data.extend(data)

    return loaded_data

data = []
teams = {}  # Dictionary to store teams and their associated projects
fake = Faker()  # Initialize the Faker instance

# Ask the user if they want to generate test data
generate_test_data = input("Do you want to generate test data? (yes/no): ")
if generate_test_data.lower() == 'yes':
    num_projects = int(input("Enter the number of projects to generate: "))
    test_data = []

    for _ in range(num_projects):
        project_name = fake.word()
        risk_level = fake.random_element(elements=("Low", "High", "Moderate"))
        risk_comment = fake.text(max_nb_chars=100)
        dependencies = fake.words(nb=5)
        team = fake.company()
        expected_start_date = fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d')
        actual_start_date = fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d')
        expected_finish_date = fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d')
        actual_finish_date = fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d')

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
        }

        test_data.append(project_data)

    data.extend(test_data)  # Add generated test data to the existing data
else:
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
            "Team": team,
            "Expected Start Date": expected_start_date,
            "Actual Start Date": actual_start_date,
            "Expected Finish Date": expected_finish_date,
            "Actual Finish Date": actual_finish_date,
        }

        # Add the project to the team's list of projects
        if team not in teams:
            teams[team] = []
        teams[team].append(project_data)

# Load data from JSON files in a folder (modify the folder path accordingly)
folder_path = "/path/to/your/json/files"
loaded_data = load_data_from_json_folder(folder_path)
data.extend(loaded_data)  # Add loaded data to the existing data

# Create a DataFrame from input data
df = pd.DataFrame(data)

# Calculate team efficiency for each team and store it in a dictionary
team_efficiency_data = {}
for team, team_projects in teams.items():
    efficiency = calculate_team_efficiency(team_projects)
    team_efficiency_data[team] = efficiency

# Calculate team efficiency for the entire dataset
team_efficiency = calculate_team_efficiency(df)

# Display team efficiency
print("Team Efficiency:")
print("=" * 40)
for team, efficiency in team_efficiency.items():
    print(f"Team: {team}, Efficiency: {efficiency:.2f}%")

# Display entered data
print("Entered Data:")
print("=" * 40)
for item in data:
    modified_item = {key: value.replace('{', '|').replace('}', '|').replace("'", "|") for key, value in item.items()}
    print(modified_item)

# Save data to JSON
json_filename = save_to_json(data)
print(f"Data saved to {json_filename}")

# Save data to XLSX
xlsx_filename = save_to_xlsx(team_efficiency_data)
print(f"Data saved to {xlsx_filename}")
