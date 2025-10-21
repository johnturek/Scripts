# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-21

### Added

- Comprehensive README.md with installation and usage instructions
- requirements.txt for dependency management
- settings.py.example template for configuration
- USAGE.md with detailed examples and troubleshooting
- CHANGELOG.md for tracking changes
- Enhanced error handling and logging in all scripts
- Command-line argument support in all scripts
- utils.py module with shared utility functions
- exportToExcel.py for Excel export with formatted worksheets
- catalyst_cli.py unified CLI tool for all operations
- Support for multiple export formats (CSV, JSON, Excel)
- Progress indicators for long-running operations
- Site information caching to reduce API calls
- Verbose logging mode (-v flag)
- Output directory specification
- Selective data export (switches-only, sites-only, pools-only)
- Connection testing functionality
- Device listing and counting features
- Professional Excel formatting with color-coded headers
- Summary worksheet in Excel exports

### Changed

- getSwitches.py: Refactored with improved error handling, logging, and CLI arguments
- withExport.py: Refactored with multiple format support and better error handling
- Updated .gitignore to exclude output files (CSV, JSON, Excel)
- All scripts now have proper docstrings and type hints
- Improved code organization with modular design
- Better exception handling for API errors
- More informative log messages and error reporting

### Improved

- Performance through site information caching
- User experience with progress indicators
- Code maintainability with utility module
- Documentation with multiple guides
- Error messages with actionable suggestions
- Script reusability through modular design

### Fixed

- Potential issues with missing site information
- Better handling of API connection errors
- Proper encoding (UTF-8) for all file operations
- Graceful degradation when optional features are unavailable

## [1.0.0] - Original Release

### Initial Features

- getSwitches.py: Basic switch export to CSV
- withExport.py: Raw data export for switches, sites, and IP pools
- Basic Catalyst Center API integration
- CSV export functionality
- Site information retrieval
- Settings-based authentication

### Known Limitations

- Limited error handling
- No command-line arguments
- Single output format (CSV)
- No logging
- No documentation
- Hardcoded configuration
