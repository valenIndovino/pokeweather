from flask import Flask
from flask_cors import CORS
from app.routes import register_blueprints
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # Habilitar CORS en toda la API, esto lo hago para poder ejecutar los endpoints desde Swagger

    register_blueprints(app)

    return app