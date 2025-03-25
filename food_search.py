# Importation des bibliothèques nécessaires pour les requêtes HTTP, le parsing HTML et la gestion des données JSON
import requests
from bs4 import BeautifulSoup
import json

# Ce bloc de code définit une fonction pour rechercher un article alimentaire sur un site web donné en utilisant une requête HTTP GET.

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

def extract_prices(html_content):
    # Analyse du contenu HTML et extraction des prix.
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    for result in soup.select('article'):
        title_element = result.select_one('h3 a')
        if title_element:
            title = title_element.text
            link = title_element['href']
            results.append({'title': title, 'link': link, 'price': "N/A"}) # Prix non disponible car l'extraction du prix ne fonctionne pas
    return results

def main():
    # Fonction principale pour rechercher des articles alimentaires dans différents magasins et afficher les résultats.
    food_item = "lait"
    stores = {
        "IGA": "iga.net",
        "Metro": "metro.ca",
        "SuperC": "superc.ca",
        "Maxi": "maxi.ca"
    }
    all_results = {}
    for store_name, store_domain in stores.items():
        print(f"\n--- {store_name} ---")
        print(f"Recherche de {food_item} sur {store_name}...")
        html_content = search_food_item(food_item, store_domain)
        search_results = extract_prices(html_content)
        if search_results:
            print("Résultats:")
            for result in search_results:
                print(f"- Titre: {result['title']}")
                print(f"  Lien: {result['link']}")
        else:
            print("Aucun résultat trouvé.")
        all_results[store_name] = search_results

if __name__ == "__main__":
    main()