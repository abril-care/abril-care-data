# Abril Care Data

**Open data infrastructure for the care economy.**

The US loses $122 billion annually to childcare disruptions. 51% of Americans live in childcare deserts. Only 15% of eligible families receive federal childcare subsidies.

The data to solve these problems exists—scattered across 50 state licensing systems, locked in proprietary platforms, buried in government PDFs. This project pulls it into the open.

---

## The Problem

Care data in the US is fragmented, inaccessible, and serves the wrong people.

**Fragmented:** Provider information is scattered across 50 state licensing systems, each with different formats, update schedules, and access methods. No unified view exists.

**Inaccessible:** What data does exist is locked in proprietary platforms (Care.com, Brightwheel) or buried in government PDFs. Researchers can't study access gaps. Advocates can't identify deserts. Families can't make informed choices.

**Serves the wrong people:** When care data is aggregated, it's typically by companies extracting value from families—not returning it to communities.

The result: the people most affected by care infrastructure gaps—working mothers, communities of color, rural families—are the least equipped with data to navigate them.

---

## The Vision

**Open infrastructure for care data, owned by communities, not corporations.**

We're building:

1. **Aggregation** — Pulling provider data from public state sources into a unified, accessible format
2. **Transparency** — Making licensing, inspection, and capacity data freely available via API
3. **Foundation** — Creating the data layer that enables better tools: care finders, policy analysis, workforce research, subsidy optimization

This is not another platform to extract family data for ad targeting. It's public infrastructure—like OpenStreetMap for care.

---

## Why This Matters

### For Families

A single mother in DC shouldn't need to call 30 providers to find one with infant availability that accepts subsidies. The data exists in state systems. It just isn't accessible.

### For Researchers

Understanding care deserts, workforce dynamics, and policy impacts requires data. Currently, researchers spend months on FOIA requests and manual data cleaning before analysis can begin.

### For Advocates

You can't fix what you can't see. Open care data enables evidence-based advocacy: showing legislators exactly where subsidies aren't reaching families, where provider shortages are acute, where the system is failing.

### For Providers

Small providers—especially family childcare homes—are invisible in the current ecosystem. Open data infrastructure makes them findable, helping fill the 51% of America that's a care desert.

---

## What We're Building

### Phase 1: Provider Data Layer

Aggregating licensed provider data from all 50 states into a unified, accessible format.

**Current coverage:**

| State | Providers | Data |
|-------|----------:|------|
| New York | 16,710 | [ny_providers.json](data/providers/ny_providers.json) |
| Virginia | 5,185 | [va_providers.json](data/providers/va_providers.json) |
| Maryland | 1,950 | [md_providers.json](data/providers/md_providers.json) |
| DC | 549 | [dc_providers.json](data/providers/dc_providers.json) |
| **Total** | **24,394** | **Available now** |

**Expanding to:** Texas, California, Florida, and all 50 states. Each state has public licensing data—it just needs to be aggregated.

### Phase 2: Subsidy & Eligibility Data

Integrating government subsidy information: who qualifies, which providers accept it, how to apply. Currently, only 15% of eligible families receive federal childcare subsidies. The data to change that exists—it's just not connected.

### Phase 3: Community Tools

Building on the data layer to create tools communities actually need: care finders, policy dashboards, workforce analytics, advocacy resources.

---

## Data Principles

**Open by default.** All aggregated data is freely accessible. No paywalls, no API keys required for basic access.

**Privacy-preserving.** We aggregate provider data (businesses), not family data (people). No tracking, no profiling, no extraction.

**Community-governed.** As this project grows, governance should shift to the communities it serves—not remain with a single founder or organization.

**Interoperable.** Standard schemas, clean APIs, easy integration. Built to be built upon.

---

## Technical Overview

```python
from abril import providers

# Find childcare in DC
results = providers.search(
    state="DC",
    type="childcare",
    accepts_subsidies=True,
    has_infant_capacity=True
)

for provider in results:
    print(f"{provider.name}: {provider.capacity.infant} infant slots")
```

### Architecture

- **Extractors**: State-specific modules that fetch data from public sources (APIs, PDFs, web portals)
- **Schema**: Unified Pydantic models normalizing provider data across states
- **API**: FastAPI endpoints for search, filtering, and bulk export

### Current Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Schema | Pydantic |
| API | FastAPI |
| Data Sources | Socrata (NYC), PDF parsing (DC), web scraping (MD, VA) |

---

## Get Involved

### Use the Data

```bash
pip install abril-care-data
```

Documentation: [docs/](docs/)

### Add a State

Every state has public provider licensing data. The highest-impact contribution is adding a new state. See [Adding a State](docs/adding-a-state.md).

**Next priorities:** Texas, California, Florida, Illinois, Pennsylvania, Ohio—covering 50% of the US population.

### Report Issues

Found incorrect data? Missing providers? [Open an issue](https://github.com/abril-care/abril-care-data/issues).

### Spread the Word

If you're working on care access, family economic security, or open data—let's connect. This infrastructure is only valuable if people build on it.

---

## Roadmap

### 2026 Q2 — Foundation
- [x] New York, DC, Maryland, Virginia (24,394 providers)
- [ ] Public API launch
- [ ] Texas, Florida, California

### 2026 Q3 — Scale
- [ ] 25 states covered
- [ ] Subsidy eligibility engine
- [ ] Provider availability tracking

### 2026 Q4 — National
- [ ] All 50 states
- [ ] Research partnership pilots
- [ ] Community governance framework

---

## License

MIT. Use it, build on it, make it better.

---

## Links

- **Repository**: [github.com/abril-care/abril-care-data](https://github.com/abril-care/abril-care-data)
- **Issues**: [Report bugs or request features](https://github.com/abril-care/abril-care-data/issues)
- **Contact**: hello@abrilcare.com

---

*Building open infrastructure for the care economy.*
