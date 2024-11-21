import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Configuración Firebase
cred = credentials.Certificate("assets/ml-scrapping-21e01-firebase-adminsdk-blpoa-30ded61242.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# En esta sección empieza el scraping
def scrape_mercadolibre(url):
    try:
        print(f"Procesando URL: {url}")  # Verifica la URL recibida
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error al acceder a la URL: {response.status_code}")
            return {"error": f"Error al acceder a la URL: {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No disponible"
        price = soup.find("span", class_="price-tag-fraction").get_text(strip=True) if soup.find("span", class_="price-tag-fraction") else "No disponible"
        scraped_data = {"title": title, "price": price, "url": url}
        print(f"Datos scrapeados: {scraped_data}")  # Log de los datos obtenidos
        return scraped_data
    except Exception as e:
        print(f"Error en scrape_mercadolibre: {e}")
        return {"error": str(e)}
    # response = requests.get(url)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     products = []

    #     for item in soup.find_all('li', class_='ui-search-layout_item'):
    #         title = item.find('h2', class_='ui-search-item__title')
    #         price = item.find('span', class_='price-tag-fraction')

    #         if title and price:
    #             products.append({
    #                 'title': title.text.strip(),
    #                 'price': price.text.strip()
    #             })
    #     return products
    # else:
    #     print(f"Error al acceder a la URL: {response.status_code}")
    #     return []

def save_to_firebase(data, collection_name="mercadolibre_data"):
    for item in data:
        db.collection(collection_name).add(item)

url = "https://www.mercadolibre.com.co/bookmarks/wishlist/hub/detail/15df8c6b-c90b-40e8-82a4-fff49a3261bf"
scraped_data = scrape_mercadolibre(url)

if scraped_data:
    save_to_firebase(scraped_data)
    print("Datos guardados en firebase.")
else:
    print("No se obtuvieron datos.")