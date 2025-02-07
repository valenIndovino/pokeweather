resource "keycloak_user" "ash" {
  realm_id = keycloak_realm.pokeweather.id
  username = "ash123"
  enabled  = true
  email    = "ash123@pokemon.com"
  first_name = "Ash"
  last_name  = "Ketchum"

  initial_password {
    value     = "pikachu123"
    temporary = false
  }

}