# Cisco Catalyst Center Network Export Scripts

A collection of Python scripts to export network device information from Cisco Catalyst Center (formerly DNA Center).

## Features

### Core Functionality
- Export detailed switch information to CSV format
- Export raw device, site, and IP subnet data for analysis
- Site information including geolocation data
- Professional Excel reports with multiple worksheets
- Configurable authentication and connection settings

### Enhanced Features (v2.0)
- **Multiple Export Formats**: CSV, JSON, and Excel
- **Command-Line Interface**: Unified CLI tool for all operations
- **Error Handling**: Comprehensive error handling and logging
- **Progress Indicators**: Visual feedback for long-running operations
- **Data Caching**: Efficient API usage with intelligent caching
- **Flexible Filtering**: Export specific data types
- **Setup Validation**: Built-in tool to verify configuration
- **Extensive Documentation**: Detailed guides and examples

## Prerequisites

- Python 3.7 or higher
- Access to a Cisco Catalyst Center instance
- Valid Catalyst Center credentials with appropriate permissions

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/johnturek/Scripts.git
   cd Scripts
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `settings.py` file with your Catalyst Center credentials:
   ```bash
   cp settings.py.example settings.py
   ```

4. Edit `settings.py` with your credentials:
   ```python
   CATALYST_USERNAME = "your_username"
   CATALYST_PASSWORD = "your_password"
   CATALYST_BASE_URL = "https://your-catalyst-center.example.com"
   ```

5. Validate your setup:
   ```bash
   python validate_setup.py
   ```

## Quick Reference

| Script | Purpose | Output |
|--------|---------|--------|
| `getSwitches.py` | Export detailed switch info with sites | CSV file |
| `withExport.py` | Export raw JSON data for all resources | CSV or JSON files |
| `exportToExcel.py` | Create comprehensive Excel report | Excel workbook |
| `catalyst_cli.py` | Unified CLI for all operations | Various |
| `validate_setup.py` | Validate installation and configuration | Console output |

### Quick Start Commands

```bash
# Validate setup
python validate_setup.py

# Test connection
python catalyst_cli.py test

# Export switches
python getSwitches.py

# Create Excel report
python exportToExcel.py

# Export raw JSON data
python withExport.py --format json
```

For detailed usage instructions, see [USAGE.md](USAGE.md).

## Usage

### Export Detailed Switch Information

This script exports switch details with site information to a CSV file:

```bash
python getSwitches.py
```

**Output**: `cisco_switches.csv` with columns:
- hostname
- managementIpAddress
- macAddress
- serialNumber
- platformId
- softwareVersion
- role
- site_name
- latitude
- longitude

### Export Raw Network Data

This script exports raw JSON data for switches, sites, and IP subnets:

```bash
python withExport.py
```

**Output Files**:
- `all_switches_raw.csv` - Raw switch data in JSON format
- `all_sites_raw.csv` - Raw site data in JSON format
- `all_ip_subnets_raw.csv` - Raw IP subnet/pool data in JSON format

## Configuration

### Settings File

The `settings.py` file should contain:

```python
# Catalyst Center API credentials
CATALYST_USERNAME = "admin"
CATALYST_PASSWORD = "password"
CATALYST_BASE_URL = "https://catalyst-center.example.com"

# Optional: Verify SSL certificates (default: True)
# CATALYST_VERIFY = False

# Optional: API version (default: latest)
# CATALYST_VERSION = "2.3.5.3"
```

**Security Note**: Never commit `settings.py` to version control. It's already included in `.gitignore`.

## Output Examples

### cisco_switches.csv
```csv
hostname,managementIpAddress,macAddress,serialNumber,platformId,softwareVersion,role,site_name,latitude,longitude
switch01,10.1.1.1,00:11:22:33:44:55,FCW1234ABCD,C9300-48P,17.6.3,ACCESS,Building A,37.7749,-122.4194
```

### all_switches_raw.csv
```csv
raw_json
"{\"id\": \"abc123\", \"hostname\": \"switch01\", ...}"
```

## Troubleshooting

### Authentication Errors
- Verify your credentials in `settings.py`
- Ensure your account has appropriate API permissions
- Check that the Catalyst Center URL is correct and accessible

### SSL Certificate Errors
If you encounter SSL verification errors, you can disable certificate verification (not recommended for production):
```python
catalyst = CatalystCenter(
    base_url=CATALYST_BASE_URL,
    username=CATALYST_USERNAME,
    password=CATALYST_PASSWORD,
    verify=False
)
```

### No Devices Found
- Verify devices are present in Catalyst Center
- Check that devices have the 'Switch' family designation
- Ensure your account has permissions to view devices

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and operational purposes.

## Support

For issues related to the Catalyst Center SDK, visit:
- [catalystcentersdk Documentation](https://github.com/cisco-en-programmability/catalystcentersdk)
- [Cisco Catalyst Center API Documentation](https://developer.cisco.com/docs/dna-center/)

## Changelog

### Version 1.0.0
- Initial release with basic switch export functionality
- Support for site and IP subnet data export
- CSV output format
