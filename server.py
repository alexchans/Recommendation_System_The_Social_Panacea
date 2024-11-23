from fastapi import FastAPI, HTTPException
import json
import subprocess
import threading
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

# Firebase initialization
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesocialpanacea-default-rtdb.firebaseio.com/'
})

# Load similarities (initial load)
with open('user_similarities.json', 'r') as f:
    user_similarities = json.load(f)

app = FastAPI()

# Variables to track last state and update time
last_update_time = None
cached_data = None

# Function to recompute similarities
def recompute_similarities():
    print("Running recommendation_system.py...")
    subprocess.run(["python", "recommendation_system.py"])
    global user_similarities
    with open('user_similarities.json', 'r') as f:
        user_similarities = json.load(f)
    print("Updated user_similarities.json.")

# Listener function for Firebase
def on_users_changed(event):
    global last_update_time, cached_data

    current_time = datetime.now()
    ref = db.reference('users')
    current_data = ref.get()

    # Check for actual changes in the data
    if current_data != cached_data:  # Only update if data has changed
        print("Detected actual Firebase change.")
        cached_data = current_data  # Update the cache

        if last_update_time is None or (current_time - last_update_time).total_seconds() > 10:
            print("Updating similarities...")
            recompute_similarities()
            last_update_time = current_time
    else:
        print("No actual changes detected.")

# Start a Firebase listener in a separate thread
def start_firebase_listener():
    print("Starting Firebase listener...")
    ref = db.reference('users')
    ref.listen(on_users_changed)

listener_thread = threading.Thread(target=start_firebase_listener, daemon=True)
listener_thread.start()

# API endpoints
@app.get("/")
def home():
    return {"message": "Recommendation System API is live!"}

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: str, top_n: int = 5):
    if user_id not in user_similarities:
        raise HTTPException(status_code=404, detail="User not found")

    recommendations = list(user_similarities[user_id].items())[:top_n]
    return {"user_id": user_id, "recommendations": recommendations}

# To handle favicon requests
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return {}
