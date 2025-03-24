import os
import sys
import logging
from locust import HttpUser, TaskSet, task, between

# Configure logging to export results to a log file
logging.basicConfig(
    filename="locust_test_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# Add pywin32_system32 to the PATH if not already there
if r"C:\Users\Face\Documents\WorkStuff\SST6826\env\Lib\site-packages\pywin32_system32" not in os.environ["PATH"]:
    os.environ["PATH"] += r";C:\Users\Face\Documents\WorkStuff\SST6826\env\Lib\site-packages\pywin32_system32"


class UserBehavior(TaskSet):
    @task(1)
    def load_homepage(self):
        """Simulate a user loading the main dashboard."""
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200 and "Intelligent Transportation System Dashboard" in response.text:
                response.success()
                logging.info("✅ Homepage loaded successfully.")
                print("✅ Homepage loaded successfully.")
            else:
                response.failure(f"❌ Homepage failed! Status code: {response.status_code}")
                logging.error(f"❌ Homepage failed! Status code: {response.status_code}")

    @task(2)
    def load_initial_data(self):
        """Simulate a user requesting initial vehicle data."""
        with self.client.get("/api/initial-data", timeout=10, catch_response=True) as response:
            if response.status_code == 200 and ("vehicle_id" in response.text or "id" in response.text):
                response.success()
                logging.info("✅ Initial data request successful.")
                print("✅ Initial data request successful.")
            else:
                logging.error(f"❌ Initial data request failed! Status code: {response.status_code}, Response: {response.text}")
                response.failure(f"❌ Initial data request failed! Status code: {response.status_code}")

    @task(1)
    def predict_vehicle_status(self):
        """Simulate a user sending a prediction request."""
        payload = {
            "lat": 51.5074,
            "lng": -0.1278,
            "speed": 50,
            "type": "car"
        }
        with self.client.post("/api/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200 and "prediction" in response.json():
                prediction = response.json().get("prediction", "N/A")
                response.success()
                logging.info(f"✅ Prediction request successful. Prediction: {prediction}")
                print(f"✅ Prediction request successful. Prediction: {prediction}")
            else:
                response.failure(f"❌ Prediction request failed! Status code: {response.status_code}")
                logging.error(f"❌ Prediction request failed! Status code: {response.status_code}")


class WebsiteUser(HttpUser):
    """Configure the user behavior and wait time between tasks."""
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Simulate user wait time between 1 to 5 seconds
