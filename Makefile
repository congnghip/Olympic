# ==============================================================================
# DX-OS OPEN-CORE AUTOMATION MAKEFILE
# ==============================================================================

.PHONY: help up down restart logs ps clean seed dev-backend dev-frontend

help:
	@echo "Các lệnh điều khiển hệ sinh thái DX-OS Open-Core:"
	@echo "  make up           Khởi động toàn bộ cụm dịch vụ (Docker Compose)"
	@echo "  make down         Dừng toàn bộ hệ thống"
	@echo "  make restart      Khởi động lại toàn bộ dịch vụ"
	@echo "  make logs         Xem logs của toàn bộ hệ thống"
	@echo "  make ps           Kiểm tra trạng thái các container"
	@echo "  make clean        Dọn dẹp volume và container"
	@echo "  make dev-backend  Chạy Backend FastAPI cục bộ bằng Python"
	@echo "  make dev-frontend Chạy Frontend Web Portal cục bộ bằng npm"

up:
	docker compose up -d --build

down:
	docker compose down

restart:
	docker compose down && docker compose up -d

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down -v --remove-orphans

dev-backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && npm install && npm run dev
