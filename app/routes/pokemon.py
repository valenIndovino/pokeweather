from flask import Blueprint, jsonify, request
from app.services.pokemon_service import (
    get_pokemon_type,
    get_random_pokemon_by_type,
    get_longest_name_pokemon,
    get_random_pokemon_by_weather
)
from app.utils.auth_middleware import token_required

pokemon_bp = Blueprint("pokemon", __name__)

@pokemon_bp.route("/type/<name>", methods=["GET"])
@token_required
def pokemon_type(name):
    return jsonify(get_pokemon_type(name))

@pokemon_bp.route("/random/<type_name>", methods=["GET"])
@token_required
def random_pokemon(type_name):
    return jsonify(get_random_pokemon_by_type(type_name))

@pokemon_bp.route("/longest/<type_name>", methods=["GET"])
@token_required
def longest_pokemon(type_name):
    return jsonify(get_longest_name_pokemon(type_name))

@pokemon_bp.route("/weather/<city>", methods=["GET"])
@token_required
def pokemon_by_weather(city):
    return jsonify(get_random_pokemon_by_weather(city))