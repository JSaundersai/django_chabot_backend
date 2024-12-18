#!/bin/bash

# Navigate to the backend directory
cd ~/chatbot

# Activate the virtual environment
source venv/bin/activate

cd ~/chatbot/django_chabot_backend/backend/chatbot_dir

# Run the parameter_store_loader python file to update the .env with correct details
python3 parameter_store_loader.py

# Create MongoDB indexes before starting server
python3 -c "
from pymongo import MongoClient
from django.conf import settings
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DATABASE]
db.user_inputs.create_index([('user_id', 1)])
db.user_inputs.create_index([('timestamp', -1)])
db.conversations.create_index([('session_id', 1)])
db.conversations.create_index([('user_id', 1)])
db.interactions.create_index([('timestamp', -1)])
"

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Run Django development server
gunicorn --workers=3 \
         --bind 0.0.0.0:8000 \
         --access-logfile - \
         --error-logfile - \
         chatbot_project.wsgi:application
