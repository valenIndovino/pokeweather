from openmeteo_requests import Client
import requests

# Mapeo de umbrales de temperatura y el tipo de Pokémon más fuerte en esas condiciones
TEMPERATURE_TO_POKEMON_TYPE = {
    "fire": lambda temp: temp >= 30,  # Si la temperatura es mayor o igual a 30°C → Pokémon de tipo Fuego
    "ground": lambda temp: 20 <= temp < 30,  # Entre 20°C y 30°C → Pokémon de tipo Tierra
    "normal": lambda temp: 10 <= temp < 20,  # Entre 10°C y 20°C → Pokémon de tipo Normal
    "water": lambda temp: 0 <= temp < 10,  # Entre 0°C y 10°C → Pokémon de tipo Agua
    "ice": lambda temp: temp < 0  # Menos de 0°C → Pokémon de tipo Hielo
}

def get_temperature(city: str) -> float or None:
    """
    Obtiene la temperatura actual de una ciudad usando Open-Meteo.

    Pasos:
    1. Obtiene la latitud y longitud de la ciudad usando la API de geocodificación de Open-Meteo.
    2. Utiliza las coordenadas obtenidas para consultar la temperatura actual en Open-Meteo.

    Args:
        city (str): Nombre de la ciudad a consultar.

    Returns:
        float: Temperatura actual en grados Celsius si la consulta es exitosa.
        None: Si la API no responde correctamente o la ciudad no es encontrada.
    """
    client = Client()

    # Obtener latitud y longitud de la ciudad con Open-Meteo Geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_response = requests.get(geo_url)

    if geo_response.status_code != 200 or "results" not in geo_response.json():
        return None  # Si la ciudad no se encuentra o hay un error en la API

    # Extraer coordenadas de la primera coincidencia
    location = geo_response.json()["results"][0]
    lat, lon = location["latitude"], location["longitude"]

    # Hacer la solicitud a Open-Meteo para obtener la temperatura actual
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m&timezone=auto"
    response = requests.get(url)

    if response.status_code != 200:
        return None  # Si hay un error en la respuesta de la API

    # Extraer la temperatura actual en grados Celsius
    return response.json()["current"]["temperature_2m"]

def get_strongest_pokemon_type_by_temperature(city: str) -> str or None:
    """
    Determina el tipo de Pokémon más fuerte basado en la temperatura actual de una ciudad.

    Pasos:
    1. Obtiene la temperatura actual de la ciudad mediante `get_temperature(city)`.
    2. Determina el tipo de Pokémon más fuerte basado en los umbrales de temperatura predefinidos.

    Args:
        city (str): Nombre de la ciudad para la consulta.

    Returns:
        str: Tipo de Pokémon más fuerte según la temperatura.
        None: Si no se pudo obtener la temperatura.
    """
    temperature = get_temperature(city)
    if temperature is None:
        return None  # No se pudo obtener la temperatura

    # Determinar el tipo de Pokémon basado en la temperatura
    for pokemon_type, condition in TEMPERATURE_TO_POKEMON_TYPE.items():
        if condition(temperature):
            return pokemon_type

    return "normal"  # Valor por defecto si no se encuentra coincidencia en la temperatura
