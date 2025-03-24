# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables to avoid Python buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set environment for GCP service account key
ENV GOOGLE_APPLICATION_CREDENTIALS=/home/mohit_verma/service-account-file-new.json

# Create a directory for the app
WORKDIR /app

# Copy the entire application into the Docker container
COPY . /app

# Install required packages
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
