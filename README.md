# RTI Assistant AI

AI-powered CivicTech assistant built for RTI (Right to Information) guidance and draft generation.

## Features

- AI-based RTI question answering
- Retrieval-Augmented Generation (RAG)
- RTI draft generator
- Source PDF access
- Suggested questions
- Streamlit frontend

## Tech Stack

- Frontend: Streamlit
- Backend: Python, LangChain, HuggingFace, FAISS

## Setup

Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Build the vector store:

```bash
python ingest.py
```

## Testing and Quality

The project uses pytest with coverage reporting and an enforced coverage threshold above 50%.

```bash
pytest
pytest --cov=. --cov-report=term-missing --cov-report=xml --cov-report=html --cov-fail-under=51
coverage report
coverage xml
coverage html
ruff check .
black --check .
mypy app.py ingest.py
bandit -r app.py ingest.py -ll
pip-audit -r requirements.txt
```

Equivalent shortcuts are available through `make test`, `make coverage-report`, `make lint`,
`make type-check`, `make audit`, and `make security`.

## Security

- Secret scanning: Gitleaks pre-commit hook
- Static analysis: Bandit
- Dependency audit: pip-audit for Python dependencies
- Dependency and quality gates: local pre-commit hooks

## Project Structure

```text
rti-assistant/
|-- app.py
|-- ingest.py
|-- requirements.txt
|-- README.md
|-- data/
|-- vectorstore/
|-- assets/
`-- tests/
```

## License

This project is licensed under the MIT License.
