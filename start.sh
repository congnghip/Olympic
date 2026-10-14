#!/bin/bash
set -e

echo "=========================================================="
echo "🚀 DX-OS Open-Core Platform (OLP 2026 Competition Edition)"
echo "=========================================================="

# 1. Khởi động API Gateway & Solver Backend trên cổng 8000
echo "[1/3] Khởi động API Gateway & Core Solver Service (Port 8000)..."
cd /app/apps/backend_service
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 2. Khởi động Giao diện Phân tích Streamlit trên cổng 8501
echo "[2/3] Khởi động Streamlit Analytics & Research Dashboard (Port 8501)..."
cd /app/apps/analytics
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 &

# 3. Khởi động Trung tâm Điều hành WebGIS IOC (Dual Map) trên cổng 8502
echo "[3/3] Khởi động WebGIS Realtime Dispatcher IOC (Port 8502)..."
cd /app/apps/map_dispatcher
uvicorn server:app --host 0.0.0.0 --port 8502 &

echo "=========================================================="
echo "✅ Tất cả các dịch vụ đã sẵn sàng!"
echo "📍 WebGIS Dispatcher (Trọng tâm chấm thi): http://localhost:8502"
echo "📍 Streamlit Analytics:                  http://localhost:8501"
echo "📍 Swagger API Documentation:            http://localhost:8000/docs"
echo "=========================================================="

wait -n
exit $?
