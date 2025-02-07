from flask import Blueprint
from .pokemon import pokemon_bp
from .auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(pokemon_bp, url_prefix="/api/pokemon") # Paquete de rutas de Pokemon
    app.register_blueprint(auth_bp, url_prefix="/api/auth") # Paquete de rutas de IDP