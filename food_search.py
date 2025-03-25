# Importation des bibliothèques nécessaires pour les requêtes HTTP et le parsing HTML
import requests
# Importation de la bibliothèque BeautifulSoup pour le parsing HTML
from bs4 import BeautifulSoup
# Importation de la bibliothèque json pour la gestion des données au format JSON
import json

# Ajout d'un commentaire pour la fonction de recherche d'éléments alimentaires
def search_food_item(food_item, store):
    # Construction de la requête de recherche
    search_query = f"{food_item} site:{store}"
    # Construction de l'URL de recherche
    search_url = f"http://192.168.1.237:4000/?q={search_query}"
    # Définition de l'entête User-Agent pour la requête
    headers = {'User-Agent': 'Mozilla/5.0'}
    # Envoi de la requête GET avec les entêtes définis
    response = requests.get(search_url, headers=headers)
    # Vérification de l'état de la réponse
    response.raise_for_status()
    # Renvoi du contenu de la réponse
    return response.text

# Ajout d'un commentaire pour la fonction d'extraction des prix
def extract_prices(html_content):
    # Création d'un objet BeautifulSoup pour parser le contenu HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # Initialisation d'une liste pour stocker les résultats
    results = []
    # Boucle sur les éléments de type 'article' pour extraire les informations
    for result in soup.select('article'):
        # Recherche de l'élément 'h3 a' contenant le titre et le lien
        title_element = result.select_one('h3 a')
        # Vérification si l'élément 'h3 a' est présent
        if title_element:
            # Extraction du titre et du lien
            title = title_element.text
            link = title_element['href']
            # Ajout du résultat à la liste avec le prix par défaut "N/A"
            results.append({'title': title, 'link': link, 'price': "N/A"}) # Price N/A as price extraction is not working
    # Retour de la liste des résultats
    return results

# Définition de la fonction principale
def main():
    # Exemple d'élément alimentaire à rechercher
    food_item = "lait"

    # Dictionnaire des magasins avec leurs noms et domaines
    stores = {
        "IGA": "iga.net",
        "Metro": "metro.ca",
        "SuperC": "superc.ca",
        "Maxi": "maxi.ca"
    }

    # Initialisation d'un dictionnaire pour stocker les résultats de toutes les recherches
    all_results = {}

    # Boucle sur les magasins pour effectuer les recherches
    for store_name, store_domain in stores.items():
        # Affichage du nom du magasin actuel
        print(f"\n--- {store_name} ---")

        # Affichage d'un message pour indiquer la recherche en cours
        print(f"Searching {food_item} on {store_name}...")

        # Recherche de l'élément alimentaire sur le site du magasin
        html_content = search_food_item(food_item, store_domain)

        # Extraction des résultats de la recherche
        search_results = extract_prices(html_content)

        # Vérification si des résultats ont été trouvés
        if search_results:
            # Affichage d'un message pour indiquer la présence de résultats
            print("Results:")

            # Boucle sur les résultats pour les afficher
            for result in search_results:
                # Affichage du titre et du lien de chaque résultat
                print(f"- Title: {result['title']}")
                print(f"  Link: {result['link']}")
        else:
            # Affichage d'un message pour indiquer l'absence de résultats
            print("No results found.")

        # Stockage des résultats de la recherche actuelle dans le dictionnaire des résultats globaux
        all_results[store_name] = search_results

if __name__ == "__main__":
    main()