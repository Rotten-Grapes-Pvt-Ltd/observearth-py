# Development Setup

This guide will help you set up a development environment for contributing to ObserveEarth.

## Prerequisites

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Git for version control

## Setup Steps

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/observearth-py.git
cd observearth-py
```

### 2. Install Dependencies

```bash
# Install all dependencies including dev tools
poetry install

# Activate the virtual environment
poetry shell
```

### 3. Verify Installation

```bash
# Run tests to ensure everything works
poetry run pytest

# Test basic functionality
poetry run python -c "import observearth as oe; print('✅ Setup complete!')"
```

## Development Tools

The project includes several development tools:

### Code Formatting
```bash
# Format code with Black
poetry run black observearth/ tests/

# Sort imports with isort
poetry run isort observearth/ tests/
```

### Type Checking
```bash
# Run type checking with mypy
poetry run mypy observearth/
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=observearth

# Run specific test file
poetry run pytest tests/test_indices.py -v
```

### Documentation
```bash
# Serve documentation locally
poetry run mkdocs serve

# Build documentation
poetry run mkdocs build
```

## Project Structure

```
observearth-py/
├── observearth/           # Main package
│   ├── core/             # Core functionality
│   │   ├── base_satellite.py
│   │   ├── items.py
│   │   ├── indices.py
│   │   ├── export.py
│   │   └── utils.py
│   └── datasets/         # Satellite implementations
│       ├── sentinel2.py
│       └── landsat8.py
├── tests/                # Test suite
├── docs/                 # Documentation
├── examples/             # Example notebooks
└── pyproject.toml        # Poetry configuration
```

## Environment Variables

For testing with real data, you may need:

```bash
# Optional: Set up Microsoft Planetary Computer credentials
export PLANETARY_COMPUTER_SUBSCRIPTION_KEY="your-key"
```

## IDE Setup

### VS Code
Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort

### PyCharm
Configure Poetry as the project interpreter:
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Poetry Environment
3. Select existing environment

## Next Steps

- Read the [Contributing Guidelines](guidelines.md)
- Learn about [Testing](testing.md)
- Check out existing [Issues](https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py/issues)

## Getting Help

- 💬 [GitHub Discussions](https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py/discussions)
- 🐛 [Report Issues](https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py/issues)
- 📧 Email: krishna@rottengrapes.tech