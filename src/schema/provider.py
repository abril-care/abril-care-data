"""Provider schema definition."""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field


class License(BaseModel):
    """Provider license information."""

    number: str
    type: str  # 'center', 'family_home', 'group_home', 'religious_exempt'
    status: str  # 'active', 'suspended', 'revoked', 'expired'
    issued: Optional[date] = None
    expires: Optional[date] = None


class Location(BaseModel):
    """Provider location."""

    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    county: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class Capacity(BaseModel):
    """Provider capacity by age group."""

    total: int
    infant: Optional[int] = None  # 0-12 months
    toddler: Optional[int] = None  # 12-36 months
    preschool: Optional[int] = None  # 3-5 years
    school_age: Optional[int] = None  # 5+ years


class Contact(BaseModel):
    """Provider contact information."""

    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    primary_contact: Optional[str] = None


class Provider(BaseModel):
    """
    Unified care provider record.

    This schema normalizes provider data from multiple state sources
    into a consistent format.
    """

    # Identifiers
    id: str = Field(..., description="Unique identifier (source-originalid)")
    source_id: str = Field(..., description="Original ID from source system")
    source: str = Field(..., description="Source system identifier")

    # Basic info
    name: str
    type: str  # 'childcare_center', 'family_childcare', 'group_home', etc.

    # License
    license: License

    # Location
    location: Location

    # Capacity
    capacity: Optional[Capacity] = None

    # Contact
    contact: Optional[Contact] = None

    # Subsidies
    accepts_subsidies: Optional[bool] = None
    subsidy_programs: Optional[List[str]] = None

    # Quality
    quality_rating: Optional[str] = None
    quality_rating_date: Optional[date] = None

    # Inspections
    last_inspection: Optional[date] = None
    violations_count: Optional[int] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    data_quality_score: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Data completeness score"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "nyc-dohmh-12345",
                "source_id": "12345",
                "source": "nyc_dohmh",
                "name": "Sunshine Child Care Center",
                "type": "childcare_center",
                "license": {
                    "number": "DC-2024-1234",
                    "type": "center",
                    "status": "active",
                    "expires": "2026-12-31",
                },
                "location": {
                    "address_line1": "123 Main St",
                    "city": "Washington",
                    "state": "DC",
                    "zip_code": "20001",
                    "lat": 38.9072,
                    "lng": -77.0369,
                },
                "capacity": {"total": 75, "infant": 10, "toddler": 20, "preschool": 30, "school_age": 15},
                "contact": {"phone": "(202) 555-1234"},
                "accepts_subsidies": True,
                "quality_rating": "Level 4",
            }
        }
