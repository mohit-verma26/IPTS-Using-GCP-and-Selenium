from google.cloud import storage
import os

# Hardcoding the environment variable for credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ROG/Downloads/SST6826f/SST6826/service-account-file-new.json"

def upload_model_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the specified GCS bucket."""
    print(f"🌍 Using credentials from: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    # Upload the file to GCS
    blob.upload_from_filename(source_file_name)
    print(f"✅ Model uploaded to gs://{bucket_name}/{destination_blob_name}")

if __name__ == "__main__":
    bucket_name = "my_bucket_vehicle"  # Replace with your bucket name
    source_file_name = "./model_output/vehicle_status_model.joblib"
    destination_blob_name = "vehicle_models/vehicle_status_model.joblib"
    
    upload_model_to_gcs(bucket_name, source_file_name, destination_blob_name)
