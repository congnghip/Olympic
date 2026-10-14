#!/bin/bash

# Start FastAPI backend on port 8000
echo "Starting FastAPI backend on port 8000..."
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit analytics frontend on port 8501
echo "Starting Streamlit frontend on port 8501..."
cd /app/streamlit
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
