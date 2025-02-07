import requests
import os
import logging
from app.config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class KeycloakService:
    """
    Service to handle user authentication and registration in Keycloak.
    """

    BASE_URL = f"{Config.KEYCLOAK_SERVER_URL}/realms/{Config.KEYCLOAK_REALM}/protocol/openid-connect"

    @staticmethod
    def get_token(username, password):
        """
        Retrieves a JWT token from Keycloak for an authenticated user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict or tuple: The token response if successful, or an error message with status code.
        """
        url = f"{KeycloakService.BASE_URL}/token"
        data = {
            "client_id": Config.KEYCLOAK_CLIENT_ID,
            "grant_type": "password",
            "username": username,
            "password": password
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        logger.info(f"Requesting JWT token for user: {username}")

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            logger.info(f"Token successfully retrieved for user: {username}")
            return response.json()

        logger.warning(f"Failed login attempt for user: {username}")
        return {"error": "Invalid credentials"}, 401

    @staticmethod
    def register_user(username, password):
        """
        Registers a new user in Keycloak.

        Args:
            username (str): The username to register.
            password (str): The password for the new user.

        Returns:
            dict or tuple: A success message if the user is created, or an error message with status code.
        """
        url = f"{Config.KEYCLOAK_SERVER_URL}/admin/realms/{Config.KEYCLOAK_REALM}/users"
        data = {
            "username": username,
            "enabled": True,
            "credentials": [{"type": "password", "value": password, "temporary": False}]
        }
        headers = {"Content-Type": "application/json"}

        logger.info(f"Registering new user: {username}")

        admin_token = KeycloakService.get_admin_token()
        if "access_token" not in admin_token:
            logger.error("Admin authentication failed. Cannot register user.")
            return {"error": "Could not authenticate admin"}, 500

        headers["Authorization"] = f"Bearer {admin_token['access_token']}"
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            logger.info(f"User registered successfully: {username}")
            return {"message": "User registered successfully"}, 201

        logger.error(f"Failed to register user: {username} - Status Code: {response.status_code}")
        return {"error": "Could not register user"}, response.status_code

    @staticmethod
    def get_admin_token():
        """
        Retrieves an admin token from Keycloak.

        Returns:
            dict or tuple: The admin token if successful, or an error message with status code.
        """
        url = f"{Config.KEYCLOAK_SERVER_URL}/realms/master/protocol/openid-connect/token"
        data = {
            "client_id": Config.KEYCLOAK_ADMIN_CLIENT_ID,
            "grant_type": "password",
            "username": Config.KEYCLOAK_ADMIN_USERNAME,
            "password": Config.KEYCLOAK_ADMIN_PASSWORD
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        logger.info("Requesting admin token from Keycloak")

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            logger.info("Admin token retrieved successfully")
            return response.json()

        logger.error("Failed to obtain admin token from Keycloak")
        return {"error": "Could not get admin token"}, 500