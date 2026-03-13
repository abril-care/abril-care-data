# Abril Care Data

**Open source infrastructure for care provider data.**

Aggregating childcare, elder care, and disability services data across the US into a unified, accessible API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## The Problem

Care data in the US is fragmented across:
- **50 state licensing systems** (each with different formats, access methods)
- **Proprietary platforms** (Care.com, Brightwheel, etc.)
- **Government silos** (CCDF, Medicaid HCBS, state subsidies)

Families can't find care. Researchers can't study access gaps. Developers can't build better tools.

## The Solution

An open data layer that:
1. **Aggregates** provider data from public state sources
2. **Normalizes** into a unified schema
3. **Exposes** via a simple API
4. **Updates** automatically

---

## Quick Start

```bash
# Install
pip install abril-care-data

# Search providers
from abril import providers

# Find childcare in DC
results = providers.search(
    state="DC",
    type="childcare",
    lat=38.9072,
    lng=-77.0369,
    radius_miles=5
)

for provider in results:
    print(f"{provider.name} - {provider.capacity} slots")
```

---

## Available Data

### Currently Live

| Region | Providers | Source | Updated |
|--------|-----------|--------|---------|
| **NYC** | ~12,000 | NYC Open Data (API) | Daily |
| **DC** | ~600 | OSSE (PDF) | Monthly |

### Coming Soon

| Region | Providers | Source | ETA |
|--------|-----------|--------|-----|
| **Maryland** | ~9,000 | CheckCCMD | April 2026 |
| **Virginia** | ~7,000 | VDOE | April 2026 |
| **Texas** | ~15,000 | TX3C | May 2026 |

---

## Data Schema

Every provider record includes:

```json
{
  "id": "nyc-dohmh-12345",
  "name": "Sunshine Child Care Center",
  "type": "childcare_center",
  "license": {
    "number": "DC-2024-1234",
    "status": "active",
    "expires": "2026-12-31"
  },
  "location": {
    "address": "123 Main St",
    "city": "Washington",
    "state": "DC",
    "zip": "20001",
    "coordinates": {
      "lat": 38.9072,
      "lng": -77.0369
    }
  },
  "capacity": {
    "total": 75,
    "infant": 10,
    "toddler": 20,
    "preschool": 30,
    "school_age": 15
  },
  "contact": {
    "phone": "(202) 555-1234",
    "email": "info@sunshine.example.com"
  },
  "accepts_subsidies": true,
  "quality_rating": "Level 4",
  "last_inspection": "2025-11-15",
  "source": "dc_osse",
  "updated_at": "2026-03-13T12:00:00Z"
}
```

See [docs/schema.md](docs/schema.md) for full specification.

---

## API Endpoints

### REST API

```bash
# Search providers
GET /api/v1/providers?state=DC&type=childcare&lat=38.9&lng=-77.0&radius=10

# Get provider by ID
GET /api/v1/providers/{id}

# Get provider inspections
GET /api/v1/providers/{id}/inspections

# Check subsidy eligibility
POST /api/v1/eligibility/check
```

### Self-Hosted

```bash
# Run locally
docker-compose up

# API available at http://localhost:8000
```

---

## Why Open Source?

Care data should be **public infrastructure**, not locked in proprietary platforms.

Open data enables:
- **Researchers** to study care access and outcomes
- **Policymakers** to see where subsidies are (and aren't) reaching families
- **Developers** to build tools without recreating data pipelines
- **Families** to find care without hitting paywalls

---

## Project Structure

```
abril-care-data/
├── src/
│   ├── extractors/           # State-specific data extractors
│   │   ├── nyc_dohmh.py      # NYC Open Data (API)
│   │   ├── dc_osse.py        # DC OSSE (PDF parsing)
│   │   ├── md_checkcc.py     # Maryland (web scraping)
│   │   └── va_vdoe.py        # Virginia (web scraping)
│   ├── transformers/         # Data cleaning & normalization
│   ├── schema/               # Pydantic models
│   └── api/                  # FastAPI application
├── data/
│   └── samples/              # Sample data for testing
├── docs/
│   ├── schema.md             # Data schema specification
│   ├── adding-a-state.md     # How to add a new state
│   └── architecture.md       # System design
├── tests/
├── docker-compose.yml
└── pyproject.toml
```

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Priority Areas

1. **Add more states** - Each state has different data sources. [Guide →](docs/adding-a-state.md)
2. **Improve data quality** - Geocoding, deduplication, validation
3. **Build integrations** - FHIR export, Google Sheets, Airtable

### Good First Issues

Look for issues tagged [`good first issue`](https://github.com/abril-care/abril-care-data/labels/good%20first%20issue).

---

## Roadmap

### Q2 2026
- [x] NYC data via Open Data API
- [x] DC data via OSSE PDF parsing
- [ ] Maryland data via CheckCCMD scraping
- [ ] Virginia data via VDOE scraping
- [ ] Public REST API

### Q3 2026
- [ ] Subsidy eligibility engine (CCDF calculator)
- [ ] Texas data (TX3C API)
- [ ] California data (CalSAWS)
- [ ] Provider availability tracking

### Q4 2026
- [ ] FHIR-compatible export
- [ ] Real-time availability via provider integrations
- [ ] Quality ratings integration (QRIS)

---

## Related Projects

- [NYC Open Data - Childcare Centers](https://data.cityofnewyork.us/Health/Childcare-Centers/tdif-34xu)
- [data.ny.gov - Child Care Regulated Programs](https://data.ny.gov/Human-Services/Child-Care-Regulated-Programs/cb42-qumz)
- [ChildCare Aware](https://www.childcareaware.org/) - National referral network

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Acknowledgments

Built with support from:
- NYC Open Data
- State licensing agencies
- The open source community

---

## Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/abril-care/abril-care-data/issues)
- **Discussions:** [Ask questions or share ideas](https://github.com/abril-care/abril-care-data/discussions)
- **Email:** [hello@abrilcare.com](mailto:hello@abrilcare.com)

---

*Building open infrastructure for the care economy.*
