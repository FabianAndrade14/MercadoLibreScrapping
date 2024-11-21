import json
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from scrapper.mercado_Libre_Scrapper import scrape_mercadolibre, save_to_firebase

app = Flask(__name__)
api = Api(app)

# configuración de Swagger
SWAGGER_URL = "/swagger"
API_DOC_PATH = "static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, "/static/swagger.json")
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# en esta sección se crean los endpoints
@app.route("/static/swagger.json")
def swagger_json():
    """
    Devuelve el archivo JSON de Swagger desde el sistema de archivos.
    """
    with open(API_DOC_PATH,"r") as swagger_file:
        swagger_data = json.load(swagger_file)
    return jsonify(swagger_data)

class MercadoLibreScraper(Resource):
    def get(self):
        """
        Método GET: Verifica si el endpoint está disponible.
        """
        return {"message": "Este endpoint está funcionando. Usa POST para enviar datos."}, 200
        
    def post(self):
        """
        Endpoint para realizar scraping en MercadoLibre.
        """
        data = request.get_json()
        url = data.get("url")

        if not url:
            return {"error": "URL es requerida."}, 400
        
        scraped_data = scrape_mercadolibre(url)
        if "error" in scraped_data:
            return scraped_data, 400
        
        # Guardando los datos en Firebase
        save_to_firebase(scraped_data)
        return {"message": "Datos guardados en Firebase.", "data": scraped_data}, 201
    
api.add_resource(MercadoLibreScraper, "/api/scrape")

if __name__ == "__main__":
    app.run(debug=True)