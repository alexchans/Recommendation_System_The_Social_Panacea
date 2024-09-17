import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Example User-Question matrix
user_question_matrix = np.array([
    [4, 2, 5],  # User 1
    [3, 4, 1],  # User 2
    [4, 2, 5],  # User 3
    [1, 5, 3]   # User 4
])

# Compute cosine similarity between users
similarities = cosine_similarity(user_question_matrix)

print(similarities)

# Function to generate recommendation list for each user
def get_recommendations(similarity_matrix):
    recommendations = {}
    num_users = similarity_matrix.shape[0]

    for user in range(num_users):
        # Get similarity scores for the current user (excluding the self-similarity)
        other_users = [(i+1, similarity_matrix[user][i]) for i in range(num_users) if i != user]
        
        # Sort the other users based on similarity score in descending order
        sorted_similarities = sorted(other_users, key=lambda x: x[1], reverse=True)
        
        # Store the sorted list in recommendations dictionary
        recommendations[f"User {user + 1}"] = sorted_similarities
    
    return recommendations

# Get the sorted recommendations for each user
user_recommendations = get_recommendations(similarities)

# Print recommendations
for user, recs in user_recommendations.items():
    print(f"{user} recommendations: {recs}")
