import eventlet
eventlet.monkey_patch()  # Must be called before importing any other modules!

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import redis
import json
import os
import requests
import google.auth
from google.auth.transport.requests import Request
from google.cloud import firestore
from datetime import datetime
from multiprocessing import Process
import data_simulation  # Import your data simulation script

# Set up Firestore credentials
if os.environ.get("ENV") == "GCP":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/mohit_verma/service-account-file-new.json"
else:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ROG/Downloads/SST6826f/SST6826/service-account-file-new.json"

# Initialize Flask app, Firestore, and Redis
app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")
db = firestore.Client()

# Set up Redis for Pub/Sub
try:
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("✅ Redis connected successfully.")
except redis.ConnectionError:
    print("❌ Failed to connect to Redis.")
    redis_client = None

# Vertex AI Prediction endpoint
PROJECT_ID = "transportation-app-450511"
REGION = "us-central1"
ENDPOINT_ID = "8918680872123629568"
ENDPOINT = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict"

def get_access_token():
    """Retrieve an access token for authenticating with Vertex AI."""
    try:
        credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        print(f"❌ Failed to retrieve access token: {e}")
        return None

@app.route("/")
def index():
    """Render the main dashboard."""
    return render_template("index.html")

@app.route("/api/initial-data", methods=["GET"])
def get_initial_data():
    """Fetch the latest vehicle data from Redis and send it to the frontend."""
    if not redis_client:
        return jsonify({"error": "Redis not available"}), 500
    
    try:
        keys = list(redis_client.scan_iter("vehicle:*"))
        print(f"🔍 Found {len(keys)} keys in Redis.")  # Log how many keys were found
        
        vehicles = []
        for key in keys:
            vehicle_data = redis_client.get(key)
            if vehicle_data:
                print(f"🔍 Key: {key} | Data: {vehicle_data[:100]}...")  # Print first 100 characters for review
                vehicles.append(json.loads(vehicle_data))
            else:
                print(f"⚠️ Skipping empty or corrupted data for key: {key}")

        
        if not vehicles:
            print("⚠️ No vehicle data found in Redis.")  # Log when no vehicles are found
            return jsonify({"message": "No vehicle data available"}), 200
        
        return jsonify(vehicles)
    
    except Exception as e:
        print(f"❌ Error fetching initial data from Redis: {e}")  # Log any exception
        return jsonify({"error": "Failed to fetch initial data"}), 500

@app.route("/api/predict", methods=["POST"])
def predict():
    """Make a prediction using the Vertex AI model."""
    data = request.get_json()
    access_token = get_access_token()

    if not access_token:
        return jsonify({"error": "Failed to retrieve access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "instances": [[data["lat"], data["lng"], data["speed"], 0, 0]]  # Match the required input format for prediction
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        prediction = result.get("predictions", [0])[0]
        return jsonify({"prediction": prediction})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def redis_listener():
    """Listen to Redis channel, store the latest vehicle data, and emit updates via WebSocket."""
    if not redis_client:
        print("❌ Redis is not available for listening.")
        return

    pubsub = redis_client.pubsub()
    pubsub.subscribe("vehicle_updates")

    for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])
                vehicle_id = data["id"]
                redis_client.set(f"vehicle:{vehicle_id}", json.dumps(data))
                socketio.emit("vehicle_update", [data])
            except Exception as e:
                print(f"❌ Error processing message: {e}")

def start_data_simulation():
    """Start the data simulation as a separate process."""
    data_simulation.run_simulation()  # Ensure `run_simulation` is the main method in your data simulation script.

if __name__ == "__main__":
    simulation_process = Process(target=start_data_simulation)
    simulation_process.start()

    socketio.start_background_task(redis_listener)
    socketio.run(app, host="0.0.0.0", port=5000)
    simulation_process.join()
