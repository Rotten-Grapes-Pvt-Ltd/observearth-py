"""Base satellite class for all satellite collections."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import planetary_computer
from pystac_client import Client

from .items import SatelliteItems


class BaseSatellite(ABC):
    """Base class for all satellite collections."""

    def __init__(self):
        """Initialize the satellite with MPC STAC client."""
        self.client = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )

    @property
    @abstractmethod
    def collection_id(self) -> str:
        """Return the STAC collection ID for this satellite."""
        pass

    def search(
        self,
        start_date: str,
        end_date: str,
        geom: Dict[str, Any],
        cloud_cover: Optional[int] = None,
        **kwargs,
    ) -> SatelliteItems:
        """
        Search for satellite items.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            geom: GeoJSON geometry
            cloud_cover: Maximum cloud cover percentage
            **kwargs: Additional search parameters

        Returns:
            SatelliteItems object containing the search results
        """
        search_params = {
            "collections": [self.collection_id],
            "datetime": f"{start_date}/{end_date}",
            "intersects": geom,
        }

        search_params.update(kwargs)
        if cloud_cover is not None:
            search_params["query"]["eo:cloud_cover"] = {"lt": cloud_cover}

        search = self.client.search(**search_params)
        items = list(search.items())

        return SatelliteItems(items, self.collection_id, geom)
