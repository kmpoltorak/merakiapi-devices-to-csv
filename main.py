#!/usr/bin/python

# Import packages
import meraki
import requests

# Import constants from configuration file
import config


def verify_api_status_code(organization_id):
    """Function verifies if the API for organization is turned on and is the API key good by returning the HTML response status code"""
    
    # Meraki API key header
    headers = {'X-Cisco-Meraki-API-Key': config.API_KEY}
    # Getting status code from HTML API request i.e. 200, 404
    status_code = requests.get(config.DEFAULT_BASE_URL + "/organizations/" + organization_id + "/networks", headers=headers, timeout=10).status_code
    return status_code


def main():
    """
    Script is gathering data from Meraki API about all organizations, networks and devices and write them to CSV file
    """
    
    # Initiate Meraki dashboard API session
    dashboard = meraki.DashboardAPI(
        api_key=config.API_KEY,
        base_url=config.DEFAULT_BASE_URL,
        log_file_prefix=config.LOG_FILE_PREFIX,
        log_path=config.LOG_PATH,
        output_log=config.OUTPUT_LOG,
        print_console=config.PRINT_TO_CONSOLE
        # add more if needed
    )

    # List variable for found devices to generate CSV file
    device_list = ["organization_name,network_name,device_name,device_model,device_serial,device_IP"]

    try:
        print("Starting scan...")
        # Get list of organizations
        organizations = dashboard.organizations.getOrganizations()
        # For each organization verify API and list networks
        for organization in organizations:
            # If the status code is equal to 200 API is working fine
            if verify_api_status_code(organization["id"]) == 200:
                networks = dashboard.organizations.getOrganizationNetworks(organization["id"])
                # For each network in organization list all the devices
                for network in networks:
                    devices = dashboard.networks.getNetworkDevices(network["id"])
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
        with open(config.OUTPUT_FILENAME, "w", encoding="utf-8") as file:
            for _ in device_list:
                file.write(_ + "\n")
        # Close the file
        file.close()
        print("File created")
        
    # Print other errors that can occur
    except Exception as e:
        print(f"ERROR: {e}")


# Run the script
if __name__ == '__main__':
    main()
