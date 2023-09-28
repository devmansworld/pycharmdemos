import pandas as pd
from colorama import Fore

# Sample data (replace with your actual data)
data = {
    "Project Name": ["Project A", "Project B", "Project C"],
    "Microservices Involved": [["Service1", "Service2"], ["Service3"], ["Service4"]],
    "Team Name": ["Team X", "Team Y", "Team Z"],
    "Team Lead": ["Lead X", "Lead Y", "Lead Z"],
    "Tasks": ["Task 1, Task 2", "Task 3", "Task 4"],
    "Scenario Steps": [["Step 1", "Step 2"], ["Step 3"], ["Step 4"]],
    "Software Delivery Date": ["2023-01-15", "2023-02-10", "2023-03-05"],
    "Start Testing Date": ["2023-01-20", "2023-02-15", "2023-03-10"],
    "End Testing Date": ["2023-01-25", "2023-02-20", "2023-03-15"],
    "Expected Testing Time (hours)": [20, 15, 25],
    "Real Testing Time (hours)": [18, 16, 28],
    "Test Status": ["Completed", "In Progress", "Not Started"],
}

df = pd.DataFrame(data)

# Function to calculate risk and provide a comment
def calculate_risk(row):
    # Customize risk calculation logic here (based on your criteria)
    expected_time = row["Expected Testing Time (hours)"]
    real_time = row["Real Testing Time (hours)"]
    if real_time > expected_time:
        risk_level = "High"
        comment = "Testing took longer than expected."
    else:
        risk_level = "Low"
        comment = "Testing completed within the expected time."

    return risk_level, comment

# Apply risk calculation to each row
df["Risk Level"], df["Risk Comment"] = zip(*df.apply(calculate_risk, axis=1))

# Display the project data with risk assessment
print("Project Data with Risk Assessment")
print("=" * 35)
print(df)

# Display projects with color-coded risk levels
print("\nProjects by Risk Level")
print("=" * 25)

for index, row in df.iterrows():
    project_name = row["Project Name"]
    risk_level = row["Risk Level"]

    if risk_level == "Low":
        risk_color = Fore.GREEN + risk_level
    elif risk_level == "High":
        risk_color = Fore.RED + risk_level
    else:
        risk_color = Fore.YELLOW + risk_level

    print(f"Project: {project_name} | Risk Level: {risk_color}")

# Reset text color
print(Fore.RESET)
