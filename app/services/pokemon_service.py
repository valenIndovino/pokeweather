import requests
import random
import logging
from app.utils.weather import get_strongest_pokemon_type_by_temperature, get_temperature

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

POKEAPI_URL = "https://pokeapi.co/api/v2"

def get_pokemon_type(name: str):
    """
    Obtiene el tipo de un Pokémon según su nombre desde PokéAPI.

    Args:
        name (str): Nombre del Pokémon.

    Returns:
        dict: Información del Pokémon con su tipo o un mensaje de error.
    """
    logger.info(f"Getting pokemon type by name, processing the {name} one.")

    response = requests.get(f"{POKEAPI_URL}/pokemon/{name.lower()}")

    if response.status_code != 200:
        logger.error("No pokemon found according that name.")
        return {"error": "Pokémon not found"}, 404
    
    logger.info("Pokemon type successfully obtained.")

    data = response.json()
    types = [t["type"]["name"] for t in data["types"]]

    return {"pokemon": name, "types": types}

def get_random_pokemon_by_type(type_name: str):
    """
    Obtiene un Pokémon aleatorio de un tipo específico desde PokéAPI.

    Args:
        type_name (str): Tipo del Pokémon (ejemplo: "fire", "water").

    Returns:
        dict: Nombre del Pokémon aleatorio de ese tipo o un mensaje de error.
    """
    logger.info(f"Getting a random pokemon by type, processing the {type_name} type.")

    response = requests.get(f"{POKEAPI_URL}/type/{type_name.lower()}")

    if response.status_code != 200:
        logger.error("Type not found.")
        return {"error": "Type not found"}, 404

    data = response.json()
    if not data["pokemon"]:
        return {"error": "No Pokémon found for this type"}, 404

    logger.info(f"Successfully retrived random pokemon by {type_name} type")

    random_pokemon = random.choice(data["pokemon"])["pokemon"]["name"]
    return {"type": type_name, "random_pokemon": random_pokemon}

def get_longest_name_pokemon(type_name: str):
    """
    Obtiene el Pokémon con el nombre más largo de un tipo específico desde PokéAPI.

    Args:
        type_name (str): Tipo del Pokémon.

    Returns:
        dict: Pokémon con el nombre más largo de ese tipo o un mensaje de error.
    """
    logger.info(f"Getting the pokemon with the largest name by {type_name} type.")

    response = requests.get(f"{POKEAPI_URL}/type/{type_name.lower()}")

    if response.status_code != 200:
        logger.error("Type not found")
        return {"error": "Type not found"}, 404

    data = response.json()
    if not data["pokemon"]:
        logger.error("No pokemon found for this type.")
        return {"error": "No Pokémon found for this type"}, 404

    logger.info(f"Successfully retrieved the pokemon with the largest name by {type_name} type.")

    longest_pokemon = max(data["pokemon"], key=lambda p: len(p["pokemon"]["name"]))
    return {"type": type_name, "longest_name_pokemon": longest_pokemon["pokemon"]["name"]}

def get_random_pokemon_by_weather(city: str):
    """
    Obtiene un Pokémon aleatorio que contenga 'I', 'A' o 'M' en su nombre y 
    sea del tipo más fuerte según la temperatura de la ciudad.

    Args:
        city (str): Nombre de la ciudad.

    Returns:
        dict: Pokémon aleatorio del tipo más fuerte según el clima o un mensaje de error.
    """
    logger.info(f"Getting a random but strongest pokemon regarding the weather in {city} and it's type.")

    strongest_type = get_strongest_pokemon_type_by_temperature(city)
    if not strongest_type:
        logger.error("Error founding the type for that city/temperature.")
        return {"error": "Could not determine type"}, 400

    logger.info(f"Getting a random pokemon with type {strongest_type}")

    response = requests.get(f"{POKEAPI_URL}/type/{strongest_type}")

    if response.status_code != 200:
        logger.error(f"The type {strongest_type} is no longer exists.")
        return {"error": "Type not found"}, 404

    data = response.json()
    if not data["pokemon"]:
        logger.error(f"There is not a pokemon with the type {strongest_type}.")
        return {"error": "No Pokémon found for this type"}, 404

    # Filtrar Pokémon que contengan 'I', 'A' o 'M' en su nombre
    matching_pokemon = [p["pokemon"]["name"] for p in data["pokemon"]
                        if any(letter in p["pokemon"]["name"].upper() for letter in "IAM")]

    if matching_pokemon:
        logger.info("Successfully retrieved a pokemon matching 'I' or 'A' or 'M' inside his name")

        return {
            "city": city,
            "temperature": get_temperature(city),
            "type": strongest_type,
            "random_pokemon": random.choice(matching_pokemon)
        }
    
    logger.error(f"No matching pokemon found with 'I' or 'A' or 'M' inside his name.")

    return {"error": "No matching Pokémon found"}, 404