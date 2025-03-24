import os
from google.cloud import firestore

# Manually set the path in Python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ROG/Downloads/SST6826f/SST6826/service-account-file-new.json"

try:
    db = firestore.Client()
    print("✅ Successfully connected to Firestore!")
except Exception as e:
    print("❌ Error:", e)
