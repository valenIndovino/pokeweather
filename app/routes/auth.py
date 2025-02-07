from flask import Blueprint, jsonify, request
from app.services.keycloak_service import KeycloakService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return jsonify(KeycloakService.register_user(data.get("username"), data.get("password")))

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return jsonify(KeycloakService.get_token(data.get("username"), data.get("password")))
