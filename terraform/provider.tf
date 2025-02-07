terraform {
  required_providers {
    keycloak = {
      source  = "mrparkers/keycloak"
      version = "4.4.0"
    }
  }
}

provider "keycloak" {
  client_id     = var.client_id
  username      = var.username
  password      = var.password
  url           = var.idp_url
}