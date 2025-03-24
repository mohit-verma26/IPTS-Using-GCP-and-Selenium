import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ROG/Downloads/SST6826f/SST6826/service-account-file-new.json"

print("Verifying credentials...")
print(f"Environment Variable: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")

storage_client = storage.Client()
buckets = list(storage_client.list_buckets())
for bucket in buckets:
    print(bucket.name)
