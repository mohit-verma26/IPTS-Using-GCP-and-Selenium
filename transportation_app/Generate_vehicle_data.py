import csv
import random
from datetime import datetime, timedelta

# Function to generate random GPS coordinates within a given bounding box
def generate_random_coordinates():
    # Coordinates roughly around London
    lat = random.uniform(51.4700, 51.5300)
    lng = random.uniform(-0.1500, -0.1000)
    return lat, lng

# Function to generate a realistic status ("on-time" or "delayed")
def generate_status():
    return "on-time" if random.random() > 0.3 else "delayed"

# Function to generate random speed between 20 and 120 km/h
def generate_speed():
    return random.randint(20, 120)

# Function to generate a timestamp within the past 30 days
def generate_timestamp():
    start_date = datetime.now() - timedelta(days=30)
    random_date = start_date + timedelta(seconds=random.randint(0, 30 * 24 * 60 * 60))
    return random_date.strftime("%Y-%m-%dT%H:%M:%S")

# Generate synthetic vehicle data
def generate_vehicle_data(num_records=5000, num_vehicles=100):
    vehicle_types = ["car", "bus", "train"]
    data = []

    for _ in range(num_records):
        vehicle_id = random.randint(1, num_vehicles)
        lat, lng = generate_random_coordinates()
        speed = generate_speed()
        status = generate_status()
        vehicle_type = random.choice(vehicle_types)
        timestamp = generate_timestamp()

        data.append({
            "vehicle_id": vehicle_id,
            "lat": lat,
            "lng": lng,
            "speed": speed,
            "status": status,
            "type": vehicle_type,
            "timestamp": timestamp
        })

    return data

# Write data to a CSV file
def write_to_csv(data, filename="vehicle_data.csv"):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["vehicle_id", "lat", "lng", "speed", "status", "type", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ {len(data)} records written to {filename}")

if __name__ == "__main__":
    num_records = 10000  # Adjust the number of records based on your needs
    synthetic_data = generate_vehicle_data(num_records=num_records)
    write_to_csv(synthetic_data)
