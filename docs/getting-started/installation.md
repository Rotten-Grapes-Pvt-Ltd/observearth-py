# Installation

ObserveEarth can be installed using Poetry (recommended) or pip.

## Prerequisites

- Python 3.9 or higher
- Internet connection for accessing Microsoft Planetary Computer

## Poetry Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py.git
cd observearth-py

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Verify Installation

```bash
poetry run python -c "import observearth as oe; print('✅ Success!')"
```

## Next Steps

- [Quick Start Guide](quick-start.md)
- [Basic NDVI Tutorial](../tutorials/basic-ndvi.md)