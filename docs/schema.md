# Data Schema

This document describes the unified schema for care provider data.

## Overview

All provider data from different state sources is normalized into a consistent schema. This allows consumers to work with data from any state using the same structure.

## Provider Record

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (format: `{source}-{source_id}`) |
| `source_id` | string | Yes | Original ID from source system |
| `source` | string | Yes | Source system identifier (e.g., `nyc_dohmh`, `dc_osse`) |
| `name` | string | Yes | Provider name |
| `type` | string | Yes | Provider type (see below) |

### Provider Types

| Type | Description |
|------|-------------|
| `childcare_center` | Licensed childcare center |
| `family_childcare` | Family-based childcare (home) |
| `group_home` | Group family daycare |
| `religious_exempt` | Religiously-exempt program |
| `head_start` | Head Start program |
| `school_age` | School-age only program |

### License Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `number` | string | Yes | License/permit number |
| `type` | string | Yes | License type |
| `status` | string | Yes | Current status |
| `issued` | date | No | Issue date |
| `expires` | date | No | Expiration date |

**Status Values:** `active`, `suspended`, `revoked`, `expired`, `pending`

### Location Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `address_line1` | string | Yes | Street address |
| `address_line2` | string | No | Unit, suite, etc. |
| `city` | string | Yes | City name |
| `state` | string | Yes | Two-letter state code |
| `zip_code` | string | Yes | ZIP code |
| `county` | string | No | County name |
| `lat` | float | No | Latitude |
| `lng` | float | No | Longitude |

### Capacity Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `total` | integer | Yes | Total licensed capacity |
| `infant` | integer | No | Capacity for 0-12 months |
| `toddler` | integer | No | Capacity for 12-36 months |
| `preschool` | integer | No | Capacity for 3-5 years |
| `school_age` | integer | No | Capacity for 5+ years |

### Contact Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone` | string | No | Primary phone number |
| `email` | string | No | Email address |
| `website` | string | No | Website URL |
| `primary_contact` | string | No | Contact person name |

### Additional Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `accepts_subsidies` | boolean | No | Whether provider accepts government subsidies |
| `subsidy_programs` | array | No | List of accepted subsidy programs |
| `quality_rating` | string | No | QRIS or state quality rating |
| `quality_rating_date` | date | No | When rating was assigned |
| `last_inspection` | date | No | Most recent inspection date |
| `violations_count` | integer | No | Number of violations at last inspection |

### Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `created_at` | datetime | Yes | When record was created |
| `updated_at` | datetime | Yes | When record was last updated |
| `data_quality_score` | float | No | Completeness score (0.0-1.0) |

## Example

```json
{
  "id": "nyc-dohmh-12345",
  "source_id": "12345",
  "source": "nyc_dohmh",
  "name": "Sunshine Child Care Center",
  "type": "childcare_center",
  "license": {
    "number": "NYC-2024-12345",
    "type": "center",
    "status": "active",
    "expires": "2026-12-31"
  },
  "location": {
    "address_line1": "123 Main Street",
    "city": "Brooklyn",
    "state": "NY",
    "zip_code": "11201",
    "county": "BROOKLYN",
    "lat": 40.6892,
    "lng": -73.9857
  },
  "capacity": {
    "total": 75,
    "infant": 10,
    "toddler": 20,
    "preschool": 30,
    "school_age": 15
  },
  "contact": {
    "phone": "(718) 555-1234",
    "email": "info@sunshineccc.example.com"
  },
  "accepts_subsidies": true,
  "subsidy_programs": ["ACS_VOUCHER", "HEAD_START"],
  "quality_rating": "QUALITY_RATED",
  "last_inspection": "2025-11-15",
  "violations_count": 0,
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-03-13T14:22:00Z",
  "data_quality_score": 0.95
}
```

## Source Mappings

Each state extractor maps source-specific fields to this unified schema. See the extractor code for specific mappings:

- [NYC DOHMH](../src/extractors/nyc_dohmh.py)
- DC OSSE (coming soon)
- Maryland CheckCC (coming soon)
- Virginia VDOE (coming soon)
