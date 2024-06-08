import torch
from transformers import BertTokenizer, BertModel
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Charger le modèle BERT(Bidirectional Encoder Representations from Transformers) et le tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased')

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db_tutore = client['tutore']
collection_tutore = db_tutore['etudiant']
db_offres = client['offres']
collection_offres = db_offres['offres']

def embed_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Utiliser les embeddings du CLS token
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return embeddings

def preprocess_and_embed(docs, fields):
    texts = [' '.join([doc[field] for field in fields if field in doc]) for doc in docs]
    embeddings = np.vstack([embed_text(text) for text in texts])
    return embeddings

# Fonction principale de recherche
def search(query):
    # Préparer les corpus
    tutore_docs = list(collection_tutore.find())
    offres_docs = list(collection_offres.find())

    # Créer les embeddings
    tutore_embeddings = preprocess_and_embed(tutore_docs, ['email', 'password'])
    offres_embeddings = preprocess_and_embed(offres_docs, ['titre', 'description'])

    # Embed la requête
    query_embedding = embed_text(query)

    # Calculer les similarités cosinus
    tutore_similarities = cosine_similarity(query_embedding, tutore_embeddings).flatten()
    offres_similarities = cosine_similarity(query_embedding, offres_embeddings).flatten()

    # Trouver les documents les plus similaires
    most_similar_tutore_docs_indices = tutore_similarities.argsort()[-5:][::-1]
    most_similar_offres_docs_indices = offres_similarities.argsort()[-5:][::-1]

    similar_tutore_docs = [tutore_docs[i] for i in most_similar_tutore_docs_indices]
    similar_offres_docs = [offres_docs[i] for i in most_similar_offres_docs_indices]

    # Combiner les résultats
    results = {
        'tutore': similar_tutore_docs,
        'offres': similar_offres_docs
    }

    return results
