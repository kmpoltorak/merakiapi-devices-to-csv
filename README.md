# Overview
This script is created for gathering information about all Cisco Meraki devices in all Organizations acessible via the user API key. It builds a list of entries and  saves all of them in a CSV format file.
Script will verify if there is API enabled or not in the Merkai dashboard for certain account.

# Prerequirements
* Enabled API in the Meraki dashboard (**Organization >> Configure >> Settings >> Dashboard API access >>  Enable access to the Cisco Meraki Dashboard API**)
* Generate user API key and copy from Meraki dashboard into **config.py** file (```API_KEY = 'PASTE_YOUR_MERAKI_API_KEY_HERE'```)
* Install all needed packages with: ```pip3 install -r requirements.txt```
* Installed Python3 (my version was 3.8 and all was working fine)

How to generate Meraki user API key:
https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API

# Troubleshooting
If there are any issues you can simply turn on debugging in **config.py** file by changing **OUTPUT_LOG** constant to **True** and it will create log file after script run.

# Script output
In the output you should obtain file named **meraki_devices.csv** with statement of all the ogranization/network/devices in such format:

```
organization_name,network_name,device_name,device_model,device_serial,device_IP
```

# Known errors
* "Organizations, getOrganizations - 404 Not Found, please wait a minute if the key or org was just newly created." - verify if the API key is fine. The API key works approximately 5 minutes after its creation. It can be also old user API key.

# Meraki API knowledge base
https://dashboard.meraki.com/api_docs/v0 (there is also v1 version https://dashboard.meraki.com/api_docs/v1)
