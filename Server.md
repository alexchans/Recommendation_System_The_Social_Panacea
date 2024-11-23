# Recommendation System Server Documentation

## Overview

This repository contains a recommendation system API built with **FastAPI**. It uses **Firebase Realtime Database** to fetch user data and updates a similarity matrix (`user_similarities.json`) whenever the database changes. The server exposes endpoints to access user recommendations based on precomputed similarity data.

---

## How It Works

### Key Components

1. **`server.py`**

   - The main FastAPI server script.
   - Starts an API server to handle user recommendation requests.
   - Listens to changes in Firebase and triggers updates to the similarity matrix.

2. **`recommendation_system.py`**

   - Recomputes the similarity matrix (`user_similarities.json`) based on user data from Firebase.
   - Automatically triggered when a change is detected in the Firebase `users` node.

3. **`user_similarities.json`**

   - Stores the precomputed similarity matrix for user recommendations.

4. **Firebase Listener**
   - Integrated into `server.py`.
   - Monitors the `users` node in Firebase for changes and triggers `recommendation_system.py` as needed.

---

## API Endpoints

### 1. Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Confirms that the server is running.
- **Response**:
  ```json
  {
    "message": "Recommendation System API is live!"
  }
  ```

### 2. Recommendations Endpoint

- **URL**: `/recommendations/{user_id}`
- **Method**: `GET`
- **Query Parameters**:
  - top_n (optional, default: 5): Number of top recommendations to return.
- **Description**: Returns the top N most similar users to the given user.
- **Response**:

  ```json
  {
  "user_id": "user123",
  "recommendations": {
    "user456": 0.923,
    "user789": 0.806,
    ...
  }
  }
  ```

---

## Running the Server and Testing Endpoints

### How to Run the Server on Terminal

To start the server, use the following command in your terminal:

```bash
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

### How to Use curl to Test Endpoints

curl is a command-line tool for making HTTP requests. You can use it to test your FastAPI endpoints.

**Test the Root Endpoint**

Run the following command to check if the server is live:

```bash
curl http://127.0.0.1:8000/
```

Expected Response:

```json
{
  "message": "Recommendation System API is live!"
}
```

**Test the Recommendations Endpoint**

Replace user_id with a valid user ID to fetch recommendations:

```bash
curl "http://127.0.0.1:8000/recommendations/user_id?top_n=5"
```

Expected Response:

```json
{
  "user_id": "user_id",
  "recommendations": {
    "user456": 0.923,
    "user789": 0.806
  }
}
```

# How to Deploy

## 1. Prerequisites

Install Python 3.8 or higher.
Install required dependencies:

```bash
pip install -r requirements.txt
```

- Ensure the Firebase Admin SDK key (`key.json`) is in the root directory.

## 2. Cloud Deployment (Heroku Example)

### Prepare the Repository

Ensure the repository includes the following files:

- `server.py`
- `recommendation_system.py`
- `requirements.txt`
- `Procfile`

### Create a Procfile

```bash
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Install Heroku CLI

Download and install the Heroku CLI from Heroku CLI.

### Deploy to Heroku

### 1. Login

```bash
heroku login
```

### 2. Create a Heroku app

```bash
heroku create your-app-name
```

### 3. Push the code

```bash
git push heroku main
```

### Test the App:

Access your app at https://your-app-name.herokuapp.com/.

## Notes for Future Teams

- Ensure that key.json is securely stored and not pushed to public repositories.
- Update requirements.txt whenever new dependencies are added.
- Test the Firebase listener thoroughly before deploying changes.
- For any questions, refer to the the FastAPI documentation or Firebase documentation.
