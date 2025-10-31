#!/bin/bash

# Script to register client site with auth-service if it doesn't exist
# This should be run during the build/deployment process

set -e

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HUGO_CONFIG="$PROJECT_ROOT/hugo.toml"

# Check if hugo.toml exists
if [ ! -f "$HUGO_CONFIG" ]; then
  echo "❌ Error: hugo.toml not found at $HUGO_CONFIG"
  exit 1
fi

echo "📖 Reading configuration from hugo.toml..."

# Extract configuration from hugo.toml
CLIENT_ID=$(grep -oP "clientId\s*=\s*\"\K[^\"]*" "$HUGO_CONFIG" | head -1)
DOMAIN=$(grep -oP "baseURL\s*=\s*'https?://\K[^/']*" "$HUGO_CONFIG")
NAME=$(grep -oP "title\s*=\s*'\K[^']*" "$HUGO_CONFIG")
DESCRIPTION="Client site for $NAME"

# Validate extracted values
if [ -z "$CLIENT_ID" ]; then
  echo "❌ Error: Could not extract clientId from hugo.toml"
  exit 1
fi

if [ -z "$DOMAIN" ]; then
  echo "❌ Error: Could not extract domain from baseURL in hugo.toml"
  exit 1
fi

if [ -z "$NAME" ]; then
  echo "❌ Error: Could not extract title from hugo.toml"
  exit 1
fi

echo "   Client ID: $CLIENT_ID"
echo "   Domain: $DOMAIN"
echo "   Name: $NAME"

# Auth service configuration
AUTH_SERVICE_POD="deployment/auth-service-postgresql"
AUTH_NAMESPACE="auth-service"
DB_USER="postgres"
DB_NAME="authdb"

echo "🔍 Checking if client site '$CLIENT_ID' exists in auth-service..."

# Check if client site exists
CLIENT_EXISTS=$(kubectl exec $AUTH_SERVICE_POD -n $AUTH_NAMESPACE -- \
  psql -U $DB_USER -d $DB_NAME -tAc \
  "SELECT COUNT(*) FROM client_sites WHERE client_id = '$CLIENT_ID';")

if [ "$CLIENT_EXISTS" -gt 0 ]; then
  echo "✅ Client site '$CLIENT_ID' already exists. Skipping creation."
  echo "   Domain: $DOMAIN"
  
  # Show existing client info
  kubectl exec $AUTH_SERVICE_POD -n $AUTH_NAMESPACE -- \
    psql -U $DB_USER -d $DB_NAME -c \
    "SELECT id, client_id, domain, name, is_active FROM client_sites WHERE client_id = '$CLIENT_ID';"
else
  echo "📝 Client site '$CLIENT_ID' does not exist. Creating..."
  
  # Create client site
  kubectl exec $AUTH_SERVICE_POD -n $AUTH_NAMESPACE -- \
    psql -U $DB_USER -d $DB_NAME -c \
    "INSERT INTO client_sites (created_at, updated_at, client_id, domain, name, description, is_active) 
     VALUES (NOW(), NOW(), '$CLIENT_ID', '$DOMAIN', '$NAME', '$DESCRIPTION', true);"
  
  echo "✅ Client site '$CLIENT_ID' created successfully!"
  echo "   Domain: $DOMAIN"
  echo "   Name: $NAME"
fi

echo ""
echo "🎉 Client registration complete!"

