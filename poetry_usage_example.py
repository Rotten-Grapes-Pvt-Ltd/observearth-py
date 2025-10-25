#!/usr/bin/env python3
"""
Example showing how to use the observearth package with Poetry.
Run with: poetry run python poetry_usage_example.py
"""

import observearth as oe


def main():
    """Test Poetry installation."""
    print("🎭 Poetry Package Test")
    print("=" * 40)

    # Test Sentinel-2
    sat = oe.Sentinel2(product="2A")
    print(f"✅ Sentinel-2: {sat.collection_id}")

    # Test Landsat-8
    ls8 = oe.Landsat8()
    print(f"✅ Landsat-8: {ls8.collection_id}")

    # Test geometry utilities
    from observearth.core.utils import create_sample_geometry

    geom = create_sample_geometry(77.0, 23.0, 0.05)
    print(f"✅ Geometry: {geom['type']}")

    print("\n🎉 All Poetry functionality working!")
    print("\n💡 Usage:")
    print("   poetry run python your_script.py")
    print("   poetry run jupyter notebook")
    print("   poetry run pytest")


if __name__ == "__main__":
    main()
