import pprint

from netdisco.discovery import NetworkDiscovery

netdis = NetworkDiscovery()

netdis.scan()

for dev in netdis.discover():
    print(dev)
    pprint.pprint(netdis.get_info(dev))
    print("-" * 80)

netdis.stop()
