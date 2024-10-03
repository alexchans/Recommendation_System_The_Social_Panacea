import firebase_admin
from firebase_admin import credentials, db
import numpy as np
from gensim.models import KeyedVectors
import json

# Initialize Firebase, store db to data
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesocialpanacea-default-rtdb.firebaseio.com/'  
})
ref = db.reference('users')  
data = ref.get()

# Load pre-trained GloVe embeddings 
glove_file = 'glove.6B.50d.txt'  
word_vectors = KeyedVectors.load_word2vec_format(glove_file, binary=False, no_header=True)

# helper function to do word embedding and normalization
def word_embedding_normalization(sentence):
    words = sentence.split()  
    word_embeddings = []
    for word in words:
        word = word.lower()  
        if word in word_vectors: 
            word_embeddings.append(word_vectors[word])
    if not word_embeddings: 
        return 0.0
    mean_embedding = np.mean(word_embeddings, axis=0)
    single_value = np.mean(mean_embedding) 
    return (single_value - np.min(mean_embedding)) / (np.max(mean_embedding) - np.min(mean_embedding))

# Map used to convert personality type to words
trait_translation = {
    'I': 'Introversion', 'E': 'Extraversion',
    'S': 'Sensing', 'N': 'Intuition',
    'T': 'Thinking', 'F': 'Feeling',
    'J': 'Judging', 'P': 'Perceiving'
}

# helper function to convert personality type to words
def mbti_to_fullwords(personality_type):
    if len(personality_type) != 4 or not all(char in trait_translation for char in personality_type):
        return "Invalid MBTI type"
    return " ".join(trait_translation[char] for char in personality_type)

# Helper function to extract the last word from the enneagramType
def extract_last_word(enneagram_type):
    if isinstance(enneagram_type, str) and enneagram_type.strip() != '':
        return enneagram_type.split()[-1]
    
# Weights in percentage (as decimal)
weights = {
    'age': 0.10,
    'university': 0.15,
    'sportsPreferences': 0.08,
    'pickUpGamesPreferences': 0.05,
    'foodPreferences': 0.05,
    'eatingWithFriends': 0.06,
    'cookingWithFriends': 0.06,
    'popCulturePreferences': 0.04,
    'popCultureFriendPreferences': 0.05,
    'travelWithFriends': 0.07,
    'personalityType': 0.14,
    'enneagramType': 0.08,
    'meetingNewPeopleComfortLevel': 0.07
}

# Preprocess data and apply weights
for user, user_info in data.items():
    user_info['age'] = (user_info['age'] / 100) * weights['age']
    user_info['university'] = word_embedding_normalization(user_info['university']) * weights['university']
    user_info['sportsPreferences'] = (len(user_info['sportsPreferences']) / 11) * weights['sportsPreferences']
    user_info['pickUpGamesPreferences'] = (len(user_info['pickUpGamesPreferences']) / 9) * weights['pickUpGamesPreferences']
    user_info['foodPreferences'] = (len(user_info['foodPreferences']) / 9) * weights['foodPreferences']
    user_info['eatingWithFriends'] = (1 if user_info['eatingWithFriends'] else 0) * weights['eatingWithFriends']
    user_info['cookingWithFriends'] = (1 if user_info['cookingWithFriends'] else 0) * weights['cookingWithFriends']
    user_info['popCulturePreferences'] = (len(user_info['popCulturePreferences']) / 7) * weights['popCulturePreferences']
    user_info['popCultureFriendPreferences'] = (len(user_info['popCultureFriendPreferences']) / 7) * weights['popCultureFriendPreferences']
    user_info['travelWithFriends'] = (1 if user_info['travelWithFriends'] else 0) * weights['travelWithFriends']
    user_info['personalityType'] = word_embedding_normalization(mbti_to_fullwords(user_info['personalityType'])) * weights['personalityType'] if user_info['personalityType'] != '' else 0
    user_info['enneagramType'] = word_embedding_normalization(extract_last_word(user_info['enneagramType'])) * weights['enneagramType'] if user_info['enneagramType'] != '' else 0
    user_info['meetingNewPeopleComfortLevel'] = (user_info['meetingNewPeopleComfortLevel'] / 5) * weights['meetingNewPeopleComfortLevel']

# helper function for saving data
def convert_floats(data):
    if isinstance(data, dict):
        return {k: convert_floats(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_floats(i) for i in data]
    elif isinstance(data, np.float32):  # Check for float32 type
        return float(data)  # Convert to Python float
    return data

data = convert_floats(data)
# Save data as a JSON file
with open('processed_users_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)  # Use indent for pretty printing
print("Data has been saved as processed_users_data.json.")
