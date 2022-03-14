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
Sets a DGX node's boot once source setting via the Redfish API.

Call's the given node's Redfish API and sets it's boot once source setting.
"""

import traceback
import argparse
import redfish

def set_boot_source(nodes, username, password, boot_source):
    """
    Sets a DGX node's boot once source setting via the Redfish API"

    Args:
        nodes: A list of IPs or Hostnames for DGX node Redfish interfaces.
        username: Redfish API username.
        password: Redfish API password for the given username.
        boot_source: Boot source to boot once to.

    Raises:
        Exception: An error occurred applying the boot source.
    """

    system_self_url = '/redfish/v1/Systems/Self'

    # loop through nodes and set boot source
    for node in nodes:
        print("Setting boot source for node: " + node)

        try:
            # make a connection to the redfish api and login
            redfish_cxn = redfish.redfish_client(base_url='https://' + node,
                                                 username=username,
                                                 timeout=60,
                                                 password=password,
                                                 default_prefix='/redfish/v1')
            redfish_cxn.login(auth='session')

            # get the value of odata.etag from /redfish/v1/Systems/Self
            # this is needed for the If-Match precondition
            redfish_response = redfish_cxn.get(system_self_url, None)
            if redfish_response.status != 200:
                raise Exception("Error getting system data for node: " + node +
                                ". Redfish response status: " + str(redfish_response.status) + ".")

            odata_etag = ""
            if "@odata.etag" in redfish_response.dict:
                odata_etag = redfish_response.dict['@odata.etag']
            else:
                raise Exception("odata.etag key not present for node: " + node +
                                ". Redfish response: " + str(redfish_response))

            # set the boot source
            headers = {"If-Match": odata_etag, "Content-Type": "application/json"}
            body = {'Boot': {'BootSourceOverrideEnabled': 'Once',
                             'BootSourceOverrideTarget': boot_source}}

            redfish_response = redfish_cxn.patch(system_self_url,
                                                 headers=headers,
                                                 body=body)

            if redfish_response.status != 204:
                raise Exception("Error setting boot source for node: " + node +
                                ". Redfish response status: " + str(redfish_response.status) + ".")

            print("Successfully set boot source for node: " + node)
        except Exception: # pylint: disable=broad-except
            print("An error occurred setting boot source for node: " + node)
            traceback.print_exc()
        finally:
            try:
                redfish_cxn.logout()
            except Exception: # pylint: disable=broad-except
                pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set DGX boot once source.')
    parser.add_argument('-n', '--nodes', nargs='+',
                        required=True, help='DGX Redfish IP or Hostname')
    parser.add_argument('-u', '--username', type=str, action='store',
                        required=True, help='DGX Redfish username')
    parser.add_argument('-p', '--password', type=str, action='store',
                        required=True, help='DGX Redfish password')
    parser.add_argument('-s', '--boot_source', type=str, action='store',
                        choices=["Pxe", "Cd", "Usb", "Hdd", "BiosSetup"],
                        required=True, help='Boot source')
    args = parser.parse_args()

    set_boot_source(args.nodes, args.username, args.password, args.boot_source)
