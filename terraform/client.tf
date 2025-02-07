resource "keycloak_openid_client" "flask_client" {
  realm_id  = keycloak_realm.pokeweather.id
  client_id = "flask-client"
  name      = "Flask API Client"
  enabled   = true

  access_type = "PUBLIC"
  standard_flow_enabled = true
  direct_access_grants_enabled = true
  valid_redirect_uris = [
    "http://localhost:5001/*"
  ]
}