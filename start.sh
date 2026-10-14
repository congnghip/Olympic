#!/bin/bash
set -e

echo "Starting Backend API on port 8000..."
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit Analytics Dashboard on port 8501..."
cd /app/streamlit
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 &

echo "Starting WebGIS Real-time Map Dispatcher on port 8502..."
cd /app/map_ui
uvicorn server:app --host 0.0.0.0 --port 8502 &

wait -n
exit $?
