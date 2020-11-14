import pprint

import upnpclient

devices = upnpclient.discover()
for device in devices:
    print(device.friendly_name)
    print(device.location)
    # print(dir(device))
    print("-" * 80)
