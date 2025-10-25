"""Sentinel-2 satellite implementation."""

from typing import Any, Dict, Optional

from ..core.base_satellite import BaseSatellite
from ..core.items import SatelliteItems


class Sentinel2(BaseSatellite):
    """Sentinel-2 satellite data access."""

    def __init__(self, product: str = "2A"):
        """
        Initialize Sentinel-2 with product type.

        Args:
            product: Product type ('2A', '2B', '2C', or 'all')
        """
        super().__init__()
        self.product = product
        self._validate_product()

    def _validate_product(self) -> None:
        """Validate product type."""
        valid_products = ["2A", "2B", "2C", "all"]
        if self.product not in valid_products:
            raise ValueError(
                f"Invalid product: {self.product}. Must be one of {valid_products}"
            )

    @property
    def collection_id(self) -> str:
        """Return Sentinel-2 collection ID."""
        return "sentinel-2-l2a"

    def search(
        self,
        start_date: str,
        end_date: str,
        geom: Dict[str, Any],
        cloud_cover: Optional[int] = None,
        **kwargs,
    ) -> SatelliteItems:
        """
        Search for Sentinel-2 items with product filtering.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            geom: GeoJSON geometry
            cloud_cover: Maximum cloud cover percentage
            **kwargs: Additional search parameters

        Returns:
            SatelliteItems object containing filtered results
        """
        # Add product filtering if not 'all'
        if self.product != "all":
            if "query" not in kwargs:
                kwargs["query"] = {}
            kwargs["query"]["platform"] = {"eq": f"Sentinel-{self.product}"}
        print(f"Searching Sentinel-2 with product: {self.product}")
        return super().search(start_date, end_date, geom, cloud_cover, **kwargs)
