resource "keycloak_realm" "pokeweather" {
  realm        = "pokeweather"
  enabled      = true
  display_name = "Pokémon Weather API"
}

resource "keycloak_required_action" "verify_email" {
  realm_id = keycloak_realm.pokeweather.realm
  alias    = "VERIFY_EMAIL"
  enabled  = false
  name     = "Verify Email"
}

resource "keycloak_required_action" "verify_profile" {
  realm_id = keycloak_realm.pokeweather.realm
  alias    = "VERIFY_PROFILE"
  enabled  = false
  name     = "Verify Profile"
}