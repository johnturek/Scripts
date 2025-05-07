import csv
import json
from catalystcentersdk import CatalystCenter

catalyst = CatalystCenter()

# --- 1. Get all devices (switches) ---
devices = catalyst.device.get_all_network_devices().response
switches = [d for d in devices if 'Switch' in d.get('family', '')]

# --- 2. Get all sites ---
sites = catalyst.site.get_all_sites().response

# --- 3. Get all IP subnets (IP pools) ---
ip_pools = catalyst.network_settings.get_all_ip_pools().response

# --- Export raw data for switches ---
with open('all_switches_raw.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['raw_json'])
    for switch in switches:
        writer.writerow([json.dumps(switch)])

# --- Export raw data for sites ---
with open('all_sites_raw.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['raw_json'])
    for site in sites:
        writer.writerow([json.dumps(site)])

# --- Export raw data for IP subnets ---
with open('all_ip_subnets_raw.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['raw_json'])
    for pool in ip_pools:
        writer.writerow([json.dumps(pool)])

print("Exported raw data for switches, sites, and IP subnets to CSV files.")
