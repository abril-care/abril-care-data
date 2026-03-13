"""
NYC DOHMH Childcare Center Data Extractor.

Data source: NYC Open Data
- Childcare Centers: https://data.cityofnewyork.us/Health/Childcare-Centers/tdif-34xu
- Inspections: https://data.cityofnewyork.us/Health/DOHMH-Childcare-Center-Inspections/dsg6-ifza

This is the easiest extractor because NYC provides a clean Socrata API.
"""

import logging
from typing import List, Optional
from datetime import datetime

try:
    from sodapy import Socrata
except ImportError:
    Socrata = None

from src.schema import Provider, License, Location, Capacity, Contact

logger = logging.getLogger(__name__)


class NYCExtractor:
    """
    Extractor for NYC DOHMH childcare center data.

    Uses the Socrata Open Data API to fetch licensed childcare centers
    in New York City.
    """

    DOMAIN = "data.cityofnewyork.us"
    CENTERS_DATASET = "tdif-34xu"
    INSPECTIONS_DATASET = "dsg6-ifza"

    def __init__(self, app_token: Optional[str] = None):
        """
        Initialize the NYC extractor.

        Args:
            app_token: Optional Socrata app token for higher rate limits.
                      Get one at: https://data.cityofnewyork.us/profile/edit/developer_settings
        """
        if Socrata is None:
            raise ImportError("sodapy is required. Install with: pip install sodapy")

        self.client = Socrata(self.DOMAIN, app_token)
        self.source = "nyc_dohmh"

    def extract(self, limit: int = 50000) -> List[Provider]:
        """
        Fetch all childcare centers from NYC Open Data.

        Args:
            limit: Maximum number of records to fetch (default 50000)

        Returns:
            List of Provider objects
        """
        logger.info(f"Fetching up to {limit} childcare centers from NYC Open Data...")

        results = self.client.get(
            self.CENTERS_DATASET,
            limit=limit,
            where="status = 'Permitted'"  # Only active permits
        )

        logger.info(f"Fetched {len(results)} records")

        providers = []
        for record in results:
            try:
                provider = self._transform(record)
                providers.append(provider)
            except Exception as e:
                logger.warning(f"Failed to transform record {record.get('dc_id', 'unknown')}: {e}")

        logger.info(f"Successfully transformed {len(providers)} providers")
        return providers

    def _transform(self, record: dict) -> Provider:
        """
        Transform a raw NYC record to the unified Provider schema.

        Args:
            record: Raw record from Socrata API

        Returns:
            Provider object
        """
        # Extract permit/license info
        permit_number = record.get("permit_number", record.get("dc_id", ""))

        license_info = License(
            number=permit_number,
            type="center",
            status="active" if record.get("status") == "Permitted" else "inactive",
        )

        # Build address
        address_parts = [
            record.get("building", ""),
            record.get("street", ""),
        ]
        address = " ".join(filter(None, address_parts)).strip()

        location = Location(
            address_line1=address or "Unknown",
            city="New York",
            state="NY",
            zip_code=record.get("zipcode", ""),
            county=record.get("borough", ""),
            lat=self._safe_float(record.get("latitude")),
            lng=self._safe_float(record.get("longitude")),
        )

        # Capacity
        max_capacity = self._safe_int(record.get("maximumcapacity"))
        capacity = Capacity(total=max_capacity) if max_capacity else None

        # Contact
        phone = record.get("phone")
        contact = Contact(phone=phone) if phone else None

        # Build provider ID
        source_id = str(permit_number or record.get("dc_id", ""))
        provider_id = f"{self.source}-{source_id}"

        return Provider(
            id=provider_id,
            source_id=source_id,
            source=self.source,
            name=record.get("centername", record.get("center_name", "Unknown")),
            type="childcare_center",
            license=license_info,
            location=location,
            capacity=capacity,
            contact=contact,
            updated_at=datetime.utcnow(),
        )

    @staticmethod
    def _safe_float(value) -> Optional[float]:
        """Safely convert value to float."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_int(value) -> Optional[int]:
        """Safely convert value to int."""
        if value is None:
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None


def main():
    """CLI entry point for testing the extractor."""
    import argparse

    parser = argparse.ArgumentParser(description="Extract NYC childcare data")
    parser.add_argument("--limit", type=int, default=100, help="Number of records to fetch")
    parser.add_argument("--token", type=str, help="Socrata app token")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    extractor = NYCExtractor(app_token=args.token)
    providers = extractor.extract(limit=args.limit)

    print(f"\nExtracted {len(providers)} providers\n")

    # Print sample
    for provider in providers[:5]:
        print(f"  {provider.name}")
        print(f"    Location: {provider.location.address_line1}, {provider.location.county}")
        print(f"    Capacity: {provider.capacity.total if provider.capacity else 'N/A'}")
        print()


if __name__ == "__main__":
    main()
