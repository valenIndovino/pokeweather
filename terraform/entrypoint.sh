#!/bin/sh

echo "Esperando a que Keycloak esté listo..."
sleep 60

echo "Ejecutando Terraform..."
terraform init
terraform apply -auto-approve

echo "Terraform aplicado con éxito. Toda la configuración la puedes ver impactada a través de la consola administrativa."