# Usage Guide

This guide provides detailed examples and usage instructions for all scripts in the Catalyst Center Export Tools repository.

## Table of Contents

- [Quick Start](#quick-start)
- [Script Reference](#script-reference)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/johnturek/Scripts.git
cd Scripts

# Install dependencies
pip install -r requirements.txt

# Create settings file
cp settings.py.example settings.py

# Edit settings.py with your Catalyst Center credentials
nano settings.py
```

### 2. Test Connection

```bash
# Test if connection works
python3 catalyst_cli.py test
```

### 3. Basic Export

```bash
# Export switches to CSV
python3 getSwitches.py

# Export all data to Excel
python3 exportToExcel.py
```

## Script Reference

### getSwitches.py

Export detailed switch information with site data to CSV.

**Basic Usage:**
```bash
python3 getSwitches.py
```

**Advanced Options:**
```bash
# Specify custom output file
python3 getSwitches.py -o my_switches.csv

# Enable verbose logging
python3 getSwitches.py -v

# Combine options
python3 getSwitches.py -o switches_$(date +%Y%m%d).csv -v
```

**Output Fields:**
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

---

### withExport.py

Export raw JSON data for switches, sites, and IP pools.

**Basic Usage:**
```bash
# Export all data to CSV (default)
python3 withExport.py

# Export to JSON format
python3 withExport.py --format json

# Export to both CSV and JSON
python3 withExport.py --format both
```

**Advanced Options:**
```bash
# Export only switches
python3 withExport.py --switches-only

# Export only sites
python3 withExport.py --sites-only

# Export only IP pools
python3 withExport.py --pools-only

# Specify output directory
python3 withExport.py -o /path/to/output --format json

# Verbose mode
python3 withExport.py -v --format both
```

**Output Files:**
- `all_switches_raw.csv` / `.json` - Switch data
- `all_sites_raw.csv` / `.json` - Site data
- `all_ip_subnets_raw.csv` / `.json` - IP pool data

---

### exportToExcel.py

Export comprehensive data to Excel with multiple formatted worksheets.

**Basic Usage:**
```bash
python3 exportToExcel.py
```

**Advanced Options:**
```bash
# Specify custom output file
python3 exportToExcel.py -o network_report.xlsx

# Enable verbose logging
python3 exportToExcel.py -v
```

**Excel Workbook Contents:**
- **Summary Sheet**: Overview with counts and export date
- **Switches Sheet**: Detailed switch information with formatting
- **Sites Sheet**: All site information
- **IP Pools Sheet**: IP subnet/pool information

**Features:**
- Color-coded headers
- Auto-adjusted column widths
- Frozen header rows
- Professional formatting

---

### catalyst_cli.py

Unified command-line interface for all operations.

**Commands:**

#### Test Connection
```bash
python3 catalyst_cli.py test
```

#### Show Information
```bash
python3 catalyst_cli.py info
```

#### List Devices
```bash
# List all devices
python3 catalyst_cli.py list devices

# List only switches
python3 catalyst_cli.py list switches

# List sites
python3 catalyst_cli.py list sites

# Show counts only
python3 catalyst_cli.py list devices --count-only
```

#### Export Data
```bash
# Export switches to CSV
python3 catalyst_cli.py export switches --format csv

# Export all data to Excel
python3 catalyst_cli.py export all --format excel -o report.xlsx

# Export with verbose logging
python3 catalyst_cli.py export switches -v
```

---

### utils.py

Utility module with shared functions (imported by other scripts).

**Key Functions:**
- `load_settings()` - Load configuration from settings.py
- `connect_to_catalyst()` - Establish API connection
- `get_all_devices()` - Retrieve all network devices
- `filter_devices_by_family()` - Filter devices by type
- `get_site_info()` - Get site information with caching

## Common Use Cases

### Daily Network Export

Create a script to automate daily exports:

```bash
#!/bin/bash
# daily_export.sh

DATE=$(date +%Y%m%d)
OUTPUT_DIR="/path/to/exports/$DATE"

mkdir -p "$OUTPUT_DIR"

cd /path/to/Scripts

# Export switches
python3 getSwitches.py -o "$OUTPUT_DIR/switches_$DATE.csv"

# Export raw data for analysis
python3 withExport.py -o "$OUTPUT_DIR" --format both

# Create Excel report
python3 exportToExcel.py -o "$OUTPUT_DIR/network_report_$DATE.xlsx"

echo "Export completed: $OUTPUT_DIR"
```

### Weekly Network Report

```bash
#!/bin/bash
# weekly_report.sh

WEEK=$(date +%Y_W%U)
OUTPUT_FILE="network_report_$WEEK.xlsx"

cd /path/to/Scripts
python3 exportToExcel.py -o "$OUTPUT_FILE"

# Email or upload the report
# mail -s "Weekly Network Report" admin@example.com < "$OUTPUT_FILE"
```

### Custom Filtering

For custom filtering, you can modify the scripts or use the raw JSON export:

```bash
# Export raw data
python3 withExport.py --switches-only --format json

# Then process with jq or Python
cat all_switches_raw.json | jq '.[] | select(.role == "ACCESS")'
```

### Integration with Other Tools

```bash
# Export and import into database
python3 withExport.py --format json
python3 import_to_db.py --input all_switches_raw.json

# Generate reports
python3 getSwitches.py -o switches.csv
python3 generate_dashboard.py --input switches.csv
```

## Troubleshooting

### Connection Issues

**Problem:** SSL certificate errors

**Solution:**
```python
# In settings.py, add:
CATALYST_VERIFY = False
```

Or modify the script to disable SSL verification (not recommended for production).

---

**Problem:** Authentication fails

**Solution:**
1. Verify credentials in `settings.py`
2. Check user permissions in Catalyst Center
3. Test connection: `python3 catalyst_cli.py test`

---

### No Data Returned

**Problem:** No switches found

**Solution:**
1. Verify devices exist in Catalyst Center
2. Check device family is "Switch" (case-sensitive)
3. Verify API permissions

---

### Performance Issues

**Problem:** Script takes too long

**Solutions:**
1. Use `--switches-only` or similar filters
2. Enable caching (already implemented for sites)
3. Run during off-peak hours
4. Use raw export for faster bulk operations

---

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'catalystcentersdk'`

**Solution:**
```bash
pip install -r requirements.txt
```

---

**Problem:** `ModuleNotFoundError: No module named 'openpyxl'`

**Solution:**
```bash
pip install openpyxl
```

## Advanced Usage

### Cron Jobs

Schedule automatic exports:

```cron
# Daily export at 2 AM
0 2 * * * /path/to/Scripts/daily_export.sh

# Weekly Excel report on Mondays at 8 AM
0 8 * * 1 cd /path/to/Scripts && python3 exportToExcel.py -o weekly_report.xlsx
```

### Environment Variables

You can also use environment variables for configuration:

```bash
export CATALYST_USERNAME="admin"
export CATALYST_PASSWORD="password"
export CATALYST_BASE_URL="https://catalyst.example.com"

python3 getSwitches.py
```

### Logging to File

```bash
# Redirect logging to file
python3 getSwitches.py -v > export.log 2>&1

# Or use Python logging configuration
python3 getSwitches.py -v 2> errors.log
```

## Best Practices

1. **Security**
   - Never commit `settings.py` to version control
   - Use read-only accounts when possible
   - Enable SSL verification in production
   - Rotate credentials regularly

2. **Performance**
   - Use caching for repeated API calls
   - Filter data at source when possible
   - Schedule heavy operations during off-peak hours

3. **Maintenance**
   - Keep dependencies updated: `pip install -U -r requirements.txt`
   - Review logs regularly
   - Test scripts after Catalyst Center upgrades
   - Maintain backups of exported data

4. **Organization**
   - Use consistent naming for output files
   - Organize exports by date/type
   - Document custom modifications
   - Version control your settings templates

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review Catalyst Center SDK documentation
- Check Catalyst Center API documentation
- Review script logs with `-v` flag
