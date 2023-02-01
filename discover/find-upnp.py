import pprint
from urllib.parse import urlsplit
from urllib.request import urlretrieve

import requests
import upnpclient
import xmltodict as xmltodict

devices = upnpclient.discover()
for device in devices:
    print(device.friendly_name)
    print(device.location)
    print(urlsplit(device.location))
    pprint.pprint(xmltodict.parse(requests.get(device.location).text))
    print("-" * 80)
