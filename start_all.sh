#!/bin/bash
# Start the backend
cd backend
source venv/Scripts/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Start the frontend
cd ../frontend
ng serve