#!/bin/bash

# Start the service using docker-compose
docker compose up -d

# Show service status
docker compose ps

# Show logs
echo "Service started. To view logs, run: docker-compose logs -f" 