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

import urllib3
import logging
import csv, os

import dnac
from dnac_devices import get_all_device_hostnames

from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

urllib3.disable_warnings(InsecureRequestWarning)


def string_check(temp_config, str1, str2):
    """
    The function will return all device hostnames and allows you to filter the devices
    :param temp_config: run config of the device
    :param str1, str2: strings to search for
    :return: search result for str1 and str2
    """
    if str1 in temp_config:
        str1_result = f"Contains: {str1}"
    else:
        str1_result = f"Not found: {str1}"

    if str2 in temp_config:
        str2_result = f"Contains: {str2}"
    else:
        str2_result = f"Not found: {str2}"

    return str1_result, str2_result


def main():
    if not os.path.exists('Serach_Files'):
        os.makedirs('Serach_Files')

    os.chdir('Serach_Files')
    logging.basicConfig(
        filename='application_search_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # enter the strings to search for in the device run configs below
    search_string1 = "10.10.10.10"
    search_string2 = "switchport mode trunk"

    today = datetime.now()
    filename = 'config_search_' +today.strftime('%d%m%Y') + '.csv'

    header = ['device', search_string1, search_string2]
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    if True:
        dnac_token = dnac.get_auth_token()
        all_devices_hostnames = get_all_device_hostnames(dnac_token)
        for device in all_devices_hostnames:
            print("**for the device:***\n ", device)

            try:
                device_run_config = dnac.get_output_command_runner('show running-config', device, dnac_token)
                str1, str2 = string_check(device_run_config, search_string1, search_string2)

                # save the result into a csv file
                data = [device, str1, str2]
                with open(filename, 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
            except:
                print(f"***For {device}: could not get the device run config")

    print('\n\n***End of Application Run***')


if __name__ == '__main__':
    print('**** Application config_search.py started ***\n'
          'This application will search for a specified string in the configuration of the device(s) and save the '
          'result in a csv file\n')
    main()
