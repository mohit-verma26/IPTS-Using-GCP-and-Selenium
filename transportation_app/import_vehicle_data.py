import requests
import json

# Define the Bearer token
BEARER_TOKEN = "ya29.a0AXeO80SjYO2S48fdPrfB4RrEy6kW4BNPnFJMl8iYiTL0OkknJxeEM5XtIhKHIV6iU9ACAN8HuYrkM6xZ-oPEXxIOT6cO-uwTzBIj0-voyYxw38dq4IcfLqFI8_QDBP7MkFsBQs0QX9gnV7x1WLz2qgVXFVvzoVawYnwkmnlnQPLeYgaCgYKAUoSARASFQHGX2MiVmhlRrYJ47w4UBGlmCDjxA0181"  # Replace with your actual token

# Define the base Firestore URL
FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/transportation-app-450511/databases/(default)/documents/vehicle_data/"

def load_vehicle_data(file_path):
    """Load vehicle data from the JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: Failed to parse '{file_path}'. Ensure it's a valid JSON file.")
        return []

def insert_vehicle_data(vehicle_data):
    """Insert each vehicle entry into Firestore."""
    for vehicle in vehicle_data:
        url = FIRESTORE_URL + str(vehicle["vehicle_id"])
        payload = {
            "fields": {
                "vehicle_id": {"integerValue": vehicle["vehicle_id"]},
                "type": {"stringValue": vehicle["type"]},
                "lat": {"doubleValue": vehicle["lat"]},
                "lng": {"doubleValue": vehicle["lng"]},
                "speed": {"integerValue": vehicle["speed"]},
                "status": {"stringValue": vehicle["status"]}
            }
        }
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"✅ Vehicle {vehicle['vehicle_id']} added successfully.")
        else:
            print(f"❌ Failed to add Vehicle {vehicle['vehicle_id']}. Status Code: {response.status_code}, Response: {response.text}")

# Main Execution
vehicle_data = load_vehicle_data("vehicle_data.json")
if vehicle_data:
    insert_vehicle_data(vehicle_data)
