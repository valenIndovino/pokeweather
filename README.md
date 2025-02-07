# Pokemon Weather API

Si no estás interesado en leer un README...
Simplemente ejecuta `docker compose up -d --build`, espera unos minutos hasta que todo levante y puedes revisar la interfaz de Swagger UI ubicada en [http://localhost:5002](http://localhost:5002), donde puedes probar todos los endpoints de manera interactiva.
¡Sí, ni siquiera necesitas Postman o cURL! 😆

## Introducción
Este proyecto es una API RESTful construida con **Flask**, diseñada como parte de un desafío técnico. La API proporciona datos relacionados con Pokémon basados en las condiciones climáticas y la autenticación de usuarios.

## Endpoints
✅ **Gestión de usuarios y access tokens en Keycloak 24** registración y login usando el flujo Resource Owner Passoword Credentials (ROPC)
✅ **Recuperar el tipo de un Pokémon** basado en su nombre.  
✅ **Obtener un Pokémon aleatorio** de un tipo específico.  
✅ **Encontrar el Pokémon con el nombre más largo** de un tipo dado.  
✅ **Obtener un Pokémon basado en el clima de la ciudad** (por ejemplo, 29°C en Buenos Aires devuelve un Pokémon de tipo Tierra).

## 🛠️ Instalación y Configuración

### 🔹 1. Clonar el repositorio:

```sh
git clone https://github.com/valenIndovino/pokeweather.git
cd pokeweather
```

### 🔹 2. Crear archivo .env en raíz con las siguientes variables:

```sh
# keycloak_idp_information
KEYCLOAK_SERVER_URL = "http://keycloak:8080"
KEYCLOAK_REALM = "pokeweather"
KEYCLOAK_CLIENT_ID = "flask-client"
KEYCLOAK_ADMIN_USERNAME = "admin"
KEYCLOAK_ADMIN_PASSWORD = "admin"
KEYCLOAK_ADMIN_CLIENT_ID = "admin-cli"
```

### 🔹 3. Levantar compose.yaml y buildear Dockerfile:

```sh
docker compose up -d --build
```

### 🔹 4. Revisar que el contenedor terrafom-keycloak se haya ejecutado y terminado bien:

```sh
docker logs terraform-keycloak
# Mensaje esperado: Terraform aplicado con éxito. Toda la configuración la puedes ver impactada a través de la consola administrativa.
```

### 🔹 5. Navegar el Swagger y probar los endpoints:

Ir a -> http://localhost:5002

### Opcional: KEYCLOAK ###

En caso de que desees, puedes visitar la consola administrativa de Keycloak:
Ir a -> http://localhost:8080 (admin/admin)