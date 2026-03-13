# Contributing to Abril Care Data

Thank you for your interest in contributing! This project aims to make care provider data accessible to everyone.

## Ways to Contribute

### 1. Add a New State

The highest-impact contribution is adding data from a new state. Each state has different data sources and access methods.

**See:** [docs/adding-a-state.md](docs/adding-a-state.md)

**Current needs:**
- Maryland (CheckCCMD scraping)
- Virginia (VDOE scraping)
- Texas (TX3C API)
- California (CalSAWS)

### 2. Improve Data Quality

- Fix geocoding errors
- Improve address parsing
- Add deduplication logic
- Validate phone numbers/emails

### 3. Build Integrations

- FHIR export for healthcare interoperability
- Google Sheets connector
- Airtable sync
- Webhook notifications

### 4. Documentation

- Improve README clarity
- Add examples and tutorials
- Document edge cases

### 5. Report Issues

Found a bug or have an idea? [Open an issue](https://github.com/abril-care/abril-care-data/issues/new).

---

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (optional, for full API)
- Docker (optional, for containerized setup)

### Quick Start

```bash
# Clone the repo
git clone https://github.com/abril-care/abril-care-data.git
cd abril-care-data

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

### Running the API Locally

```bash
# Start PostgreSQL (if using Docker)
docker-compose up -d db

# Run migrations
alembic upgrade head

# Start the API
uvicorn src.api.main:app --reload
```

---

## Code Style

- **Python:** Follow PEP 8, enforced by Ruff
- **Type hints:** Required for all public functions
- **Docstrings:** Google style
- **Tests:** Required for new features

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Hooks run automatically on commit
```

---

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/add-texas-extractor`)
3. **Make your changes** with tests
4. **Run the test suite** (`pytest`)
5. **Run linting** (`ruff check . && ruff format .`)
6. **Submit a PR** with a clear description

### PR Guidelines

- Keep PRs focused on a single change
- Include tests for new functionality
- Update documentation if needed
- Reference any related issues

---

## Adding a New State Extractor

State extractors live in `src/extractors/`. Each extractor:

1. Fetches data from the state source (API, scraping, or PDF)
2. Transforms to the unified schema
3. Returns a list of `Provider` objects

### Template

```python
# src/extractors/xx_agency.py

from src.schema import Provider
from typing import List

class XXExtractor:
    """Extractor for [State] [Agency] provider data."""

    def __init__(self):
        self.source_id = "xx_agency"
        self.source_url = "https://..."

    def extract(self) -> List[Provider]:
        """Fetch and parse all providers."""
        raw_data = self._fetch_data()
        return [self._transform(record) for record in raw_data]

    def _fetch_data(self):
        """Fetch raw data from source."""
        # API call, web scraping, or PDF parsing
        pass

    def _transform(self, record: dict) -> Provider:
        """Transform raw record to Provider schema."""
        return Provider(
            source_id=f"{self.source_id}-{record['id']}",
            name=record['name'],
            # ... map all fields
        )
```

### Testing Your Extractor

```bash
# Run extractor tests
pytest tests/extractors/test_xx_agency.py -v

# Test against live data (be respectful of rate limits)
python -m src.extractors.xx_agency --test
```

---

## Data Sources

### Public Data (Preferred)

- Open Data portals (NYC, state data.gov sites)
- Published PDFs from licensing agencies
- FOIA-requested datasets

### Web Scraping (When Necessary)

If scraping:
- Respect `robots.txt`
- Add delays between requests (1-2 seconds minimum)
- Cache responses to avoid redundant fetches
- Include a User-Agent identifying this project

---

## Community

- **Discussions:** [GitHub Discussions](https://github.com/abril-care/abril-care-data/discussions)
- **Issues:** [GitHub Issues](https://github.com/abril-care/abril-care-data/issues)

---

## Code of Conduct

Be kind. Be respectful. We're all here to help families find care.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
