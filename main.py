import pyautogui
import math
import time

# Set the radius of the circle and the number of steps
radius = 100  # You can adjust this value
num_steps = 360  # 360 degrees for a full circle

# Calculate the step size to move in a circle
step_size = (2 * math.pi * radius) / num_steps

# Center of the circle (you can adjust these coordinates)
center_x, center_y = 500, 500  # Adjust as needed

# Slow down the mouse movement by adding a delay between steps
delay_between_steps = 0.1  # Adjust as needed

# Move the mouse in a clockwise circle
for i in range(num_steps):
    angle = i * step_size
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    # Move the mouse to the calculated coordinates with a duration of 0.1 seconds (adjust as needed)
    pyautogui.moveTo(x, y, duration=0.1)

    # Add a delay between steps to control the speed (adjust as needed)
    time.sleep(delay_between_steps)

    # Print a message for each step performed
    print(f"Step {i + 1}: Moved to ({x}, {y})")

# Move the mouse back to the original position (optional)
pyautogui.moveTo(center_x, center_y, duration=0.1)
print("Mouse movement completed.")
