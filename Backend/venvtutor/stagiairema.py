import time
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import re



def clean_text(text):
    # Suppression des caractères spéciaux et des symboles de ponctuation, des espaces non importants
    cleaned_text = re.sub(r'[^\w\s\-]', '', text)
    # Suppression des espaces non importants (espaces en début et fin de chaîne, espaces multiples)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    # Conversion en minuscules
    cleaned_text = cleaned_text.lower()
    return cleaned_text


def clean_data(offer):
    # Nettoyage du titre : suppression des espaces inutiles
    offer["titre"] = offer["titre"].strip()
    # Nettoyage de la description : suppression des balises HTML et des espaces inutiles
    offer["description"] = BeautifulSoup(offer["description"], "html.parser").get_text().strip()
    # Nettoyage de l'entreprise : suppression des espaces inutiles
    offer["entreprise"] = offer["entreprise"].strip()
    # Nettoyage des autres champs (avantages, rémunération, convention)
    offer["avantages"] = offer["avantages"].strip()
    offer["remuneration"] = offer["remuneration"].strip()
    offer["convention"] = offer["convention"].strip()

     # Nettoyage des champs avant le join
    titre_cleaned = clean_text(offer["titre"])
    description_cleaned = clean_text(offer["description"])
    type_stage_cleaned = clean_text(offer["type_stage"])


    # Ajout du champ "join" en joignant les textes nettoyés
    offer["join"] = " ".join([titre_cleaned, description_cleaned, type_stage_cleaned]).strip()

    return offer



def run_scraping():
    url = 'https://www.stagiaires.ma/offres-stages'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # notre code de scraping pour récupérer les données
    data = []
    divs = soup.find_all('div', class_='offer-container')

    for offer in divs:
        # Code pour extraire les informations de chaque offre de stage
        date_debut_stage_tag = offer.find('small', {'title': 'Date début de stage'})
        titre_stage_tag = offer.find('strong')
        description_tag = offer.find('p', class_='mt2')
        div_actions = offer.find('div', class_='actions')
        entreprise_tag = div_actions.find('small', class_='text-muted')
        avantages_tag = offer.find('span', class_='btn-info')
        remuneration_tag = offer.find('span', class_='btn-warning')
        convention_tag = offer.find('span', class_='btn-success')
        duree_stage_tag = offer.find('span', title="Durée de stage")
        type_stage_tag = offer.find('span', class_='btn-primary')
        lien_href = offer.find('a')['href'] if offer.find('a') else "Lien non trouvé"
        
        if all([date_debut_stage_tag, titre_stage_tag, description_tag, entreprise_tag]):
            date_debut_stage = date_debut_stage_tag.text.strip()
            titre_stage = titre_stage_tag.text.strip()
            description = description_tag.text.strip()
            entreprise = entreprise_tag.text.strip()
            avantages = avantages_tag.get('title').split(': ')[1] if avantages_tag else "Non spécifié"
            remuneration = remuneration_tag.get('title') if remuneration_tag else "Non spécifié"
            convention = "Oui" if convention_tag else "Non"
            duree_stage = duree_stage_tag.text.strip() if duree_stage_tag else "Non spécifié"
            type_stage = type_stage_tag.text.strip() if type_stage_tag else "Non spécifié"

            data.append({
                "date_debut": date_debut_stage,
                "titre": titre_stage,
                "description": description,
                "entreprise": entreprise,
                "avantages": avantages,
                "remuneration": remuneration,
                "convention": convention,
                "duree_stage": duree_stage,
                "type_stage": type_stage,
                "lien_href": lien_href
            })

    # Vérification des nouvelles données par rapport à celles déjà présentes dans la base de données MongoDB
    client = MongoClient('localhost', 27017)  # Connexion à MongoDB (par défaut localhost, port 27017)
    db = client['tutorr']  # Nom de la base de données
    collection = db['tutorr']  # Nom de la collection
    
    for offer in data:
        offer = clean_data(offer)
        # Vérifier si l'offre existe déjà dans la base de données en fonction de certains critères
        existing_offer = collection.find_one({"titre": offer["titre"], "entreprise": offer["entreprise"]})

        if existing_offer is None:
            # Si l'offre n'existe pas déjà dans la base de données, l'ajouter
            collection.insert_one(offer)
            print("Nouvelle offre ajoutée:", offer)

def check_for_new_data():
    while True:
        run_scraping()
        time.sleep(1)  # Vérifiez toutes les heures

if __name__ == "__main__":
    check_for_new_data()
