# Adding a New State

This guide walks through adding a new state data source to Abril Care Data.

## Overview

Each state has different data sources and access methods:

| State | Data Source | Access Method | Difficulty |
|-------|-------------|---------------|------------|
| NYC | NYC Open Data | REST API (Socrata) | Easy |
| DC | OSSE | Monthly PDF | Easy |
| Maryland | CheckCCMD | Web scraping | Medium |
| Virginia | VDOE | Form scraping | Medium |
| Texas | TX3C | REST API | Easy |
| California | CalSAWS | Complex | Hard |

## Step 1: Research the Data Source

Before coding, understand:

1. **Where is the data?**
   - State licensing agency website
   - Open data portal
   - Search tool

2. **What format?**
   - API (best)
   - Downloadable CSV/Excel
   - PDF reports
   - Web search only (requires scraping)

3. **What fields are available?**
   - Provider name, address, phone
   - License number and status
   - Capacity
   - Inspection history

4. **Update frequency?**
   - Real-time
   - Daily
   - Monthly

5. **Any rate limits or access restrictions?**

## Step 2: Create the Extractor

Create a new file in `src/extractors/`:

```python
# src/extractors/xx_agency.py

"""
[State] [Agency] Childcare Data Extractor.

Data source: [URL]
Access method: [API/scraping/PDF]
"""

import logging
from typing import List, Optional
from datetime import datetime

from src.schema import Provider, License, Location, Capacity, Contact

logger = logging.getLogger(__name__)


class XXExtractor:
    """Extractor for [State] [Agency] provider data."""

    def __init__(self):
        self.source = "xx_agency"  # Unique identifier
        self.source_url = "https://..."

    def extract(self, limit: Optional[int] = None) -> List[Provider]:
        """
        Fetch all providers from the source.

        Args:
            limit: Optional limit on number of records

        Returns:
            List of Provider objects
        """
        logger.info(f"Fetching providers from {self.source}...")

        raw_data = self._fetch_data(limit)

        providers = []
        for record in raw_data:
            try:
                provider = self._transform(record)
                providers.append(provider)
            except Exception as e:
                logger.warning(f"Failed to transform record: {e}")

        logger.info(f"Extracted {len(providers)} providers")
        return providers

    def _fetch_data(self, limit: Optional[int] = None) -> List[dict]:
        """
        Fetch raw data from source.

        Implement based on access method:
        - API: Use httpx or requests
        - Scraping: Use BeautifulSoup or Playwright
        - PDF: Use tabula-py or pdfplumber
        """
        raise NotImplementedError

    def _transform(self, record: dict) -> Provider:
        """Transform raw record to unified schema."""

        # Map source fields to schema
        return Provider(
            id=f"{self.source}-{record['id']}",
            source_id=str(record['id']),
            source=self.source,
            name=record['name'],
            type=self._map_type(record.get('type')),
            license=License(
                number=record['license_number'],
                type=self._map_license_type(record.get('license_type')),
                status=self._map_status(record.get('status')),
            ),
            location=Location(
                address_line1=record['address'],
                city=record['city'],
                state="XX",  # Two-letter state code
                zip_code=record['zip'],
            ),
            # ... map remaining fields
            updated_at=datetime.utcnow(),
        )

    def _map_type(self, source_type: str) -> str:
        """Map source provider type to schema type."""
        mapping = {
            "Center": "childcare_center",
            "Family Home": "family_childcare",
            # Add mappings for this source
        }
        return mapping.get(source_type, "childcare_center")

    def _map_status(self, source_status: str) -> str:
        """Map source license status to schema status."""
        mapping = {
            "Open": "active",
            "Active": "active",
            "Closed": "inactive",
            "Suspended": "suspended",
            # Add mappings for this source
        }
        return mapping.get(source_status, "active")
```

## Step 3: Add Tests

Create tests in `tests/extractors/`:

```python
# tests/extractors/test_xx_agency.py

import pytest
from src.extractors.xx_agency import XXExtractor


class TestXXExtractor:
    def test_transform_valid_record(self):
        """Test transforming a valid record."""
        extractor = XXExtractor()
        record = {
            "id": "12345",
            "name": "Test Provider",
            # ... sample record
        }
        provider = extractor._transform(record)

        assert provider.id == "xx_agency-12345"
        assert provider.name == "Test Provider"
        assert provider.source == "xx_agency"

    def test_extract_live(self):
        """Test fetching live data (integration test)."""
        extractor = XXExtractor()
        providers = extractor.extract(limit=10)

        assert len(providers) <= 10
        for provider in providers:
            assert provider.name
            assert provider.location.state == "XX"
```

## Step 4: Register the Extractor

Add to `src/extractors/__init__.py`:

```python
from .xx_agency import XXExtractor

__all__ = ["NYCExtractor", "XXExtractor"]
```

## Step 5: Document

Update:

1. **README.md** - Add to "Available Data" table
2. **docs/schema.md** - Add source mapping reference
3. **Extractor docstring** - Include data source URL and notes

## Examples by Access Method

### API (easiest)

See `src/extractors/nyc_dohmh.py` for a Socrata API example.

```python
from sodapy import Socrata

client = Socrata("data.cityofnewyork.us", app_token)
results = client.get("dataset-id", limit=50000)
```

### PDF Parsing

```python
import tabula

tables = tabula.read_pdf(url, pages='all')
df = pd.concat(tables)
```

### Web Scraping

```python
import httpx
from bs4 import BeautifulSoup

response = httpx.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
rows = soup.select('table.results tr')
```

### Form Scraping (with JavaScript)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.fill('#search-input', 'query')
    page.click('#submit')
    # ... extract results
```

## Best Practices

1. **Be respectful** - Add delays between requests
2. **Cache responses** - Don't re-fetch unchanged data
3. **Handle errors gracefully** - Log and skip bad records
4. **Test with small limits first** - Use `limit=10` during development
5. **Document source quirks** - Note any unusual field mappings

## Need Help?

- Open an issue with the state you want to add
- Check existing extractors for patterns
- Ask in GitHub Discussions
