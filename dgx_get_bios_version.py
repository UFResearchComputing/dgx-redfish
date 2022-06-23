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
Gets a DGX node's BIOS version via the Redfish API.

Call's the given node's Redfish API and queries for it's BIOS version.
If successfull the BIOS version is printed to the screen.
"""

import traceback
import argparse
import getpass
import collections
import redfish

def get_bios_versions(nodes, username, password):
    """
    Gets a DGX node's BIOS version via the Redfish API"

    Args:
        nodes: A list of IPs or Hostnames for DGX node Redfish interfaces.
        username: Redfish API username.
        password: Redfish API password for the given username.

    Returns:
        A dictionary mapping of BIOS versions returned from the Redfish API.

    Raises:
        Exception: An error occurred obtaining the BIOS version.
    """
    bios_versions = {}

    # loop through nodes and get bios versions
    for node in nodes:
        try:
            # make a connection to the redfish api and login
            redfish_cxn = redfish.redfish_client(base_url='https://' + node,
                                                 username=username,
                                                 timeout=60,
                                                 password=password,
                                                 default_prefix='/redfish/v1')
            redfish_cxn.login(auth='session')

            # get the bios version
            redfish_response = redfish_cxn.get('/redfish/v1/Systems/Self', None)

            if redfish_response.status != 200:
                raise Exception("Error getting bios version for node: " + node +
                                ". Redfish response: " + str(redfish_response))

            bios_versions[node] = redfish_response.dict['BiosVersion']
        except Exception: # pylint: disable=broad-except
            print("An error occurred getting bios version for node: " + node)
            traceback.print_exc()
        finally:
            try:
                redfish_cxn.logout()
            except Exception: # pylint: disable=broad-except
                pass
    return bios_versions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get DGX Bios versions.')
    parser.add_argument('-n', '--nodes', nargs='+',
                        required=True, help='DGX Redfish IPs or Hostnames')
    parser.add_argument('-u', '--username', type=str, action='store',
                        required=True, help='DGX Redfish username')
    args = parser.parse_args()

    redfish_password = getpass.getpass()

    redfish_bios_versions = collections.OrderedDict(sorted(get_bios_versions(args.nodes,
                                                    args.username, redfish_password).items()))
    for key, value in redfish_bios_versions.items():
        print(key + ": " + value)
