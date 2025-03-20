#!/bin/bash
echo "Building and deploying fraud detection system..."
docker-compose up -d

# Wait for the database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Generate sample data (if needed)
echo "Generating sample data..."
docker-compose exec backend python generate_sample_data.py

echo "Deployment complete! Access the application at http://localhost"