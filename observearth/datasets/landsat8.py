"""Landsat-8 satellite implementation."""

from ..core.base_satellite import BaseSatellite


class Landsat8(BaseSatellite):
    """Landsat-8 satellite data access."""

    def __init__(self):
        """Initialize Landsat-8."""
        super().__init__()

    @property
    def collection_id(self) -> str:
        """Return Landsat-8 collection ID."""
        return "landsat-8-c2-l2"
