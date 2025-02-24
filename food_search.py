import requests
# Added a comment to trigger PR creation
from bs4 import BeautifulSoup
import json

def search_food_item(food_item, store):
    search_query = f"{food_item} site:{store}"
    search_url = f"http://192.168.1.237:4000/?q={search_query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    return response.text

def extract_prices(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    for result in soup.select('article'):
        title_element = result.select_one('h3 a')
        if title_element:
            title = title_element.text
            link = title_element['href']
            results.append({'title': title, 'link': link, 'price': "N/A"}) # Price N/A as price extraction is not working
    return results

def main():
    food_item = "lait" # Example food item
    stores = {
        "IGA": "iga.net",
        "Metro": "metro.ca",
        "SuperC": "superc.ca",
        "Maxi": "maxi.ca"
    }

    all_results = {}
    for store_name, store_domain in stores.items():
        print(f"\n--- {store_name} ---")
        print(f"Searching {food_item} on {store_name}...")
        html_content = search_food_item(food_item, store_domain)
        search_results = extract_prices(html_content)
        if search_results:
            print("Results:")
            for result in search_results:
                print(f"- Title: {result['title']}")
                print(f"  Link: {result['link']}")
        else:
            print("No results found.")
        all_results[store_name] = search_results

if __name__ == "__main__":
    main()