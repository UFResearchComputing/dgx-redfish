# dgx-redfish

Description
----------
Python scripts for maintaining Nvidia DGX nodes using the Redfish API.

Requirements
----------
* python3.6+
* python-redfish-library

Installing
----------
* Install python-redfish-library. https://github.com/DMTF/python-redfish-library

```bash
$ pip install redfish
```

* Clone dgx-redfish

```bash
$ git clone git@github.com:UFResearchComputing/dgx-redfish.git
```

Usage
----------
```bash
$ python <script>.py --help
$ python dgx_get_bios_settings.py -n <dgx redfish interface> -u <dgx redfish username>
$ python dgx_get_bios_version.py -n <dgx redfish interface1> <dgx redfish interface2> -u <dgx redfish username>
$ python dgx_set_bios_settings.py -n <dgx redfish interface1> <dgx redfish interface2> -u <dgx redfish username> -f <dgx bios file>
$ python dgx_set_boot_once.py -n <dgx redfish interface1> <dgx redfish interface2> -u <dgx redfish username> -s <Pxe, Usb, Cd, Hdd, BiosSetup>
```

Copyright and License
---------------------

Copyright 2022 University of Florida Research Foundation, Inc. All Commercial Rights Reserved.

This project is covered under the [GNU General Public License V3](https://www.gnu.org/licenses/gpl-3.0.en.html).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.