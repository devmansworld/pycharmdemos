

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the directory containing the Microsoft Edge WebDriver executable
webdriver_dir = os.path.expanduser("~")  # Use the user's home directory

# Add the WebDriver directory to the PATH environment variable
os.environ["PATH"] += os.pathsep + webdriver_dir

# Initialize the Edge WebDriver (without specifying executable_path)
driver = webdriver.Edge()

# Open the convenience store website
driver.get('https://www.homedepot.com.mx')

print("Opened website")

# Perform the shopping cart operations
products = ['pan', 'pen', 'apple']

# Search for items
for product in products:
    search_input = driver.find_element(By.ID, 'SimpleSearchForm_SearchTerm')
    search_input.clear()
    search_input.send_keys(product)
    search_input.send_keys(Keys.RETURN)

    try:
        # Wait for the 'btn1' element to be present for a maximum of 5 seconds
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn1'))
        )

        # Perform actions on the element once it's found (e.g., click)
        element.click()

        # Wait for 4 seconds (you can adjust the duration)
        time.sleep(4)

    except Exception as e:
        # Handle any exceptions (e.g., element not found, timeout)
        print(f"An error occurred: {str(e)}")

# Navigate to the cart page
#cart_link = driver.find_element(By.ID, 'link-cart')
#cart_link.click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
goto_cart_button = driver.find_element(By.ID, 'GotoCartButton2')
goto_cart_button.click()
# Wait for 3 seconds (you can adjust the duration)
time.sleep(3)

# Parse the cart page using BeautifulSoup
cart_page_html = driver.page_source
soup = BeautifulSoup(cart_page_html, 'html.parser')

# Find and extract the total value
total_element = soup.find('span', {'class': 'summary__text-value summary__text-value--price'})
cart_total = total_element.text.strip()
time.sleep(50)
# Print the cart total
print(f"Cart Total: {cart_total}")

# Continue with checkout and other steps as needed
time.sleep(50)
# Close the browser
driver.quit()




# ... Other imports ...
from bs4 import BeautifulSoup


# Define a new step to scroll down to the bottom of the page and click an element
@when('Cuando hago clic en el botón "Ir al carrito"')
def step_when_click_goto_cart_button(context):
    # Scroll down to the bottom of the page using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for a moment (you can adjust the duration)
    time.sleep(2)

    # Click on the element with ID "GotoCartButton2"
    goto_cart_button = driver.find_element(By.ID, 'GotoCartButton2')
    goto_cart_button.click()

# Add a new step to verify the cart total
@then('Entonces debería ver el total del carrito')
def step_then_see_cart_total(context):
    # Debugging print to ensure the step is reached
    print("Verifying cart total")

    # Parse the cart page using BeautifulSoup
    cart_page_html = driver.page_source
    soup = BeautifulSoup(cart_page_html, 'html.parser')

    # Find and extract the total value
    total_element = soup.find('span', {'class': 'summary__text-value summary__text-value--price'})

    if total_element:
        cart_total = total_element.text.strip()
        print(f"Cart Total: {cart_total}")
    else:
        print("Total element not found!")

# ... Other step definitions ...

if __name__ == '__main__':
    # Execute the Cucumber scenario using Behave
    behave_cmdline_args = ['behave', 'path/to/home_cart_test.feature']
    behave.main(behave_cmdline_args)
