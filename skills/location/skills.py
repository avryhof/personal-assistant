import settings
from devices.location.device import GeoIP
from personal_assistant.assistant_skill_class import AssistantSkill
from utilities.utility_functions import is_empty


class DateSkill(AssistantSkill):
    name = "Date Skill"
    utterances = [
        "what is the date",
        "what date is it",
        "what is today's date",
        "what is today",
    ]
    now = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if is_empty(getattr(settings, "LOCATION")):
            self.log("Updating Location")
            g = GeoIP()
            g.get_location()
            setattr(settings, "LOCATION", g)

        self.now = settings.LOCATION.get_local_time()

    def dom_word(self):
        dom_parts = []

        dom_str = self.now.strftime("%d")
        dom = int(dom_str)

        if dom == 10:
            dom_parts.append("tenth")

        elif dom == 20:
            dom_parts.append("twentieth")

        elif dom_parts == 30:
            dom_parts.append("thirtieth")

        elif dom > 19:
            tens_place = int(dom_str[0])
            dom = int(dom_str[1])

            if tens_place == 2:
                dom_parts.append("twenty")

            elif tens_place == 3:
                dom_parts.append("thirty")

        if dom == 1:
            dom_parts.append("first")
        if dom == 2:
            return "second"
        if dom == 3:
            return "third"
        if dom == 4:
            return "fourth"
        if dom == 5:
            return "fifth"
        if dom == 6:
            return "sixth"
        if dom == 7:
            return "seventh"
        if dom == 8:
            return "eighth"
        if dom == 9:
            return "ninth"
        if dom == 10:
            return "tenth"
        if dom == 11:
            dom_parts.append("eleventh")
        if dom == 12:
            return "twelfth"
        if dom == 13:
            return "thirteenth"
        if dom == 14:
            return "fourteenth"
        if dom == 15:
            return "fifteenth"
        if dom == 16:
            return "sixteenth"
        if dom == 17:
            return "seventeenth"
        if dom == 18:
            return "eightteenh"
        if dom == 19:
            return "nineteenth"

        return " ".join(dom_parts)

    def handle(self):
        dow = self.now.strftime("%A")
        month = self.now.strftime("%B")
        dom = self.dom_word()
        century = self.now.strftime("%Y")[0:2]
        year = self.now.strftime("%Y")[2:4]

        if self.dumb:
            phrase = f"{dow}, {month} {self.now.day}, {century}{year}"

        else:
            phrase = f"{dow}, {month} {dom} {century} {year}"

        self.log("Saying: {}".format(phrase))
        self.speak(phrase)

        return True


class LocationSkill(AssistantSkill):
    name = "Location Skill"
    utterances = [
        "where am I",
        "where are we",
        "what is this location",
        "what is the location",
        "what city are we in",
        "what city am I in",
        "what town are we in",
        "what town am I in",
    ]

    now = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if is_empty(getattr(settings, "LOCATION")):
            self.log("Updating Location")
            g = GeoIP()
            g.get_location()
            setattr(settings, "LOCATION", g)

    def handle(self):
        if self.dumb:
            phrase = f"{settings.LOCATION.city}, {settings.LOCATION.state} {settings.LOCATION.zip_code}"
        else:
            phrase = f"{settings.LOCATION.city} {settings.LOCATION.state_name}"

        self.log("Saying: {}".format(phrase))
        self.speak(phrase)

        return True


class TimeSkill(AssistantSkill):
    name = "Time Skill"
    utterances = ["what is the time", "what time is it"]

    now = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if is_empty(getattr(settings, "LOCATION")):
            self.log("Updating Location")
            g = GeoIP()
            g.get_location()
            setattr(settings, "LOCATION", g)

        self.now = settings.LOCATION.get_local_time()

    def handle(self):
        hour = self.now.hour
        if hour > 12:
            hour = hour - 12

        minute = self.now.minute
        ap = self.now.strftime("%p")

        ap = f"{ap[0]} {ap[1]}"

        if minute < 10:
            minute = f"oh {minute}"

        if self.dumb:
            phrase = "{}:{} {}".format(hour, minute, self.now.strftime("%p"))

        else:
            phrase = f"{hour} {minute} {ap}"

        self.log("Saying: {}".format(phrase))
        self.speak(phrase)

        return True


class WeatherSkill(AssistantSkill):
    name = "Weather Skill"
    utterances = [
        "what is the weather",
    ]

    now = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if is_empty(getattr(settings, "LOCATION")):
            self.log("Updating Location")
            g = GeoIP()
            g.get_location()
            setattr(settings, "LOCATION", g)

    def handle(self):
        weather = settings.LOCATION.get_weather()
        phrase = f"The current conditions are {weather.description} " \
                 f"and {int(round(weather.temperature__ferenheight, 0))} degrees. " \
                 f"The wind is {weather.wind_direction__words} " \
                 f"at {int(round(weather.wind_speed__mph, 0))} miles per hour."

        self.log("Saying: {}".format(phrase))
        self.speak(phrase)

        return True
