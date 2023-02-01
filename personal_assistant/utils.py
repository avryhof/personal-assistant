from urllib.parse import urlsplit

import peewee
import upnpclient
from netdisco.discovery import NetworkDiscovery

from personal_assistant.models import Device
from utilities.debugging import log_message
from utilities.utility_functions import is_empty

netdis = NetworkDiscovery()


def find_devices():
    netdis.scan()

    for dev in netdis.discover():
        info = netdis.get_info(dev)
        try:
            device = Device.get(ip_address=info.get("host"), port=info.get("port"))
        except peewee.DoesNotExist:
            log_message(
                f"Found device: {info.get('host')}:{info.get('port')} - {info.get('name')}"
            )
            device = Device.create(ip_address=info.get("host"), port=info.get("port"))

        device.name = info.get("name")
        device.service = str(dev)
        device.save()

    netdis.stop()

    upnp_devices = upnpclient.discover()
    for upnp_device in upnp_devices:
        addr = urlsplit(upnp_device.location)
        ip, port = addr.netloc.split(":")

        try:
            device = Device.get(ip_address=ip, port=int(port))
        except peewee.DoesNotExist:
            log_message(f"Found device: {ip}:{port} - {upnp_devices.friendly_name}")
            device = Device.create(ip_address=ip, port=int(port))
        else:
            log_message(f"Update device: {ip}:{port} - {upnp_devices.friendly_name}")

        if is_empty(device.name):
            device.name = str(upnp_device.friendly_name)

        device.save()
