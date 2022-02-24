# Copyright 2022 University of Florida Research Foundation, Inc. All Commercial Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Sets a DGX node's BIOS settings via the Redfish API.

Call's the given node's Redfish API and sets it's BIOS settings.
Takes in a file with the BIOS settings to apply.
"""

import argparse
import redfish

def set_bios_settings(nodes, username, password, settings_file):
    """
    Sets a DGX node's BIOS settings via the Redfish API"

    Args:
        nodes: A list of IPs or Hostnames for DGX node Redfish interfaces.
        username: Redfish API username.
        password: Redfish API password for the given username.
        settings_file: BIOS settings file to apply.

    Raises:
        Exception: An error occurred applying the BIOS settings.
    """

    # read in settings file
    bios_settings = {"Attributes": {}}
    with open(settings_file, 'r', encoding='utf8') as bios_settings_file:
        for line in bios_settings_file:
            if '=' in line:
                bios_setting = line.strip().split('=')

                bios_setting_key = bios_setting[0]
                bios_setting_value = bios_setting[1]

                if bios_setting_value.isnumeric():
                    bios_setting_value = int(bios_setting_value)

                bios_settings['Attributes'][bios_setting_key] = bios_setting_value

    # loop through nodes and set bios settings
    for node in nodes:
        print("Setting bios settings for node: " + node)

        # make a connection to the redfish api and login
        redfish_cxn = redfish.redfish_client(base_url='https://' + node,
                                             username=username,
                                             timeout=60,
                                             password=password,
                                             default_prefix='/redfish/v1')
        redfish_cxn.login(auth='session')

        # set the bios settings
        headers = {"If-Match": "*", "Content-Type": "application/json"}
        redfish_response = redfish_cxn.patch('/redfish/v1/Systems/Self/Bios/SD',
                                             headers=headers,
                                             body=bios_settings)

        if redfish_response.status != 204:
            raise Exception("Error setting bios settings for node: " + node +
                            ". Redfish response: " + str(redfish_response))

        print("Successfully set bios settings for node: " + node)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set DGX Bios settings.')
    parser.add_argument('-n', '--nodes', nargs='+',
                        required=True, help='DGX Redfish IP or Hostname')
    parser.add_argument('-u', '--username', type=str, action='store',
                        required=True, help='DGX Redfish username')
    parser.add_argument('-p', '--password', type=str, action='store',
                        required=True, help='DGX Redfish password')
    parser.add_argument('-f', '--file', type=str, action='store',
                        required=True, help='BIOS settings in file format')
    args = parser.parse_args()

    set_bios_settings(args.nodes, args.username, args.password, args.file)
