import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import argparse
import os

def preprocess_data(data):
    """Preprocess the data by encoding, handling missing values, and feature selection."""
    
    # Encode 'status' as 0 for 'on-time' and 1 for 'delayed'
    data['status'] = data['status'].map({'on-time': 0, 'delayed': 1})
    
    # Fill missing values separately for numeric and categorical columns
    for column in data.columns:
        if data[column].dtype == 'object':  # Categorical columns
            data[column] = data[column].fillna(data[column].mode()[0])
        else:  # Numeric columns
            data[column] = data[column].fillna(data[column].median())
    
    # One-Hot Encode 'type' column (car, bus, train)
    data = pd.get_dummies(data, columns=['type'], drop_first=True)
    
    # Drop unnecessary columns
    data = data.drop(columns=["vehicle_id", "timestamp"])
    
    return data

def train_model(data_path, model_dir):
    """Train a Random Forest Classifier on the vehicle data."""
    print(f"Loading data from {data_path}...")
    
    # Use relative path for loading the CSV file
    data = pd.read_csv(data_path)
    
    # Preprocess the data
    data = preprocess_data(data)
    
    # Split data into features and target
    X = data.drop(columns=["status"])
    y = data["status"]
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "vehicle_status_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved at {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", required=False, help="Path to input CSV file", default="vehicle_data.csv")
    parser.add_argument("--model-dir", required=True, help="Directory to save the trained model")
    args = parser.parse_args()
    
    train_model(args.data_path, args.model_dir)
