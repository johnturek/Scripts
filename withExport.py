#!/usr/bin/env python3
"""
Export raw Cisco Catalyst Center data for switches, sites, and IP subnets.

This script retrieves raw JSON data from Catalyst Center and exports it to CSV
files for further analysis or processing. Supports multiple output formats.
"""

import csv
import json
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any
from catalystcentersdk import CatalystCenter
from catalystcentersdk.exceptions import ApiError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_settings():
    """Load settings from settings.py file or use environment defaults."""
    try:
        from settings import CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
        return CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
    except ImportError:
        logger.warning("Settings file not found. Attempting to use environment-based authentication...")
        # Try environment-based authentication (Catalyst SDK will handle this)
        return None, None, None


def connect_to_catalyst() -> CatalystCenter:
    """
    Establish connection to Catalyst Center.
    
    Returns:
        CatalystCenter: Connected Catalyst Center client
    """
    try:
        username, password, base_url = load_settings()
        
        if username and password and base_url:
            logger.info(f"Connecting to Catalyst Center at {base_url}...")
            catalyst = CatalystCenter(
                base_url=base_url,
                username=username,
                password=password,
                verify=True
            )
        else:
            logger.info("Using environment-based authentication...")
            catalyst = CatalystCenter()
        
        logger.info("Successfully connected to Catalyst Center")
        return catalyst
    except Exception as e:
        logger.error(f"Failed to connect to Catalyst Center: {e}")
        sys.exit(1)


def get_switches(catalyst: CatalystCenter) -> List[Dict[str, Any]]:
    """Retrieve all network switches."""
    try:
        logger.info("Retrieving all network devices...")
        devices = catalyst.device.get_all_network_devices().response
        switches = [d for d in devices if 'Switch' in d.get('family', '')]
        logger.info(f"Found {len(switches)} switches")
        return switches
    except ApiError as e:
        logger.error(f"API error while retrieving devices: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while retrieving devices: {e}")
        return []


def get_sites(catalyst: CatalystCenter) -> List[Dict[str, Any]]:
    """Retrieve all sites."""
    try:
        logger.info("Retrieving all sites...")
        sites = catalyst.site.get_all_sites().response
        logger.info(f"Found {len(sites)} sites")
        return sites
    except ApiError as e:
        logger.error(f"API error while retrieving sites: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while retrieving sites: {e}")
        return []


def get_ip_pools(catalyst: CatalystCenter) -> List[Dict[str, Any]]:
    """Retrieve all IP pools."""
    try:
        logger.info("Retrieving all IP pools...")
        ip_pools = catalyst.network_settings.get_all_ip_pools().response
        logger.info(f"Found {len(ip_pools)} IP pools")
        return ip_pools
    except ApiError as e:
        logger.error(f"API error while retrieving IP pools: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while retrieving IP pools: {e}")
        return []


def export_to_csv(data: List[Dict], filename: str, data_type: str) -> None:
    """
    Export data to CSV file with raw JSON.
    
    Args:
        data: List of data dictionaries
        filename: Output file name
        data_type: Type of data being exported (for logging)
    """
    try:
        logger.info(f"Writing {len(data)} {data_type} records to {filename}...")
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['raw_json'])
            for item in data:
                writer.writerow([json.dumps(item)])
        logger.info(f"Successfully exported {data_type} to {filename}")
    except IOError as e:
        logger.error(f"Failed to write to file {filename}: {e}")


def export_to_json(data: List[Dict], filename: str, data_type: str) -> None:
    """
    Export data to JSON file.
    
    Args:
        data: List of data dictionaries
        filename: Output file name
        data_type: Type of data being exported (for logging)
    """
    try:
        logger.info(f"Writing {len(data)} {data_type} records to {filename}...")
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2)
        logger.info(f"Successfully exported {data_type} to {filename}")
    except IOError as e:
        logger.error(f"Failed to write to file {filename}: {e}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Export raw Cisco Catalyst Center data (switches, sites, IP pools)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['csv', 'json', 'both'],
        default='csv',
        help='Output format (default: csv)'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='.',
        help='Output directory for exported files (default: current directory)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--switches-only',
        action='store_true',
        help='Export only switch data'
    )
    parser.add_argument(
        '--sites-only',
        action='store_true',
        help='Export only site data'
    )
    parser.add_argument(
        '--pools-only',
        action='store_true',
        help='Export only IP pool data'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine what to export
    export_switches = args.switches_only or not (args.sites_only or args.pools_only)
    export_sites = args.sites_only or not (args.switches_only or args.pools_only)
    export_pools = args.pools_only or not (args.switches_only or args.sites_only)
    
    # Connect to Catalyst Center
    catalyst = connect_to_catalyst()
    
    # Retrieve and export data
    if export_switches:
        switches = get_switches(catalyst)
        if switches:
            if args.format in ['csv', 'both']:
                export_to_csv(switches, output_dir / 'all_switches_raw.csv', 'switches')
            if args.format in ['json', 'both']:
                export_to_json(switches, output_dir / 'all_switches_raw.json', 'switches')
    
    if export_sites:
        sites = get_sites(catalyst)
        if sites:
            if args.format in ['csv', 'both']:
                export_to_csv(sites, output_dir / 'all_sites_raw.csv', 'sites')
            if args.format in ['json', 'both']:
                export_to_json(sites, output_dir / 'all_sites_raw.json', 'sites')
    
    if export_pools:
        ip_pools = get_ip_pools(catalyst)
        if ip_pools:
            if args.format in ['csv', 'both']:
                export_to_csv(ip_pools, output_dir / 'all_ip_subnets_raw.csv', 'IP pools')
            if args.format in ['json', 'both']:
                export_to_json(ip_pools, output_dir / 'all_ip_subnets_raw.json', 'IP pools')
    
    logger.info("Export completed successfully!")


if __name__ == "__main__":
    main()
