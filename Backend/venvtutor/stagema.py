from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import re
import time

def clean_text(text):
    # Suppression des caractères spéciaux et des symboles de ponctuation, des espaces non importants
    cleaned_text = re.sub(r'[^\w\s\-]', '', text)
    # Suppression des espaces non importants (espaces en début et fin de chaîne, espaces multiples)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    # Conversion en minuscules
    cleaned_text = cleaned_text.lower()
    return cleaned_text

def clean_categories(categories):
    cleaned_category = ""
    if len(categories) > 1:
        cleaned_category = clean_text(categories[1].text.strip())
    return cleaned_category


def run_scraping():
    url = 'https://www.stage.ma/offres-stage?salary=false&free_submissions_left=false&page=3'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    data = []
    # Trouver tous les éléments avec la classe spécifiée
    items = soup.find_all("div", class_="flex flex-col min-tab:justify-between max-mob:items-center")

    # Parcourir chaque élément et extraire les informations
    for item in items:
        # Extraire le nom de l'organisme
        nom_organisme_elem = item.find("a", class_="min-tab:hidden max-mob:mt-1 text-emerald-600 hover:underline")
        nom_organisme = nom_organisme_elem.text.strip() if nom_organisme_elem else "Nom d'organisme non spécifié"
        # Extraire le titre de l'offre de stage
        titre_offre_stage_elem = item.find("a", class_="flex text-lg capitalize max-mob:mt-4 text-blue-600 underline hover:no-underline group-hover:text-primary-600 font-bold")
        titre_offre_stage = titre_offre_stage_elem.text.strip() if titre_offre_stage_elem else "Titre d'offre de stage non spécifié"
        # Extraire le lien de l'offre de stage
        lien_offre_stage = titre_offre_stage_elem["href"] if titre_offre_stage_elem else "Lien non spécifié"
        
        # Extraire les catégories de stage
        categories_span = item.find("div", class_="flex space-x-2 max-mob:mt-2")
        categories = categories_span.find_all("span") if categories_span else []
        type_stage = clean_categories(categories)

        # Si le type de stage est "stage fin d'études", le remplacer par "PFE"
        if type_stage == "stage fin détudes":
            type_stage = "PFE"

        # Extraire la rémunération
        remuneration_elem = item.find("span", class_="text-xs px-2 py-1 rounded-lg bg-primary-100 text-primary-600")
        remuneration = remuneration_elem.text.strip() if remuneration_elem else "Rémunération non spécifiée"
        
        # Ajouter les données extraites à la liste 'data'
        data.append((nom_organisme, titre_offre_stage, lien_offre_stage, type_stage, remuneration))

        # Attendre quelques secondes avant la prochaine requête pour éviter de surcharger le serveur
        time.sleep(1)

    # Connexion à MongoDB
    client = MongoClient('localhost', 27017)  
    db = client['tt']  
    collection = db['tt']  

    # Ajouter les données à MongoDB
    for offer_data in data:
        nom_organisme, titre_offre_stage, lien_offre_stage, type_stage, remuneration = offer_data
        
        # Nettoyer le titre de l'offre de stage
        cleaned_titre_offre_stage = clean_text(titre_offre_stage)
        
        # Concaténer le titre de l'offre de stage nettoyé et le type de stage
        join = cleaned_titre_offre_stage + " " + type_stage
        
        # Ajouter les données à MongoDB
        collection.update_one(
            {"titre": titre_offre_stage},  # Critères pour trouver l'offre existante
            {"$setOnInsert": {  # Opérateur $setOnInsert pour ne pas mettre à jour les documents existants
                "entreprise": nom_organisme,
                "titre": titre_offre_stage,
                "lien_href": lien_offre_stage,
                "type_stage": type_stage,
                "remuneration": remuneration,
                "join": join
            }},
            upsert=True  # Insérer si l'offre n'existe pas, sinon mettre à jour
        )

    print("Les données ont été ajoutées à la base de données MongoDB.")

def check_for_new_data():
    while True:
        run_scraping()
        time.sleep(60)

if __name__ == "__main__":
    check_for_new_data()