from app.config import Config
import requests
from functools import wraps
from flask import request, jsonify
import jwt
from jwt.algorithms import RSAAlgorithm

# Configuración de Keycloak
KEYCLOAK_SERVER_URL = Config.KEYCLOAK_SERVER_URL
KEYCLOAK_REALM = Config.KEYCLOAK_REALM
KEYCLOAK_PUBLIC_KEY = None

def get_keycloak_public_key(kid=None, alg="RS256"):
    """
    Obtiene la clave pública correcta de Keycloak según el algoritmo y `kid` del token.

    Args:
        kid (str): Key ID del token JWT para seleccionar la clave correcta.
        alg (str): Algoritmo esperado (por defecto "RS256").

    Returns:
        str: Clave pública en formato PEM o None si no se encuentra.
    """
    url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
    response = requests.get(url)

    if response.status_code == 200:
        keys = response.json().get("keys", [])
        
        for key in keys:
            # Filtrar por algoritmo y `kid` si se proporciona
            if key["alg"] == alg and (kid is None or key["kid"] == kid):
                return RSAAlgorithm.from_jwk(key)  # Convertir JWK a PEM

    return None  # No se encontró una clave válida

def token_required(f):
    """
    Middleware decorator para proteger rutas con autenticación JWT de Keycloak.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtener token del header Authorization
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Unauthorized", "message": "Invalid or missing authentication token. Please provide a valid Bearer token in the Authorization header."}), 401

        try:
            # Extraer el `kid` del token sin validarlo
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            # Obtener la clave pública correcta desde Keycloak
            public_key = get_keycloak_public_key(kid=kid)
            if not public_key:
                return jsonify({"error": "Could not retrieve public key"}), 500

            # Decodificar el token JWT con la clave correcta
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience="account"
            )

            # Adjuntar usuario al request
            request.user = decoded_token

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(*args, **kwargs)

    return decorated