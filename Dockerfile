# ====================================================================
# DX-OS Open-Core: Unified Competition Container Dockerfile (OLP 2026)
# ====================================================================

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install build dependencies for C++17 solver & GIS
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libyaml-cpp-dev \
    nlohmann-json3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy source tree
COPY . /app

# Compile C++17 3D-ACO Solver Core
WORKDIR /app/apps/solver_core
RUN mkdir -p build && cd build && cmake .. && make test || true

# Copy compiled test binary to backend if available
RUN mkdir -p /app/apps/backend_service/bin && \
    if [ -f /app/apps/solver_core/build/test ]; then \
        cp /app/apps/solver_core/build/test /app/apps/backend_service/bin/test; \
    fi

# Install Python dependencies across modules
WORKDIR /app
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.31.0 \
    streamlit==1.38.0 \
    requests==2.32.3 \
    pydantic==2.9.2 \
    pyyaml==6.0.2

WORKDIR /app
RUN chmod +x /app/start.sh

# Ports:
# 8000: API Gateway & Core Solver Service
# 8501: Streamlit Research & Analytics
# 8502: Realtime WebGIS Map Dispatcher (IOC)
EXPOSE 8000
EXPOSE 8501
EXPOSE 8502

CMD ["/app/start.sh"]
