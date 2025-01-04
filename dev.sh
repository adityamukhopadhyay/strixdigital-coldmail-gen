#!/bin/bash

# Start the Python backend server
cd backend && uvicorn app.main:app --reload --port 8000 &

# Wait a moment for the backend to start
sleep 2

# Return to the root directory and start the frontend
cd .. && npm run dev 