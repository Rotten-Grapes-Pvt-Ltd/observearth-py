# Contributing Guidelines

Thank you for your interest in contributing to ObserveEarth! This document outlines our contribution process and standards.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## How to Contribute

### 1. Types of Contributions

- 🐛 **Bug Reports** - Report issues you encounter
- ✨ **Feature Requests** - Suggest new functionality  
- 📝 **Documentation** - Improve docs and examples
- 🧪 **Tests** - Add or improve test coverage
- 🔧 **Code** - Fix bugs or implement features

### 2. Before You Start

- Check existing [issues](https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py/issues) and [pull requests](https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py/pulls)
- For major changes, open an issue first to discuss the approach
- Follow the [development setup](setup.md) guide

### 3. Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# ... edit code ...

# 3. Format and test
poetry run black observearth/ tests/
poetry run isort observearth/ tests/
poetry run pytest

# 4. Commit with clear message
git commit -m "feat: add support for Sentinel-1 data"

# 5. Push and create PR
git push origin feature/your-feature-name
```

## Code Standards

### Python Style
- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 88)
- Use [isort](https://isort.readthedocs.io/) for import sorting
- Add type hints for all public functions

### Documentation
- Add docstrings to all public functions and classes
- Use [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings
- Update relevant documentation in `docs/`
- Include examples in docstrings when helpful

### Testing
- Write tests for new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Include both unit and integration tests

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Maintenance tasks

### Examples
```bash
feat(indices): add EVI (Enhanced Vegetation Index)
fix(export): handle NaN values in PNG export
docs(api): update Sentinel-2 product documentation
test(core): add tests for geometry clipping
```

## Pull Request Process

### 1. PR Requirements
- [ ] Clear title and description
- [ ] Tests pass (`poetry run pytest`)
- [ ] Code is formatted (`poetry run black .`)
- [ ] Documentation updated if needed
- [ ] No merge conflicts

### 2. PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### 3. Review Process
- Maintainers will review within 48 hours
- Address feedback promptly
- Keep discussions constructive
- Be open to suggestions

## Adding New Features

### New Satellite Support
1. Create new file in `observearth/datasets/`
2. Inherit from `BaseSatellite`
3. Implement required methods
4. Add band mapping
5. Write tests
6. Update documentation

### New Indices
1. Add formula to `observearth/core/indices.py`
2. Update `_get_required_bands()` method
3. Add tests in `tests/test_indices.py`
4. Document in API reference

### Example: Adding SAVI Index
```python
# In observearth/core/indices.py
def compute_index(name: str, **bands) -> xr.DataArray:
    # ... existing code ...
    elif name == "SAVI":
        red, nir = bands["RED"], bands["NIR"]
        L = 0.5  # Soil brightness correction factor
        return ((nir - red) / (nir + red + L)) * (1 + L)
```

## Release Process

Releases are handled by maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Publish to PyPI

## Getting Help

- 💬 [GitHub Discussions](https://github.com/Rotten-Grapes-Pvt-Ltd/observearth-py/discussions)
- 📧 Email maintainers: krishna@rottengrapes.tech
- 📖 Read existing code and tests for examples

## Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to ObserveEarth! 🚀