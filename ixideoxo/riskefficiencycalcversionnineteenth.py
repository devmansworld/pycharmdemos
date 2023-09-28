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
            print("Invalid date format. Please use YYYY-MM-DD format or 'exit' to quit. Please try again.")

# Function to parse and validate risk levels
def get_valid_risk_level(prompt):
    while True:
        risk_level = input(prompt)
        if risk_level.lower() in ('low', 'high', 'moderate'):
            return risk_level.lower()
        else:
            print("Invalid risk level. Please enter 'Low', 'High', or 'Moderate'. Please try again.")

# Function to generate fake data using Faker
def generate_fake_data(num_projects):
    fake = Faker()
    fake_data = []
    for _ in range(num_projects):
        project_name = fake.company()
        risk_level = fake.random_element(elements=('Low', 'High', 'Moderate'))
        risk_comment = fake.sentence()
        dependencies = ', '.join(fake.words(nb=3))
        team = fake.job()
        expected_start_date = fake.date_between(start_date='-1y', end_date='today')
        actual_start_date = fake.date_between(start_date=expected_start_date, end_date='today')
        expected_finish_date = fake.date_between(start_date=actual_start_date, end_date='+1y')
        actual_finish_date = fake.date_between(start_date=actual_start_date, end_date=expected_finish_date)
        fake_data.append({
            "Project Name": project_name,
            "Risk Level": risk_level,
            "Risk Comment": risk_comment,
            "Dependencies": dependencies,
            "Team": team,
            "Expected Start Date": expected_start_date.strftime('%Y-%m-%d'),
            "Actual Start Date": actual_start_date.strftime('%Y-%m-%d'),
            "Expected Finish Date": expected_finish_date.strftime('%Y-%m-%d'),
            "Actual Finish Date": actual_finish_date.strftime('%Y-%m-%d'),
        })
    return fake_data

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

# Function to display data
def display_data(data):
    print("\nEntered Data:")
    print("=" * 80)
    for item in data:
        print(f"Project Name: {item['Project Name']}")
        print(f"Risk Level: {item['Risk Level']}")
        print(f"Risk Comment: {item['Risk Comment']}")
        print(f"Dependencies: {item['Dependencies']}")
        print(f"Team: {item['Team']}")
        print(f"Expected Start Date: {item['Expected Start Date']}")
        print(f"Actual Start Date: {item['Actual Start Date']}")
        print(f"Expected Finish Date: {item['Expected Finish Date']}")
        print(f"Actual Finish Date: {item['Actual Finish Date']}")
        print("=" * 80)

data = []
while True:
    project_name = input("Enter project name (or 'exit' to quit): ")
    if project_name.lower() == 'exit':
        break

    risk_level = get_valid_risk_level("Enter risk level (Low, High, Moderate): ")
    risk_comment = input("Enter risk comment: ")
    dependencies = input("Enter project dependencies (comma-separated): ")
    team = input("Enter testing team: ")

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
json_filename = save_to_json(data)
print(f"Data saved to {json_filename}")

# Save data to XLSX
xlsx_filename = save_to_xlsx(team_efficiency)
print(f"Data saved to {xlsx_filename}")

# Display entered data
display_data(data)

# Ask the user if they want to generate mock data
# Ask the user if they want to generate fake data
generate_fake = input("Do you want to generate fake data? (yes/no): ").lower()
if generate_fake == 'yes':
    num_fake_projects = int(input("Enter the number of fake projects to generate: "))
    fake_data = generate_fake_data(num_fake_projects)
    data.extend(fake_data)

# Rest of the code remains the same

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
json_filename = save_to_json(data)
print(f"Data saved to {json_filename}")

# Save data to XLSX
xlsx_filename = save_to_xlsx(team_efficiency)
print(f"Data saved to {xlsx_filename}")

# Display entered data
display_data(data)
