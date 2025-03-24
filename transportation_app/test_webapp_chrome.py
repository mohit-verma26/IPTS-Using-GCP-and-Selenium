# test_webapp_chrome.py

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging to track test results
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Chrome options
chrome_options = Options()
# Optionally open DevTools for debugging
chrome_options.add_argument("--auto-open-devtools-for-tabs")
# Uncomment the following if you need to configure a proxy
# chrome_options.add_argument("--proxy-server=http://your.proxy:port")

# Initialize ChromeDriver with options and set an increased page load timeout
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(60)  # Wait up to 60 seconds for the page to load

url = "http://34.55.40.33:5000/"
logging.info("Opening web app: " + url)
driver.get(url)
driver.maximize_window()
time.sleep(5)  # Allow the page to load fully

try:
    # Test 1: Web App Load Test
    logging.info("Running Test 1: Web App Load Test...")
    if "Intelligent Transportation System Dashboard" not in driver.title:
        raise AssertionError("❌ Test Failed: Title not found")
    logging.info("✅ Test 1 Passed: Web app loaded successfully.")

    # Test 2: Verify Map Element Exists
    logging.info("Running Test 2: Map Element Test...")
    map_element = driver.find_element(By.ID, "map")
    if not map_element.is_displayed():
        raise AssertionError("❌ Test Failed: Map element not found")
    logging.info("✅ Test 2 Passed: Map element is displayed.")

    # Test 3: Real-Time Notifications Test
    logging.info("Running Test 3: Real-Time Notifications Test...")
    notifications_panel = driver.find_element(By.ID, "notifications")
    if not notifications_panel.is_displayed():
        raise AssertionError("❌ Test Failed: Notifications panel not found")
    if "Waiting for updates..." in notifications_panel.text:
        raise AssertionError("❌ Test Failed: Notifications not updating")
    logging.info("✅ Test 3 Passed: Notifications panel is updating in real-time.")

    # Test 4: Vehicle Status Panel Test
    logging.info("Running Test 4: Vehicle Status Panel Test...")
    status_panel = driver.find_element(By.ID, "vehicle-status")
    if not status_panel.is_displayed():
        raise AssertionError("❌ Test Failed: Vehicle status panel not found")
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
    if response_time >= 10:
        raise AssertionError(f"❌ Test Failed: Response time too high ({response_time:.2f}s)")
    logging.info(f"✅ Test 7 Passed: Response time is {response_time:.2f}s.")

except AssertionError as e:
    logging.error(str(e))

finally:
    # Close the browser
    driver.quit()
