#!/usr/bin/env python3
"""
Catalyst Center CLI Tool - Unified interface for all export operations.

This script provides a command-line interface to export data from Cisco
Catalyst Center in various formats and configurations.
"""

import sys
import logging
import argparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Catalyst Center Data Export Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export switches to CSV
  %(prog)s export switches --format csv
  
  # Export all data to Excel
  %(prog)s export all --format excel -o network_data.xlsx
  
  # Export raw JSON data for switches only
  %(prog)s export raw --switches-only --format json
  
  # List available devices
  %(prog)s list devices
  
  # Test connection
  %(prog)s test
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data from Catalyst Center')
    export_parser.add_argument(
        'data_type',
        choices=['switches', 'sites', 'pools', 'all', 'raw'],
        help='Type of data to export'
    )
    export_parser.add_argument(
        '-f', '--format',
        choices=['csv', 'json', 'excel'],
        default='csv',
        help='Output format (default: csv)'
    )
    export_parser.add_argument(
        '-o', '--output',
        help='Output file name'
    )
    export_parser.add_argument(
        '--switches-only',
        action='store_true',
        help='Export only switches (for raw export)'
    )
    export_parser.add_argument(
        '--sites-only',
        action='store_true',
        help='Export only sites (for raw export)'
    )
    export_parser.add_argument(
        '--pools-only',
        action='store_true',
        help='Export only IP pools (for raw export)'
    )
    
    # List command
    list_parser = subparsers.add_parser('list', help='List information from Catalyst Center')
    list_parser.add_argument(
        'item_type',
        choices=['devices', 'switches', 'sites', 'pools'],
        help='Type of items to list'
    )
    list_parser.add_argument(
        '--count-only',
        action='store_true',
        help='Show only count, not details'
    )
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test connection to Catalyst Center')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show Catalyst Center information')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Handle commands
    if args.command == 'export':
        handle_export(args)
    elif args.command == 'list':
        handle_list(args)
    elif args.command == 'test':
        handle_test(args)
    elif args.command == 'info':
        handle_info(args)


def handle_export(args):
    """Handle export command."""
    from utils import load_settings, connect_to_catalyst
    
    username, password, base_url = load_settings()
    catalyst = connect_to_catalyst(username, password, base_url)
    
    if args.data_type == 'switches':
        export_switches(catalyst, args.format, args.output)
    elif args.data_type == 'all' and args.format == 'excel':
        export_to_excel_all(catalyst, args.output)
    elif args.data_type == 'raw':
        export_raw_data(catalyst, args)
    else:
        logger.error(f"Unsupported combination: {args.data_type} with format {args.format}")
        sys.exit(1)


def export_switches(catalyst, fmt, output):
    """Export switches in specified format."""
    import csv
    from utils import get_all_devices, filter_devices_by_family, get_site_info
    
    devices = get_all_devices(catalyst)
    switches = filter_devices_by_family(devices, 'Switch')
    
    if not switches:
        logger.warning("No switches found")
        return
    
    output_file = output or 'cisco_switches.csv'
    
    # Enrich with site data
    site_cache = {}
    enriched_data = []
    
    for switch in switches:
        site_id = switch.get('siteId')
        site_name = ''
        
        if site_id:
            site_info = get_site_info(catalyst, site_id, site_cache)
            site_name = site_info.get('site', {}).get('name', '')
        
        enriched_data.append({
            'hostname': switch.get('hostname', ''),
            'managementIpAddress': switch.get('managementIpAddress', ''),
            'macAddress': switch.get('macAddress', ''),
            'serialNumber': switch.get('serialNumber', ''),
            'platformId': switch.get('platformId', ''),
            'softwareVersion': switch.get('softwareVersion', ''),
            'role': switch.get('role', ''),
            'site_name': site_name,
        })
    
    # Export to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if enriched_data:
            writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
            writer.writeheader()
            writer.writerows(enriched_data)
    
    logger.info(f"Exported {len(enriched_data)} switches to {output_file}")


def export_to_excel_all(catalyst, output):
    """Export all data to Excel."""
    try:
        import exportToExcel
        output_file = output or 'catalyst_export.xlsx'
        
        # Get data
        switches = exportToExcel.get_switches_with_sites(catalyst)
        sites = exportToExcel.get_sites(catalyst)
        pools = exportToExcel.get_ip_pools(catalyst)
        
        # Export
        exportToExcel.export_to_excel(switches, sites, pools, output_file)
        
    except ImportError as e:
        logger.error(f"Excel export requires openpyxl: {e}")
        sys.exit(1)


def export_raw_data(catalyst, args):
    """Export raw data."""
    import withExport
    
    # This would need refactoring of withExport to use as module
    logger.info("For raw export, please use: python withExport.py")
    logger.info("Example: python withExport.py --format json --switches-only")


def handle_list(args):
    """Handle list command."""
    from utils import load_settings, connect_to_catalyst, get_all_devices, filter_devices_by_family
    
    username, password, base_url = load_settings()
    catalyst = connect_to_catalyst(username, password, base_url)
    
    if args.item_type == 'devices':
        devices = get_all_devices(catalyst)
        if args.count_only:
            print(f"Total devices: {len(devices)}")
        else:
            for device in devices:
                print(f"{device.get('hostname', 'N/A'):<30} {device.get('family', 'N/A'):<20} {device.get('managementIpAddress', 'N/A')}")
    
    elif args.item_type == 'switches':
        devices = get_all_devices(catalyst)
        switches = filter_devices_by_family(devices, 'Switch')
        if args.count_only:
            print(f"Total switches: {len(switches)}")
        else:
            for switch in switches:
                print(f"{switch.get('hostname', 'N/A'):<30} {switch.get('platformId', 'N/A'):<30} {switch.get('managementIpAddress', 'N/A')}")
    
    elif args.item_type == 'sites':
        sites = catalyst.site.get_all_sites().response
        if args.count_only:
            print(f"Total sites: {len(sites)}")
        else:
            for site in sites:
                site_info = site.get('site', {})
                print(f"{site_info.get('name', 'N/A'):<50} {site_info.get('locationType', 'N/A')}")
    
    elif args.item_type == 'pools':
        pools = catalyst.network_settings.get_all_ip_pools().response
        if args.count_only:
            print(f"Total IP pools: {len(pools)}")
        else:
            for pool in pools:
                print(f"{pool.get('ipPoolName', 'N/A'):<30} {pool.get('ipPoolCidr', 'N/A')}")


def handle_test(args):
    """Test connection to Catalyst Center."""
    from utils import load_settings, connect_to_catalyst
    
    try:
        username, password, base_url = load_settings()
        logger.info(f"Testing connection to {base_url}...")
        
        catalyst = connect_to_catalyst(username, password, base_url)
        
        # Try a simple API call
        devices = catalyst.device.get_all_network_devices().response
        
        print("\n" + "="*50)
        print("CONNECTION TEST SUCCESSFUL")
        print("="*50)
        print(f"Base URL: {base_url}")
        print(f"Username: {username}")
        print(f"Total devices found: {len(devices)}")
        print("="*50 + "\n")
        
    except Exception as e:
        print("\n" + "="*50)
        print("CONNECTION TEST FAILED")
        print("="*50)
        print(f"Error: {e}")
        print("="*50 + "\n")
        sys.exit(1)


def handle_info(args):
    """Show Catalyst Center information."""
    from utils import load_settings, connect_to_catalyst
    
    username, password, base_url = load_settings()
    catalyst = connect_to_catalyst(username, password, base_url)
    
    # Get summary information
    devices = catalyst.device.get_all_network_devices().response
    sites = catalyst.site.get_all_sites().response
    
    switches = [d for d in devices if 'Switch' in d.get('family', '')]
    routers = [d for d in devices if 'Router' in d.get('family', '')]
    
    print("\n" + "="*50)
    print("CATALYST CENTER SUMMARY")
    print("="*50)
    print(f"Base URL: {base_url}")
    print(f"\nNetwork Devices:")
    print(f"  Total Devices: {len(devices)}")
    print(f"  Switches: {len(switches)}")
    print(f"  Routers: {len(routers)}")
    print(f"  Other: {len(devices) - len(switches) - len(routers)}")
    print(f"\nSites: {len(sites)}")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
