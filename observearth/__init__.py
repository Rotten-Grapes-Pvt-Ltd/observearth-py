"""
observearth: Simplifying Earth Observation Data Access from Microsoft Planetary Computer
"""

from .datasets.landsat8 import Landsat8
from .datasets.sentinel2 import Sentinel2

__version__ = "0.1.0"
__all__ = ["Sentinel2", "Landsat8"]
