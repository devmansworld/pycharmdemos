import pandas as pd
import json
from datetime import datetime
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

# Function to generate an Excel template
def generate_excel_template():
    template_data = {
        "Project Name": [],
        "Risk Level": [],
        "Risk Comment": [],
        "Dependencies": [],
        "Team": [],
        "Expected Start Date": [],
        "Actual Start Date": [],
        "Expected Finish Date": [],
        "Actual Finish Date": []
    }

    df = pd.DataFrame(template_data)
    template_filename = 'project_data_template.xlsx'
    df.to_excel(template_filename, index=False)
    print(f"Excel template '{template_filename}' generated. Please fill in the data in the Excel file.")

# Ask the user whether to enter data manually or use an Excel template
while True:
    choice = input("Choose an option:\n1. Enter data manually\n2. Use Excel template\n3. Exit\nEnter the option number: ")

    if choice == '1':
        data = []
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
        break
    elif choice == '2':
        generate_excel_template()
        break
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter a valid option (1, 2, or 3).")

