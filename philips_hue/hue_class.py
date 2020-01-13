import pprint
import re

import requests
import upnpclient

from philips_hue.models import Bridge


def discover_hue(**kwargs):
    cloud = kwargs.get("cloud", False)
    upnp = kwargs.get("upnp", True)

    bridges = Bridge.select()

    bridge_addresses = []
    for bridge in bridges:
        bridge_addresses.append(bridge.ip)

    if cloud:
        devices_resp = requests.get("https://discovery.meethue.com/")

        if devices_resp.status_code == 200:
            devices = devices_resp.json()
            for device in devices:
                ip_address = device.get("internalipaddress")
                urlbase = "http://%s:80" % ip_address
                debug_address = "%s/debug/clip.html" % urlbase

                if ip_address not in bridge_addresses:
                    new_bridge = Bridge.create(
                        name="Philips Hue Bridge",
                        ip=ip_address,
                        serial_number=device.get("id"),
                        url=urlbase,
                        debug=debug_address,
                        device_id=device.get("id"),
                    )
                    bridge_addresses.append(ip_address)

    if upnp:
        devices = upnpclient.discover()
        for device in devices:
            if "Philips hue" in device.friendly_name:
                urlbase = device.location.replace("/description.xml", "")
                ip_address = re.search(
                    r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", urlbase
                ).group(1)
                debug_address = "%s/debug/clip.html" % urlbase

                if ip_address not in bridge_addresses:
                    new_bridge = Bridge.create(
                        name=device.friendly_name,
                        ip=ip_address,
                        serial_number=device.serial_number,
                        url=urlbase,
                        debug=debug_address,
                        device_id=device.serial_number,
                    )
                    bridge_addresses.append(ip_address)

    bridges = Bridge.select()

    return bridges


bridges = discover_hue(cloud=True, upnp=False)
for bridge in bridges:
    bridge.connect("test")

    for light in bridge.lights():
        if light.name == "Floor lamp":
            print(light.name)
            light.toggle()

            if light.is_on:
                for x in range(0, 255):
                    light.brightness(x)
