#!/usr/bin/python3

# Import packages
import meraki
import requests

# Import constants from configuration file
from config import *

"""
Script is gathering data from Meraki API about all organizations, networks and devices and write them to CSV file.
Successful on minimum Python 3.8.
"""


# Function verifies if the API for organization is turned on and is the API key good by returning the HTML response status code
def verify_api_status_code(organization_id):
    # Meraki API key header
    headers = {'X-Cisco-Meraki-API-Key': API_KEY}
    # Getting status code from HTML API request i.e. 200, 404
    status_code = requests.get(DEFAULT_BASE_URL + "/organizations/" + organization_id + "/networks",
                               headers=headers).status_code
    return status_code


def main():
    # Initiate Meraki dashboard API session
    dashboard = meraki.DashboardAPI(
        api_key=API_KEY,
        base_url=DEFAULT_BASE_URL,
        log_file_prefix=LOG_FILE_PREFIX,
        log_path=LOG_PATH,
        output_log=OUTPUT_LOG,
        print_console=PRINT_TO_CONSOLE
        # add more if needed
    )

    # List variable for found devices to generate CSV file
    device_list = ["organization_name,network_name,device_name,device_model,device_serial,device_IP"]

    # Python test block
    try:
        print("Starting scan...")
        # Get list of organizations
        organizations = dashboard.organizations.getOrganizations()
        # For each organization verify API and list networks
        for organization in organizations:
            # If the status code is equal to 200 API is working fine
            if verify_api_status_code(organization["id"]) == 200:
                networks = dashboard.networks.getOrganizationNetworks(organization["id"])
                # For each network in organization list all the devices
                for network in networks:
                    devices = dashboard.devices.getNetworkDevices(network["id"])
                    # For each device append to the list with certain values
                    for device in devices:
                        # If the device have name use name
                        if "name" in device:
                            # Check if the device IP address is not None
                            if device["lanIp"] is not None:
                                device_list.append(organization["name"] + ',' + network["name"] + ',' +
                                                   device["name"] + ',' + device["model"] + ',' +
                                                   device["serial"] + ',' + device["lanIp"])
                            # Else write None instead of IP
                            else:
                                device_list.append(organization["name"] + ',' + network["name"] + ',' +
                                                   device["name"] + ',' + device["model"] + ',' +
                                                   device["serial"] + ',' + "None")
                        # If device don't have name use its mac address as name
                        else:
                            # Check if the device IP address is not None
                            if device["lanIp"] is not None:
                                device_list.append(organization["name"] + ',' + network["name"] + ',' +
                                                   device["mac"] + ',' + device["model"] + ',' +
                                                   device["serial"] + ',' + device["lanIp"])
                            # Else write None instead of IP
                            else:
                                device_list.append(organization["name"] + ',' + network["name"] + ',' +
                                                   device["mac"] + ',' + device["model"] + ',' +
                                                   device["serial"] + ',' + "None")
            else:
                # Print information if the API connection will fail
                print(f'WARNING: For organization "{organization["name"]}" API is not enabled or there is bad API key.')
        # Write all data from the list to CSV format file line by line
        file = open(OUTPUT_FILENAME, "w")
        for row in device_list:
            file.write(row + "\n")
        # Close the file
        file.close()
        print("File created")
    # Print other errors that can occur
    except Exception as e:
        print(f"ERROR: {e}")


# Run the script
if __name__ == '__main__':
    main()
