BLACK := black --check .
FLAKE8 := flake8 .
VENV := venv

# Build the Docker image
.PHONY: build
build:
	docker-compose up --build -d

.PHONY: down
down:
	docker compose down

.PHONY: prune
prune:
	docker system prune -a

.PHONY: lint
lint: venv
	$(VENV)/bin/$(BLACK)
	$(VENV)/bin/$(FLAKE8)

.PHONY: format
format: venv
	$(VENV)/bin/black .

.PHONY: flake8
flake8: venv
	$(VENV)/bin/$(FLAKE8)

.PHONY: black
black: venv
	$(VENV)/bin/$(BLACK)

.PHONY: venv
venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV)
