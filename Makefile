BLACK := black --check .
FLAKE8 := flake8 .
VENV := venv

# Build the Docker image
.PHONY: build
build:
	docker build -t tic-tac-toe-game .

# Run the Docker container
.PHONY: docker_run
docker_run:
	docker run -d -p 8000:8000 tic-tac-toe-game

# Use Docker Compose to build and run the container
.PHONY: compose_up
compose_up:
	docker-compose up -d

# Use Docker Compose to stop and remove the container
.PHONY: compose_down
compose_down:
	docker-compose down

.PHONY: prune
prune:
	docker system prune -a

.PHONY: lint
lint:
	$(BLACK)
	$(FLAKE8)

.PHONY: flake8
flake8:
	flake8 .

.PHONY: black
black:
	black .

.PHONY: venv
venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV)

# Run the FastAPI application
.PHONY: run
run:
	PYTHONPATH=$(pwd) uvicorn games.api:app --reload
