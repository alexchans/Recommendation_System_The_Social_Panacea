# Recommendation System with Collaborative Filtering

This project implements a recommendation system using **collaborative filtering**. The model computes user similarities based on various attributes retrieved from a **Firebase Realtime Database**. The output is a JSON file containing each user's similarity with other users, ranked from highest to lowest.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/alexchans/Recommendation_System_The_Social_Panacea.git
```

### 2. Install required dependencies

```bash
pip install -r requirements.txt
```

### 3. Download required files

- **Firebase Admin SDK Key:** Download your key.json from Firebase (this is your private key).
- **GloVe Pre-trained Embeddings:** Download the glove.6B.50d.txt file from the GloVe website and place it in your working directory.

### 4. Configure Firebase

In the script, ensure the Firebase Realtime Database URL is properly set:

```bash
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-url.firebaseio.com/'
})

```

# How It Works

### User Data:

The script retrieves user data from the Firebase Realtime Database, containing user attributes like age, university, preferences, and personality types.

### Preprocessing:

1. **Weighted Attributes**:  
   Each attribute is processed and given a specific weight based on its importance.
2. **Text-based Fields (University, Personality Types)**:  
   Text fields are converted into word embeddings using GloVe embeddings and normalized.
3. **Numerical Fields (Age, Preferences)**:  
   Numerical values are normalized to fit between 0 and 1, then scaled by their respective weights.

### Collaborative Filtering:

- After preprocessing, the system uses cosine similarity to measure how similar each user is to others based on the weighted attributes.
- The result is a similarity matrix that shows the similarity score between each pair of users.

### Output:

- The final output is a JSON file (`user_similarities.json`) that lists each user and their similarity with others, sorted from the most similar to the least.

---

## Data Preprocessing

The script uses different preprocessing techniques based on the type of data:

1. **Text Fields (e.g., University, Personality Type)**:  
   Processed using word embeddings and normalized.
2. **Numerical Fields (e.g., Age, Preferences)**:  
   Scaled between 0 and 1, then multiplied by predefined weights.
3. **Boolean Fields (e.g., Cooking with Friends)**:  
   Converted to binary (0 or 1) and weighted accordingly.

---

## Weights

Each attribute is assigned a weight to reflect its importance in the similarity calculation. For example:

- **Age**: 10%
- **University**: 15%
- **Personality Type**: 14%
- **Sports Preferences**: 8%

---

## Collaborative Filtering

The model uses cosine similarity to compute how similar one user is to another based on their processed attributes.

# Running the Script

Once everything is set up, simply run the script to generate the similarity scores between users:

```bash
python recommendation_system.py
```

The similarity scores between users will be saved in a file named user_similarities.json.

# Output

The output JSON file will contain each user as a key, and a sorted list of other users with similarity scores as the value. Each user's own similarity score is excluded.

Example structure of the output:

```bash
{
    "user1": {
        "user3": 0.923,
        "user4": 0.806,
        ...
    },
    "user2": {
        "user4": 0.973,
        "user1": 0.776,
        ...
    }
}

```

# Notes

- The script is flexible and can be easily modified to accommodate additional user attributes or adjust the weights used in similarity calculations.
- The data preprocessing approach can be adjusted depending on the type of attribute being processed.

---

# Running the Server

For instructions on how to run, test, and deploy the server hosting this recommendation system, refer to the [Server.md](./Server.md) file.

The `Server.md` file includes:

- Detailed steps to start the FastAPI server locally.
- Guidance on testing endpoints.
- Deployment instructions for platforms like Heroku.
