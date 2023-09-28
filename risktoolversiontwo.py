from colorama import Fore
import pandas as pd

# Function to calculate the risk level based on input factors
def calculate_risk(scenario_steps, systems, microservices, expected_execution_time):
    # Calculate the risk based on your criteria (customize this part)
    # Here, we use a simple calculation for demonstration purposes
    risk_score = len(scenario_steps) + len(systems) + len(microservices) + expected_execution_time
    return risk_score

# Function to assign a color code based on the risk level
def assign_color(risk_score):
    if risk_score <= 10:
        return Fore.GREEN + "Low"
    elif risk_score <= 20:
        return Fore.YELLOW + "Moderate"
    else:
        return Fore.RED + "High"

# Function to get user input
def get_user_input():
    print("Project Assessment")
    print("===================")

    scenario_name = input("Scenario Name: ")
    scenario_steps = input("Scenario Steps (comma-separated): ").split(',')
    systems = input("Systems List Involved (comma-separated): ").split(',')
    example_order_id = input("Example Order ID Items Related: ")
    example_product_id = input("Example Product ID Related: ")
    microservices = input("Microservices Related (comma-separated): ").split(',')
    payment_document_ids = input("Payment Document ID Related (comma-separated): ").split(',')
    created_date = input("Created Date (YYYY-MM-DD): ")
    updated_date = input("Updated Date (YYYY-MM-DD): ")
    finished_date = input("Finished Date (YYYY-MM-DD): ")
    expected_execution_time = int(input("Expected Execution Time (hours): "))

    return {
        "Scenario Name": scenario_name,
        "Scenario Steps": scenario_steps,
        "Systems": systems,
        "Example Order ID": example_order_id,
        "Example Product ID": example_product_id,
        "Microservices": microservices,
        "Payment Document IDs": payment_document_ids,
        "Created Date": created_date,
        "Updated Date": updated_date,
        "Finished Date": finished_date,
        "Expected Execution Time": expected_execution_time,
    }

# Main program
if __name__ == "__main__":
    user_input = get_user_input()
    risk_score = calculate_risk(
        user_input["Scenario Steps"],
        user_input["Systems"],
        user_input["Microservices"],
        user_input["Expected Execution Time"]
    )
    risk_color = assign_color(risk_score)

    # Display risk assessment
    print("\nRisk Assessment")
    print("================")
    print(f"Scenario Name: {user_input['Scenario Name']}")
    print(f"Risk Level: {risk_color} ({risk_score})")
