#!/usr/bin/env python3
"""
Export detailed Cisco Catalyst Center switch information to CSV format.

This script retrieves all network switches from Catalyst Center, enriches them
with site information (including geolocation), and exports the data to a CSV file.
"""

import csv
import sys
import logging
import argparse
from typing import Dict, List, Any
from catalystcentersdk import CatalystCenter
from catalystcentersdk.exceptions import ApiError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_settings():
    """Load settings from settings.py file."""
    try:
        from settings import CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
        return CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
    except ImportError:
        logger.error("Settings file not found. Please create settings.py from settings.py.example")
        sys.exit(1)
    except AttributeError as e:
        logger.error(f"Missing required configuration in settings.py: {e}")
        sys.exit(1)


def connect_to_catalyst(username: str, password: str, base_url: str) -> CatalystCenter:
    """
    Establish connection to Catalyst Center.
    
    Args:
        username: Catalyst Center username
        password: Catalyst Center password
        base_url: Catalyst Center base URL
        
    Returns:
        CatalystCenter: Connected Catalyst Center client
    """
    try:
        logger.info(f"Connecting to Catalyst Center at {base_url}...")
        catalyst = CatalystCenter(
            base_url=base_url,
            username=username,
            password=password,
            verify=True
        )
        logger.info("Successfully connected to Catalyst Center")
        return catalyst
    except Exception as e:
        logger.error(f"Failed to connect to Catalyst Center: {e}")
        sys.exit(1)


def get_all_switches(catalyst: CatalystCenter) -> List[Dict[str, Any]]:
    """
    Retrieve all network switches from Catalyst Center.
    
    Args:
        catalyst: Connected Catalyst Center client
        
    Returns:
        List of switch devices
    """
    try:
        logger.info("Retrieving all network devices...")
        devices = catalyst.device.get_all_network_devices().response
        switches = [d for d in devices if 'Switch' in d.get('family', '')]
        logger.info(f"Found {len(switches)} switches out of {len(devices)} total devices")
        return switches
    except ApiError as e:
        logger.error(f"API error while retrieving devices: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error while retrieving devices: {e}")
        sys.exit(1)


def get_site_details(catalyst: CatalystCenter, site_id: str, site_cache: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Get site details with caching to avoid redundant API calls.
    
    Args:
        catalyst: Connected Catalyst Center client
        site_id: Site identifier
        site_cache: Cache dictionary for site data
        
    Returns:
        Site details dictionary
    """
    if site_id in site_cache:
        return site_cache[site_id]
    
    try:
        site = catalyst.site.get_site(site_id=site_id).response
        site_cache[site_id] = site
        return site
    except ApiError as e:
        logger.warning(f"Failed to retrieve site details for {site_id}: {e}")
        return {}
    except Exception as e:
        logger.warning(f"Unexpected error retrieving site {site_id}: {e}")
        return {}


def prepare_switch_data(switches: List[Dict], catalyst: CatalystCenter) -> List[Dict[str, str]]:
    """
    Prepare switch data with site information for CSV export.
    
    Args:
        switches: List of switch devices
        catalyst: Connected Catalyst Center client
        
    Returns:
        List of formatted switch data dictionaries
    """
    site_cache = {}
    csv_data = []
    
    logger.info("Processing switch data and enriching with site information...")
    for idx, switch in enumerate(switches, 1):
        if idx % 10 == 0:
            logger.info(f"Processing switch {idx}/{len(switches)}...")
        
        # Get site info
        site_id = switch.get('siteId')
        site_name = ''
        latitude = ''
        longitude = ''
        
        if site_id:
            site_info = get_site_details(catalyst, site_id, site_cache)
            site_name = site_info.get('site', {}).get('name', '')
            latitude = site_info.get('site', {}).get('latitude', '')
            longitude = site_info.get('site', {}).get('longitude', '')
        
        # Collect switch details
        csv_data.append({
            'hostname': switch.get('hostname', ''),
            'managementIpAddress': switch.get('managementIpAddress', ''),
            'macAddress': switch.get('macAddress', ''),
            'serialNumber': switch.get('serialNumber', ''),
            'platformId': switch.get('platformId', ''),
            'softwareVersion': switch.get('softwareVersion', ''),
            'role': switch.get('role', ''),
            'site_name': site_name,
            'latitude': latitude,
            'longitude': longitude,
        })
    
    return csv_data


def export_to_csv(data: List[Dict], output_file: str) -> None:
    """
    Export switch data to CSV file.
    
    Args:
        data: List of switch data dictionaries
        output_file: Output CSV file path
    """
    try:
        logger.info(f"Writing data to {output_file}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'hostname', 'managementIpAddress', 'macAddress', 'serialNumber',
                'platformId', 'softwareVersion', 'role', 'site_name', 'latitude', 'longitude'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Successfully exported {len(data)} switches to {output_file}")
    except IOError as e:
        logger.error(f"Failed to write to file {output_file}: {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Export Cisco Catalyst Center switch information to CSV'
    )
    parser.add_argument(
        '-o', '--output',
        default='cisco_switches.csv',
        help='Output CSV file name (default: cisco_switches.csv)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Load configuration
    username, password, base_url = load_settings()
    
    # Connect to Catalyst Center
    catalyst = connect_to_catalyst(username, password, base_url)
    
    # Get all switches
    switches = get_all_switches(catalyst)
    
    if not switches:
        logger.warning("No switches found in Catalyst Center")
        sys.exit(0)
    
    # Prepare data with site information
    csv_data = prepare_switch_data(switches, catalyst)
    
    # Export to CSV
    export_to_csv(csv_data, args.output)
    
    logger.info("Export completed successfully!")


if __name__ == "__main__":
    main()
