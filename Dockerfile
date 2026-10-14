# ==========================================================
# Dockerfile Mẫu Chuẩn Cho Dự Án Dự Thi (Competition Docker)
# ==========================================================

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Cài đặt các gói phụ thuộc hệ thống cơ bản
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Sao chép mã nguồn dự án vào container
COPY . /app

# Cấp quyền thực thi cho start script nếu có
RUN chmod +x /app/start.sh

# Cổng mặc định
EXPOSE 8000
EXPOSE 8501

CMD ["/app/start.sh"]
