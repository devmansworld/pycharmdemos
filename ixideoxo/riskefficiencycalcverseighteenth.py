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
        while True:
            risk_level = fake.random_element(elements=('Low', 'High', 'Moderate')).lower()
            if risk_level in ('low', 'high', 'moderate'):
                break
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

# Generate fake data
num_fake_projects = int(input("Enter the number of fake projects to generate: "))
fake_data = generate_fake_data(num_fake_projects)
data = fake_data  # Initialize data with fake data

# Rest of your code remains the same from here...
