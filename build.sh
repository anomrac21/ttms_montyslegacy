#!/bin/bash

# Initialize and update submodules
echo "Initializing submodules..."
git submodule update --init --recursive

# Pull latest from theme's master branch
echo "Pulling latest theme from master branch..."
cd themes/_menus_ttms
git checkout master
git pull origin master
cd ../..

# Register client site with auth-service (if not exists)
echo "Registering client site with auth-service..."
bash scripts/register-client.sh

# Build the Hugo site with optimization
echo "Running Hugo build with minification..."
hugo --gc --minify
