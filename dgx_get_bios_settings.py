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
Gets a DGX node's BIOS settings via the Redfish API.

Call's the given node's Redfish API and queries for it's BIOS settings.
If successfull the BIOS settings are printed to the screen.
"""

import argparse
import redfish

def get_bios_settings(node, username, password):
    """
    Gets a DGX node's BIOS settings via the Redfish API"

    Args:
        node: An IP or Hostname for a DGX node's Redfish interface.
        username: Redfish API username.
        password: Redfish API password for the given username.

    Returns:
        A dictionary mapping of BIOS settings returned from the Redfish API.

    Raises:
        Exception: An error occurred obtaining the BIOS settings.
    """

    # make a connection to the redfish api and login
    redfish_cxn = redfish.redfish_client(base_url='https://' + node,
                                         username=username,
                                         timeout=60,
                                         password=password,
                                         default_prefix='/redfish/v1')
    redfish_cxn.login(auth='session')

    # get the bios settings
    redfish_response = redfish_cxn.get('/redfish/v1/Systems/Self/Bios', None)

    if redfish_response.status != 200:
        raise Exception("Error getting bios settings for node: " + node +
                        ". Redfish response: " + str(redfish_response))

    return redfish_response.dict['Attributes']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get DGX Bios settings.')
    parser.add_argument('-n', '--node', type=str, action='store',
                        required=True, help='DGX Redfish IP or Hostname')
    parser.add_argument('-u', '--username', type=str, action='store',
                        required=True, help='DGX Redfish username')
    parser.add_argument('-p', '--password', type=str, action='store',
                        required=True, help='DGX Redfish password')
    args = parser.parse_args()

    print("Getting bios settings for node: " + args.node)

    bios_settings = get_bios_settings(args.node, args.username, args.password)

    for key, value in bios_settings.items():
        print(key + ": " + str(value))
