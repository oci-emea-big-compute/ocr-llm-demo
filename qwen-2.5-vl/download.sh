#!/bin/bash

# Create models directory with proper permissions
mkdir -p models
chmod 777 models

# Run the download script in the container
docker-compose run --rm qwen-vl-api python3 /app/download_model.py
