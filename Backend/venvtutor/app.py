from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connexion à la première base de données MongoDB (stagiare.ma)
client_stagiaire = MongoClient('localhost', 27017)
db_stagiaire = client_stagiaire['tutorr']  
collection_stagiaire = db_stagiaire['tutorr']  

# Connexion à la deuxième base de données MongoDB (stage.ma)
client_stage = MongoClient('localhost', 27017)
db_stage = client_stage['tt']  
collection_stage = db_stage['tt']  

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = search_query(query)
    return jsonify({"results": results})

def search_query(query):
    results = []
    keywords = query.lower().split()  # Convertir la requête en une liste de mots-clés en minuscules

    # Recherche dans la première base de données (stagiaire.ma)
    for doc in collection_stagiaire.find():
        text = doc['join'].lower()  
        if all(keyword in text for keyword in keywords):
            result = {
                "lien": doc['lien_href'],
                "titre": doc['titre'],
                "description": doc.get('description', 'Description non disponible')
            }
            results.append(result)

    # Recherche dans la deuxième base de données (stage.ma)
    for doc in collection_stage.find():
        text = doc['join'].lower()  
        if all(keyword in text for keyword in keywords):
            result = {
                "lien": doc['lien_href'],
                "titre": doc['titre'],
                "description": f"{doc['titre']} dans l'entreprise {doc['entreprise']} de type {doc['type_stage']}",
            }
            results.append(result)

    return results

def fetch_and_organize_offers():
    categories = {}
    
    # Récupérer les offres de la première base de données (tutorr)
    for doc in collection_stagiaire.find():
        category = doc['type_stage']
        offer = {
            "titre": doc['titre'],
            "description": doc.get('description', 'Description non disponible'),
            "lien": doc['lien_href']
        }
        if category not in categories:
            categories[category] = []
        categories[category].append(offer)
    
    # Récupérer les offres de la deuxième base de données (tt)
    for doc in collection_stage.find():
        category = doc['type_stage']
        offer = {
            "titre": doc['titre'],
            "description": f"{doc['titre']} dans l'entreprise {doc['entreprise']} de type: {doc['type_stage']}",
            "lien": doc['lien_href']
        }
        if category not in categories:
            categories[category] = []
        categories[category].append(offer)
    
    return categories

@app.route('/offers', methods=['GET'])
def get_offers():
    organized_offers = fetch_and_organize_offers()
    categories = [{"name": category, "offers": offers} for category, offers in organized_offers.items()]
    return jsonify({"categories": categories})

if __name__ == '__main__':
    app.run(debug=True)
