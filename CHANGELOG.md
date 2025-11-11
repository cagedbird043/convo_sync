# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-11

### Added

- 🚀 **Modern toolchain upgrade**
  - Pixi environment management for cross-platform reproducibility
  - Ruff for ultra-fast linting and formatting (replaces Black, isort, Flake8)
  - Hatchling build backend (replaces setuptools)
  - Pre-commit hooks for automated code quality
- 📚 **Complete documentation system**
  - MkDocs with Material theme
  - Auto-generated API documentation
  - Comprehensive user guide
  - Installation and quick start guides
- 🔄 **CI/CD automation**
  - Multi-platform testing (Linux, macOS, Windows)
  - Multi-version Python testing (3.11, 3.12)
  - Automated documentation deployment
  - Automatic PyPI releases
- 🎯 **Pixi tasks**
  - `pixi run test` - Run tests with coverage
  - `pixi run lint` - Ruff linting
  - `pixi run format` - Code formatting
  - `pixi run typecheck` - MyPy type checking
  - `pixi run security` - Bandit security scanning
  - `pixi run check` - Run all checks
  - `pixi run docs-serve` - Local documentation server

### Changed

- 📦 Minimum Python version: 3.8 → 3.11
- 🔧 Build backend: setuptools → Hatchling
- 🎨 Code formatter: Black → Ruff
- 📋 Linter: Flake8 + plugins → Ruff
- 🔀 Import sorter: isort → Ruff (built-in)
- 📝 Updated `pyproject.toml` with modern configuration
- 🔄 Updated CI/CD workflows to use Pixi

### Removed

- ❌ Removed Black, isort, Flake8, pylint (replaced by Ruff)
- ❌ Removed Python 3.8, 3.9, 3.10 support
- ❌ Removed interrogate (documentation checking)

### Migration Guide

See [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) for detailed migration instructions.

## [0.1.0] - Previous

### Added

- Initial release
- Basic JSON cleaning functionality
- Markdown conversion
- CLI interface
- Standard library only implementation
