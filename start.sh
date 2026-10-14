#!/bin/bash
set -e

echo "=== Khởi động ứng dụng dự thi Olympic ==="
echo "Dịch vụ đang sẵn sàng phục vụ tại các cổng chỉ định..."

# Ví dụ lệnh khởi động dịch vụ của bạn (chỉnh sửa tùy theo framework sử dụng):
# python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 &
# streamlit run src/app.py --server.port 8501 &

# Giữ tiến trình chạy nền:
tail -f /dev/null
