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

import os
import os.path
import difflib

import urllib3
import logging

import dnac
from dnac_devices import get_all_device_hostnames

from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


def compare_configs(cfg1, cfg2):
    """
    The function will return all device hostnames and allows you to filter the devices
    :param cfg1: run config of the device
    :param cfg2: saved run config of the device
    :return: config changes
    """
    f1 = open(cfg1, 'r')
    old_cfg = f1.readlines()
    f1.close()

    f2 = open(cfg2, 'r')
    new_cfg = f2.readlines()
    f2.close()

    # compare the two specified config files {cfg1} and {cfg2}
    d = difflib.unified_diff(old_cfg, new_cfg, n=9)

    # create a diff_list that will include all the lines that changed
    # create a diff_output string that will collect the generator output from the unified_diff function
    diff_list = []
    diff_output = ''

    for line in d:
        diff_output += line
        if line.find('Current configuration') == -1:
            if line.find('Last configuration change') == -1:
                if (line.find('+++') == -1) and (line.find('---') == -1):
                    if (line.find('-!') == -1) and (line.find('+!') == -1):
                        if line.startswith('+'):
                            diff_list.append('\n' + line)
                        elif line.startswith('-'):
                            diff_list.append('\n' + line)

    # process the diff_output to select only the sections between '!' characters for the sections that changed,
    # replace the empty '+' or '-' lines with space
    diff_output = diff_output.replace('+!', '!')
    diff_output = diff_output.replace('-!', '!')
    diff_output_list = diff_output.split('!')

    all_changes = []

    for changes in diff_list:
        for config_changes in diff_output_list:
            if changes in config_changes:
                if config_changes not in all_changes:
                    all_changes.append(config_changes)

    # create a config_text string with all the sections that include changes
    config_text = ''
    for items in all_changes:
        config_text += items

    return config_text


def check_config_difference(diff, device, change_log):
    """
    The function will save the config difference into the change log file
    :param diff: the diff between the config files
    :param device: dna device
    :change_log: file to save the change diff
    :return: None
    """
    short_description = 'Configuration Change Alert - ' + device
    updated_comment = short_description + '\nThe configuration changes are: \n' + diff

    change_log_file = open(change_log, "a")

    change_log_file.write(updated_comment)
    change_log_file.write("\n***********\n")

    change_log_file.seek(0)
    change_log_file.close()

    # search for certain changes in config of the device
    # in the code below the string 'ntp server' is searched for in the devices
    # the devices with the ntp server change will be logged into a text file
    if 'ntp server' in diff:
        ntp_comment = 'NTP Sever Change Alert - ' + device + '\n'
    else:
        ntp_comment = '\nPassed NTP Server check'

    f_diff = open('ntp_server_change.txt', 'a')
    f_diff.write(ntp_comment)
    f_diff.seek(0)
    f_diff.close()
    return None


def main():
    if not os.path.exists('Config_Files'):
        os.makedirs('Config_Files')

    os.chdir('Config_Files')

    logging.basicConfig(
        filename='application_monitoring_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    change_log = 'change_log.txt'

    if True:
        temp_run_config = 'temp_run_config.txt'
        dnac_token = dnac.get_auth_token()
        all_devices_hostnames = get_all_device_hostnames(dnac_token)

        for device in all_devices_hostnames:
            print("**for the device:***\n ", device)

            try:
                device_run_config = dnac.get_output_command_runner('show running-config', device, dnac_token)

                filename = str(device) + '_run_config.txt'
                f_temp = open(temp_run_config, 'w')
                f_temp.write(device_run_config)
                f_temp.seek(0)  # reset the file pointer to 0
                f_temp.close()

                if os.path.isfile(filename):
                    diff = compare_configs(filename, temp_run_config)
                    if diff != '':
                        check_config_difference(diff, device, change_log)
                    else:
                        print('Device: ' + device + ' - No configuration changes detected')
                else:
                    # new device discovered, save the running configuration to a file in the folder with the name
                    f_config = open(filename, 'w')
                    f_config.write(device_run_config)
                    f_config.seek(0)
                    f_config.close()
                    print('Device: ' + device + ' - New device discovered')
            except:
                print('***Device: ' + device + ' - Could not get the device config')

    print('\n\nEnd of Application Run')


if __name__ == '__main__':
    print('**** Application config_mon.py started ***\n'
          'This application will save the device configurations as text files under the Config_Files folder, '
          'If the device configuration exists the program will generate a comparision of the configurations\n')
    main()
