# Project Progress

- [x] Initialized project repository and Python 3.12 environment (`uv`, `pyproject.toml`)
- [x] Configured `.gitignore` for Python, secrets (.env), datasets, database storage, and logs
- [x] Set up centralized application logger (`core/logger.py`)
- [x] Implemented custom exception handler with traceback tracking (`core/exception.py`)
- [x] Configured Docker Compose for Qdrant and PostgreSQL (`docker-compose.yml`)
- [x] Organized Supreme Court judgments dataset (1950–2025) and added PDF filename sanitizer (`data/supreme_court_judgments/script.py`)
- [x] Tested PDF text extraction using PyMuPDF and explored metadata schema (`experiements/exp1.ipynb`)
- [x] Documented judgment structure and metadata layout (`DOCUMENT_STRUCTURE.md`)
- [x] Created architectural decision log with Qdrant storage rationale (`decisions.md`)
- [x] Added database configuration (`config/db_urls.yaml`) and YAML loader (`core/utils.py`)
- [ ] **(In Progress)** Setting up Qdrant vector database connection and configuration (`vector_store/vector_db.py`)
