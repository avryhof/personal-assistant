from devices.location.device import GeoIP

g = GeoIP()
# g.update_db()

g.get_location()

# print(g.data)
# pprint.pprint(g.data.city.name)
# pprint.pprint(g.data.location.time_zone)
# pprint.pprint(g.data.postal.code)
# pprint.pprint(g.data.subdivisions[0].iso_code)
# pprint.pprint(g.data.subdivisions[0].name)
# pprint.pprint(g.data.location.latitude, g.data.location.longitude)
# print(g.data.country.iso_code)
# print(g.data.location)

weather = g.get_weather()

print(
    f"The current conditions are {weather.description} and {weather.temperature__ferenheight} degrees.  "
    f"The wind direction is {weather.wind_direction__words}"
)
