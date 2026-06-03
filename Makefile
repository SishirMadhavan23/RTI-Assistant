.PHONY: install lint format type-check test coverage-report audit dependency-audit security pre-commit-check

install:
	pip install -r requirements.txt

lint:
	ruff check .
	flake8 --config=.flake8 .
	pylint --errors-only --rcfile=pyproject.toml tests
	vulture app.py ingest.py tests --min-confidence=80
	black --check .

format:
	ruff check . --fix
	pyupgrade --py311-plus --exit-zero-even-if-changed app.py ingest.py tests/*.py
	black .

type-check:
	mypy --follow-imports=skip app.py ingest.py

test:
	pytest

coverage-report:
	pytest --cov=. --cov-report=term-missing --cov-report=xml --cov-report=html --cov-fail-under=51

audit:
	pip-audit -r requirements.txt

dependency-audit:
	pip-audit -r requirements.txt

security:
	bandit -r app.py ingest.py -ll
	semgrep --config=auto --error app.py ingest.py

pre-commit-check:
	pre-commit run --all-files
