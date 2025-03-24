from google.cloud import firestore
import os

# Set up Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ROG/Downloads/SST6826f/SST6826/service-account-file-new.json"

# Initialize Firestore client
db = firestore.Client()

def insert_vehicle_data(vehicle):
    """Insert real-time vehicle data into Firestore."""
    print(f"🔄 Attempting to insert/update vehicle {vehicle['id']}...")
    doc_ref = db.collection("vehicle_data").document(str(vehicle["id"]))
    doc_ref.set({
        "vehicle_id": vehicle["id"],
        "type": vehicle["type"],
        "lat": vehicle["lat"],
        "lng": vehicle["lng"],
        "speed": vehicle["speed"],
        "status": vehicle["status"],
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print(f"✅ Successfully inserted/updated vehicle {vehicle['id']}.")

def update_vehicle_data(vehicle):
    """Update existing vehicle data in Firestore with real-time changes."""
    print(f"🔄 Attempting to update vehicle {vehicle['id']}...")
    doc_ref = db.collection("vehicle_data").document(str(vehicle["id"]))
    try:
        doc_ref.update({
            "lat": vehicle["lat"],
            "lng": vehicle["lng"],
            "status": vehicle["status"],
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"✅ Successfully updated vehicle {vehicle['id']}.")
    except Exception as e:
        print(f"❌ Failed to update vehicle {vehicle['id']}. Error: {e}")

def get_vehicle_history():
    """Retrieve historical data for all vehicles from Firestore."""
    print("🔍 Fetching vehicle history...")
    vehicle_ref = db.collection("vehicle_data").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    history = []
    for doc in vehicle_ref:
        vehicle = doc.to_dict()
        vehicle["id"] = doc.id  # Add document ID to the data
        print(f"📋 Retrieved vehicle {vehicle['id']}: {vehicle}")
        history.append(vehicle)
    print(f"✅ Fetched {len(history)} vehicles from Firestore.")
    return history

def get_vehicle_by_id(vehicle_id):
    """Retrieve specific vehicle data by its ID."""
    print(f"🔍 Looking up vehicle {vehicle_id}...")
    doc_ref = db.collection("vehicle_data").document(str(vehicle_id)).get()
    if doc_ref.exists:
        vehicle = doc_ref.to_dict()
        vehicle["id"] = doc_ref.id
        print(f"✅ Vehicle found: {vehicle}")
        return vehicle
    else:
        print(f"❌ Vehicle with ID {vehicle_id} not found.")
        return None

def delete_vehicle_data(vehicle_id):
    """Delete specific vehicle data by its ID from Firestore."""
    print(f"🗑️ Attempting to delete vehicle {vehicle_id}...")
    db.collection("vehicle_data").document(str(vehicle_id)).delete()
    print(f"✅ Vehicle {vehicle_id} deleted from Firestore.")
