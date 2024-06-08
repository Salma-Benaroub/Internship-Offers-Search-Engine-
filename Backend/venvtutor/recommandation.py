from flask import Flask, request, jsonify
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask_cors import CORS
from flask import session

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tutorr']
historique_collection = db['historique']
stage_collection = db['tutorr']

def get_historique_data():
    return list(historique_collection.find({}))

def get_stage_data():
    return list(stage_collection.find({}))

def create_user_profile(user_keywords, vectorizer):
    user_vector = np.zeros((1, len(vectorizer.get_feature_names_out())))
    if user_keywords:
        keyword_vector = vectorizer.transform(user_keywords)
        user_vector += keyword_vector.toarray().sum(axis=0)
    return user_vector / len(user_keywords) if user_keywords else user_vector

def recommend_stages(user_id, user_profiles, stage_vectors, stage_ids, top_n=20):
    user_vector = user_profiles[user_id]
    similarities = cosine_similarity(user_vector, stage_vectors)
    similar_indices = similarities.argsort()[0][-top_n:][::-1]
    recommended_stages = [stage_ids[idx] for idx in similar_indices]
    return recommended_stages

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    historique_data = get_historique_data()

    if not historique_data:
        return jsonify({"error": "No historique data found"}), 404

    user_keywords = []

    for entry in historique_data:
        if str(entry['user_id']) == user_id:
            user_keywords.append(entry.get('keywords', ''))

    if not user_keywords:
        return jsonify({"error": "No keywords found in historique data for this user"}), 404

    vectorizer = TfidfVectorizer()
    vectorizer.fit([user_profile for user_profile in user_keywords])

    user_profiles = {user_id: create_user_profile(user_keywords, vectorizer)}

    stage_data = get_stage_data()

    if not stage_data:
        return jsonify({"error": "No stage data found"}), 404

    stage_texts = [stage.get('join', '') for stage in stage_data]
    stage_ids = [str(stage['_id']) for stage in stage_data]

    stage_vectors = vectorizer.transform(stage_texts)

    recommended_stages = recommend_stages(user_id, user_profiles, stage_vectors, stage_ids)

    return jsonify({"user_id": user_id, "recommended_stages": recommended_stages})

if __name__ == '__main__':
    app.run(port=5000, debug=True)