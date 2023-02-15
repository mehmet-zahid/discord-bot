build:
    docker compose up --build -d --remove-orphans
rebuild:
	docker system prune -a -f
	docker compose up -d
up:
    docker compose up -d
down:
    docker compose down
show_logs:
    docker compose logs