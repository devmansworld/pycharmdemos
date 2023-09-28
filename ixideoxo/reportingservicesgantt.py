import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Sample data (replace with your actual data)
data = {
    "Service Name": ["Service A", "Service B", "Service C"],
    "Service ID": [1, 2, 3],
    "Backend Microservices": [["Microservice1", "Microservice2"], ["Microservice3"], ["Microservice4"]],
    "Team Lead": ["Team Lead 1", "Team Lead 2", "Team Lead 3"],
    "Project ID": [101, 102, 103],
    "Status": ["In Progress", "Completed", "Not Started"]
}

df = pd.DataFrame(data)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Convert project IDs to numeric values for plotting
df["Project ID"] = pd.to_numeric(df["Project ID"], errors="coerce")
df = df.dropna(subset=["Project ID"])

# Create Gantt chart
for index, row in df.iterrows():
    start_date = index
    end_date = index + 1
    ax.barh(row["Service Name"], width=1, left=start_date, color=np.random.rand(3,))
    ax.text(start_date + 0.1, row["Service Name"], f"Project {int(row['Project ID'])}", va="center")

# Customize chart appearance
ax.set_xlabel("Timeline")
ax.set_ylabel("Middleware Service")
ax.set_title("Middleware Service Gantt Chart")
ax.invert_yaxis()  # Invert the y-axis to display services from top to bottom
ax.set_xlim(0, len(df) + 1)  # Adjust x-axis limits

# Display the Gantt chart
plt.show()
