'''
Copyright(c) 2021 Cisco and / or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
https: // developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

import dnac

def get_all_device_hostnames(dnac_token):
    """
    The function will return all device hostnames and allows you to filter the devices
    :param dnac_token: DNA C token
    :return: DNA C device hostnames
    """
    all_devices_info = dnac.get_all_device_info(dnac_token)
    all_devices_hostnames = []

    for device in all_devices_info:
        if device['family'] == 'Switches and Hubs' or device['family'] == 'Routers':
            '''
            device['softwareType'] =  'IOS-XE'
            device['softwareVersion'] = '17.4.1b'
            device['locationName'] =  None
            device['location'] =  None
            '''
            all_devices_hostnames.append(device['hostname'])

    return all_devices_hostnames
