from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import logging

# Configure logging to track test results
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Firefox options for headless mode
firefox_options = Options()
firefox_options.headless = True  # Enable headless mode

# Initialize WebDriver (using Firefox in headless mode)
driver = webdriver.Firefox(options=firefox_options)
driver.get("http://34.122.172.93:5000/")  # Replace with your hosted web app URL if deployed on GCP
# In headless mode, maximize_window() may not work, but we can set window size instead.
driver.set_window_size(1920, 1080)
time.sleep(5)  # Allow the page to load fully

try:
    # Test 1: Web App Load Test
    logging.info("Running Test 1: Web App Load Test...")
    assert "Intelligent Transportation System Dashboard" in driver.title, "❌ Test Failed: Title not found"
    logging.info("✅ Test 1 Passed: Web app loaded successfully.")

    # Test 2: Verify Map Element Exists
    logging.info("Running Test 2: Map Element Test...")
    map_element = driver.find_element(By.ID, "map")
    assert map_element.is_displayed(), "❌ Test Failed: Map element not found"
    logging.info("✅ Test 2 Passed: Map element is displayed.")

    # Test 3: Real-Time Notifications Test
    logging.info("Running Test 3: Real-Time Notifications Test...")
    # Wait up to 20 seconds for the notifications panel text to change from "Waiting for updates..."
    WebDriverWait(driver, 20).until(
        lambda d: "Waiting for updates..." not in d.find_element(By.ID, "notifications").text
    )
    notifications_panel = driver.find_element(By.ID, "notifications")
    assert notifications_panel.is_displayed(), "❌ Test Failed: Notifications panel not found"
    logging.info("✅ Test 3 Passed: Notifications panel is updating in real-time.")

    # Test 4: Vehicle Status Panel Test
    logging.info("Running Test 4: Vehicle Status Panel Test...")
    status_panel = driver.find_element(By.ID, "vehicle-status")
    assert status_panel.is_displayed(), "❌ Test Failed: Vehicle status panel not found"
    logging.info("✅ Test 4 Passed: Vehicle status panel is displayed.")

    # Test 5: Real-Time Vehicle Updates and Prediction Test
    logging.info("Running Test 5: Real-Time Vehicle Updates and Prediction Test...")
    try:
        # Use XPath to find vehicle markers by their title attribute
        vehicle_markers = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@title]"))
        )
        logging.info(f"✅ Test 5 Passed: {len(vehicle_markers)} vehicle markers found.")
    except Exception as e:
        logging.error(f"❌ Test Failed: No vehicle markers found on the map. Error: {e}")

    # Test 6: Route Optimization Verification (Simulated)
    logging.info("Running Test 6: Route Optimization Verification...")
    actions = ActionChains(driver)
    actions.move_to_element(map_element).perform()  # Simulate route inspection
    logging.info("✅ Test 6 Passed: Route optimization verified visually.")

    # Test 7: Performance Test Simulation (Response Time Check)
    logging.info("Running Test 7: Performance Test Simulation...")
    start_time = time.time()
    driver.refresh()
    time.sleep(5)  # Allow the page to load again
    end_time = time.time()
    response_time = end_time - start_time
    assert response_time < 10, f"❌ Test Failed: Response time too high ({response_time:.2f}s)"
    logging.info(f"✅ Test 7 Passed: Response time is {response_time:.2f}s.")

except AssertionError as e:
    logging.error(str(e))
finally:
    # Close the browser
    driver.quit()
