import json
import pprint

import requests
from peewee import (
    Model,
    CharField,
    SqliteDatabase,
    IntegerField,
    ForeignKeyField,
    DeferredForeignKey,
)

db_file = "philips_hue.db"

db = SqliteDatabase(db_file)


class Bulb(Model):
    bridge = DeferredForeignKey("Bridge", lazy_load=True)
    index = IntegerField()
    name = CharField(null=True)
    guid = CharField(null=True)
    type = CharField()
    manufacturer = CharField()
    model = CharField()

    class Meta:
        database = db  # This model uses the "people.db" database.

    def api_call(self, **kwargs):
        endpoint = kwargs.get("endpoint", "")
        data = kwargs.get("data", False)

        retn = False
        if not self.bridge.username:
            call_url = "/".join([self.bridge.url, "api", endpoint])
        else:
            call_url = "/".join(
                [
                    self.bridge.url,
                    "api",
                    self.bridge.username,
                    "lights",
                    str(self.index),
                    endpoint,
                ]
            )

        ret = False
        if data:
            ret = requests.put(call_url, data=json.dumps(data))
        else:
            ret = requests.get(call_url)

        print(ret.text)

        if ret and ret.status_code == 200:
            retn = ret.json()

        return retn

    @property
    def status(self):

        return self.api_call()

    @property
    def is_on(self):

        return self.status.get("state").get("on")

    def brightness(self, brightness=False):
        if brightness:
            if isinstance(brightness, str) and "%" in brightness:
                brightness_percent = int(brightness.replace("%", ""))
                brightness = (brightness_percent * 255) / 100
            self.api_call(endpoint="state", data=dict(bri=int(brightness)))

        return self.status.get("state").get("bri")

    def toggle(self):
        if self.is_on:
            self.api_call(endpoint="state", data=dict(on=False))
        else:
            self.api_call(endpoint="state", data=dict(on=True))

        return self.is_on


class Bridge(Model):
    name = CharField(null=True)
    ip = CharField()
    serial_number = CharField()
    url = CharField()
    debug = CharField()
    device_id = CharField()
    appname = CharField(null=True)
    username = CharField(null=True)

    class Meta:
        database = db  # This model uses the "people.db" database.

    def api_call(self, **kwargs):
        endpoint = kwargs.get("endpoint", "")
        data = kwargs.get("data", False)

        retn = False
        if not self.username:
            call_url = "/".join([self.url, "api", endpoint])
        else:
            call_url = "/".join([self.url, "api", self.username, endpoint])

        ret = False
        if data:
            ret = requests.post(call_url, json=data)
        else:
            ret = requests.get(call_url)

        if ret and ret.status_code == 200:
            retn = ret.json()

        return retn

    def connect(self, appname, username=False):
        retn = False

        self.appname = appname

        if username:
            self.username = username

        else:
            responses = self.api_call(data={"devicetype": "%s" % appname})

            for response in responses:
                if response:
                    if "error" in response:
                        error = response.get("error")
                        retn = "%s: %s" % (error.get("type"), error.get("description"))

                    if "success" in response:
                        response_data = response.get("success")

                        self.username = response_data.get("username", "None")
                        retn = True

        self.save()

        return retn

    def lights(self):
        response = self.api_call(endpoint="lights")

        bulb_ids = []
        bulbs = Bulb.filter(bridge=self)
        for bulb in bulbs:
            bulb_ids.append(bulb.guid)

        for light_index, light_details in response.items():
            guid = light_details.get("uniqueid")
            if guid not in bulb_ids:
                Bulb.create(
                    bridge=self,
                    index=int(light_index),
                    name=light_details.get("name"),
                    guid=guid,
                    type=light_details.get("type"),
                    manufacturer=light_details.get("manufacturername"),
                    model=light_details.get("modelid"),
                )
                bulb_ids.append(guid)

        bulbs = Bulb.filter(bridge=self)

        return bulbs


db.connect()

models = [Bridge, Bulb]

for model in models:
    if not db.table_exists(model):
        db.create_tables([model])
