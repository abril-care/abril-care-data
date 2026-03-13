# Abril Care Data

**Making care work visible through open data infrastructure.**

The care economy generates $122 billion in annual lost economic output. 51% of Americans live in childcare deserts. Working families make six-figure career decisions with napkin math and gut instinct—while corporations have entire departments dedicated to data-driven resource allocation.

This project builds the data infrastructure that care decisions deserve.

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

### Phase 1: Provider Data Layer (Now)

Aggregating licensed provider data from public state sources:

| Region | Providers | Status |
|--------|-----------|--------|
| NYC | ~12,000 | Live |
| DC | ~600 | In progress |
| Maryland | ~9,000 | Next |
| Virginia | ~7,000 | Planned |

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

The highest-impact contribution is adding data from a new state. See [Adding a State](docs/adding-a-state.md).

Priority states:
- **Texas** — Large market, modern API (TX3C)
- **California** — Largest market, complex system
- **Florida** — High need, limited current coverage

### Report Issues

Found incorrect data? Missing providers? [Open an issue](https://github.com/abril-care/abril-care-data/issues).

### Spread the Word

If you're working on care access, family economic security, or open data—let's connect. This infrastructure is only valuable if people build on it.

---

## Roadmap

### 2026 Q2
- [x] NYC provider data (Open Data API)
- [ ] DC provider data (OSSE PDF parsing)
- [ ] Maryland provider data (CheckCCMD)
- [ ] Public API launch

### 2026 Q3
- [ ] Virginia, Texas expansion
- [ ] Subsidy eligibility engine
- [ ] Provider availability tracking

### 2026 Q4
- [ ] California integration
- [ ] Research partnership pilots
- [ ] Community governance framework

---

## Context

This project emerged from a simple question: why do corporations have better data infrastructure for selling software than families have for finding childcare?

I spent a decade building revenue operations systems—predictive models, data pipelines, forecast accuracy at scale. After my daughter was born, I found myself at 2am building a financial model to figure out if I could afford to go back to work. The math was brutal. The data was worse.

Working families deserve the same data infrastructure that corporations take for granted. This is a start.

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
