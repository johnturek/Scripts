#!/usr/bin/env python3
"""
Utility functions for Catalyst Center scripts.

Common functions used across multiple scripts for connection management,
data processing, and export operations.
"""

import sys
import logging
from typing import Dict, List, Any, Optional, Tuple
from catalystcentersdk import CatalystCenter
from catalystcentersdk.exceptions import ApiError

logger = logging.getLogger(__name__)


def load_settings() -> Tuple[str, str, str]:
    """
    Load settings from settings.py file.
    
    Returns:
        Tuple of (username, password, base_url)
    
    Raises:
        SystemExit: If settings file is not found or invalid
    """
    try:
        from settings import CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
        return CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
    except ImportError:
        logger.error("Settings file not found. Please create settings.py from settings.py.example")
        sys.exit(1)
    except AttributeError as e:
        logger.error(f"Missing required configuration in settings.py: {e}")
        sys.exit(1)


def connect_to_catalyst(
    username: str,
    password: str,
    base_url: str,
    verify: bool = True
) -> CatalystCenter:
    """
    Establish connection to Catalyst Center.
    
    Args:
        username: Catalyst Center username
        password: Catalyst Center password
        base_url: Catalyst Center base URL
        verify: Whether to verify SSL certificates
        
    Returns:
        Connected Catalyst Center client
        
    Raises:
        SystemExit: If connection fails
    """
    try:
        logger.info("Connecting to Catalyst Center...")
        catalyst = CatalystCenter(
            base_url=base_url,
            username=username,
            password=password,
            verify=verify
        )
        logger.info("Successfully connected to Catalyst Center")
        return catalyst
    except Exception as e:
        logger.error(f"Failed to connect to Catalyst Center: {e}")
        sys.exit(1)


def get_all_devices(catalyst: CatalystCenter) -> List[Dict[str, Any]]:
    """
    Retrieve all network devices.
    
    Args:
        catalyst: Connected Catalyst Center client
        
    Returns:
        List of all network devices
    """
    try:
        logger.info("Retrieving all network devices...")
        devices = catalyst.device.get_all_network_devices().response
        logger.info(f"Found {len(devices)} total devices")
        return devices
    except ApiError as e:
        logger.error(f"API error while retrieving devices: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while retrieving devices: {e}")
        return []


def filter_devices_by_family(devices: List[Dict[str, Any]], family: str) -> List[Dict[str, Any]]:
    """
    Filter devices by family type.
    
    Args:
        devices: List of device dictionaries
        family: Device family to filter for (e.g., 'Switch', 'Router')
        
    Returns:
        Filtered list of devices
    """
    filtered = [d for d in devices if family in d.get('family', '')]
    logger.info(f"Filtered {len(filtered)} {family} devices from {len(devices)} total")
    return filtered


def get_site_info(
    catalyst: CatalystCenter,
    site_id: str,
    cache: Optional[Dict[str, Dict]] = None
) -> Dict[str, Any]:
    """
    Get site information with optional caching.
    
    Args:
        catalyst: Connected Catalyst Center client
        site_id: Site identifier
        cache: Optional cache dictionary to avoid redundant API calls
        
    Returns:
        Site information dictionary
    """
    if cache is not None and site_id in cache:
        return cache[site_id]
    
    try:
        site = catalyst.site.get_site(site_id=site_id).response
        if cache is not None:
            cache[site_id] = site
        return site
    except ApiError as e:
        logger.warning(f"Failed to retrieve site details for {site_id}: {e}")
        return {}
    except Exception as e:
        logger.warning(f"Unexpected error retrieving site {site_id}: {e}")
        return {}


def get_device_health(catalyst: CatalystCenter, device_id: str) -> Dict[str, Any]:
    """
    Get device health information.
    
    Args:
        catalyst: Connected Catalyst Center client
        device_id: Device identifier
        
    Returns:
        Device health information
    """
    try:
        health = catalyst.devices.get_device_health(device_id=device_id).response
        return health
    except ApiError as e:
        logger.warning(f"Failed to retrieve health for device {device_id}: {e}")
        return {}
    except Exception as e:
        logger.warning(f"Unexpected error retrieving health for device {device_id}: {e}")
        return {}


def format_uptime(uptime_str: str) -> str:
    """
    Format uptime string to be more readable.
    
    Args:
        uptime_str: Raw uptime string from API
        
    Returns:
        Formatted uptime string
    """
    if not uptime_str:
        return ""
    
    # Simple formatting - can be enhanced
    return uptime_str.strip()


def validate_ip_address(ip: str) -> bool:
    """
    Validate IP address format.
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid IP address format
    """
    import ipaddress
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_get_nested(dictionary: Dict, *keys, default=None) -> Any:
    """
    Safely get nested dictionary values.
    
    Args:
        dictionary: Dictionary to search
        *keys: Keys to traverse
        default: Default value if key not found
        
    Returns:
        Value at nested key or default
    """
    value = dictionary
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            return default
    return value if value is not None else default
