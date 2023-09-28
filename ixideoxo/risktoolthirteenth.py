import pandas as pd
import json
from datetime import datetime
from faker import Faker
import plotly.express as px

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

# Function to display data in an ASCII table
def display_data(data):
    print("\nEntered Data:")
    print("=" * 97)  # Updated the width to match the headers
    print("{:<20} {:<12} {:<12} {:<25} {:<20} {:<15} {:<15} {:<15}".format(
        "Project Name", "Risk Level", "Risk Comment", "Dependencies", "Team",
        "Exp. Start Date", "Act. Start Date", "Exp. Finish Date"
    ))
    print("=" * 97)  # Updated the width to match the headers
    for item in data:
        print("{:<20} {:<12} {:<12} {:<25} {:<20} {:<15} {:<15} {:<15}".format(
            item["Project Name"], item["Risk Level"], item["Risk Comment"],
            item["Dependencies"], item["Team"], item["Expected Start Date"],
            item["Actual Start Date"], item["Expected Finish Date"]
        ))
    print("=" * 97)  # Updated the width to match the headers

data = []
fake = Faker()  # Initialize the Faker instance

# Ask the user if they want to generate test data
generate_test_data = input("Do you want to generate test data? (yes/no): ")
if generate_test_data.lower() == 'yes':
    num_projects = int(input("Enter the number of projects to generate: "))
    test_data = []

    for _ in range(num_projects):
        test_data.append({
            "Project Name": fake.word(),
            "Risk Level": fake.random_element(elements=("Low", "High", "Moderate")),
            "Risk Comment": fake.text(max_nb_chars=100),
            "Dependencies": fake.words(nb=5),
            "Team": fake.company(),
            "Expected Start Date": fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
            "Actual Start Date": fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
            "Expected Finish Date": fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            "Actual Finish Date": fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
        })

    data.extend(test_data)  # Add generated test data to the existing data
else:
    while True:
        project_name = input("Enter project name (or 'exit' to quit): ")
        if project_name.lower() == 'exit':
            break

        risk_level = input("Enter risk level (Low, High, Moderate): ")
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

# Display data in an ASCII table
display_data(data)

# Display team efficiency
print("\nTeam Efficiency:")
print("=" * 40)
for team, efficiency in team_efficiency.items():
    print(f"Team: {team}, Efficiency: {efficiency:.2f}%")

# Save data to JSON
json_filename = save_to_json(data)
print(f"\nData saved to {json_filename}")

# Save data to XLSX
xlsx_filename = save_to_xlsx(team_efficiency)
print(f"Data saved to {xlsx_filename}")

# Create a Gantt chart
fig = px.timeline(df, x_start="Expected Start Date", x_end="Expected Finish Date", y="Project Name", title="Project Timeline")
fig.update_yaxes(categoryorder="total ascending")
fig.update_xaxes(title="Timeline")
fig.update_yaxes(title="Project Name")
fig.show()
