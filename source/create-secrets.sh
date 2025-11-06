#!/bin/bash
set -e

# Directory to store temporary secret files
mkdir -p secrets

# Keycloak admin credentials
echo -n "admin" > secrets/keycloak_admin_user.txt
echo -n "StrongAdminPassword!" > secrets/keycloak_admin_pass.txt

# PostgreSQL password
echo -n "StrongDBPassword!" > secrets/postgres_password.txt

# Tyk secret
echo -n "SuperSecretTykKey!" > secrets/tyk_secret.txt

echo "✅ All Docker secrets created successfully!"
