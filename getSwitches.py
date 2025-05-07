import csv
from catalystcentersdk import CatalystCenter

# Import credentials from settings file
from settings import CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL

# Connect to Catalyst Center using credentials from settings
catalyst = CatalystCenter(
    base_url=CATALYST_BASE_URL,
    username=CATALYST_USERNAME,
    password=CATALYST_PASSWORD
)

# Retrieve all network devices
devices = catalyst.device.get_all_network_devices().response

# Filter for switches (typically by 'family' or 'type')
switches = [d for d in devices if 'Switch' in d.get('family', '')]

# Prepare a mapping of siteId to site details (to avoid redundant API calls)
site_cache = {}

def get_site_details(site_id):
    if site_id in site_cache:
        return site_cache[site_id]
    site = catalyst.site.get_site(site_id=site_id).response
    site_cache[site_id] = site
    return site

# Prepare data for CSV
csv_data = []
for switch in switches:
    # Get site info
    site_id = switch.get('siteId')
    site_name = ''
    latitude = ''
    longitude = ''
    if site_id:
        site_info = get_site_details(site_id)
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

# Write to CSV
with open('cisco_switches.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'hostname', 'managementIpAddress', 'macAddress', 'serialNumber',
        'platformId', 'softwareVersion', 'role', 'site_name', 'latitude', 'longitude'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in csv_data:
        writer.writerow(row)

print("Exported switch details to cisco_switches.csv")
