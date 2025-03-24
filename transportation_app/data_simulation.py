import redis
import json
from datetime import datetime
import random
import time
import math

# Initialize Redis client
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

# Sample initial data for 10 vehicles with predefined destinations
vehicles = [
    {"id": 1, "lat": 51.5074, "lng": -0.1278, "status": "on-time", "speed": 60, "type": "car", "destination": [51.5200, -0.1400]},
    {"id": 2, "lat": 51.5075, "lng": -0.1279, "status": "delayed", "speed": 40, "type": "bus", "destination": [51.5150, -0.1500]},
    {"id": 3, "lat": 51.5080, "lng": -0.1285, "status": "on-time", "speed": 50, "type": "train", "destination": [51.5300, -0.1100]},
    {"id": 4, "lat": 51.5090, "lng": -0.1290, "status": "on-time", "speed": 80, "type": "car", "destination": [51.5250, -0.1250]},
    {"id": 5, "lat": 51.5100, "lng": -0.1300, "status": "delayed", "speed": 70, "type": "bus", "destination": [51.5250, -0.1350]},
    {"id": 6, "lat": 51.5110, "lng": -0.1310, "status": "on-time", "speed": 90, "type": "train", "destination": [51.5300, -0.1400]},
    {"id": 7, "lat": 51.5120, "lng": -0.1320, "status": "on-time", "speed": 55, "type": "car", "destination": [51.5220, -0.1200]},
    {"id": 8, "lat": 51.5130, "lng": -0.1330, "status": "delayed", "speed": 45, "type": "bus", "destination": [51.5180, -0.1450]},
    {"id": 9, "lat": 51.5140, "lng": -0.1340, "status": "on-time", "speed": 65, "type": "train", "destination": [51.5280, -0.1250]},
    {"id": 10, "lat": 51.5150, "lng": -0.1350, "status": "on-time", "speed": 75, "type": "car", "destination": [51.5230, -0.1300]}
]

LAT_MIN, LAT_MAX = 51.4700, 51.5300
LNG_MIN, LNG_MAX = -0.1500, -0.1000

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km

def adjust_route(vehicle):
    """Adjust the route to simulate real-time optimization."""
    dest_lat, dest_lng = vehicle["destination"]
    distance_to_dest = haversine(vehicle["lat"], vehicle["lng"], dest_lat, dest_lng)
    
    if distance_to_dest > 0.5:  # If distance to destination is more than 0.5 km, adjust towards the destination
        vehicle["lat"] += (dest_lat - vehicle["lat"]) * 0.1  # Move 10% closer to the destination
        vehicle["lng"] += (dest_lng - vehicle["lng"]) * 0.1
    else:
        # If close to destination, assign a new random destination
        vehicle["destination"] = [random.uniform(LAT_MIN, LAT_MAX), random.uniform(LNG_MIN, LNG_MAX)]
        print(f"🚀 Vehicle {vehicle['id']} reached its destination. New destination set: {vehicle['destination']}")

def simulate_vehicle_movement(vehicle):
    """Simulate vehicle movement, adjust routes, and publish updates to Redis."""
    traffic_condition = random.choice(["light", "moderate", "heavy"])
    
    if traffic_condition == "light":
        move_factor = random.uniform(0.0001, 0.0002)
    elif traffic_condition == "moderate":
        move_factor = random.uniform(0.00005, 0.0001)
    else:
        move_factor = random.uniform(0.00001, 0.00005)

    vehicle["lat"] += random.uniform(-move_factor, move_factor)
    vehicle["lng"] += random.uniform(-move_factor, move_factor)
    
    vehicle["lat"] = min(max(vehicle["lat"], LAT_MIN), LAT_MAX)
    vehicle["lng"] = min(max(vehicle["lng"], LNG_MIN), LNG_MAX)
    
    if random.random() < 0.3:
        vehicle["status"] = "delayed" if vehicle["status"] == "on-time" else "on-time"
    
    adjust_route(vehicle)
    
    vehicle["timestamp"] = datetime.now().isoformat()
    
    redis_client.publish("vehicle_updates", json.dumps(vehicle))
    #print(f"📡 Published optimized update for vehicle {vehicle['id']}: {vehicle}")

def run_simulation():
    """Continuously simulate and publish optimized vehicle updates."""
    print("🚀 Starting vehicle data simulation with route optimization...")
    while True:
        for vehicle in vehicles:
            simulate_vehicle_movement(vehicle)
        time.sleep(5)  # 5 seconds between each update cycle

if __name__ == "__main__":
    run_simulation()
