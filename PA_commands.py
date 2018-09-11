import time
from weather import Weather, Unit

def get_date():
    return time.strftime("%a, %d %b %Y", time.gmtime())

def get_weather_forecast(location='tel aviv'):
    weather=Weather(unit=Unit.CELSIUS)
    location=weather.lookup_by_location(location)
    condition=location.condition
    message=[get_date(),condition.temp+"°C, "+condition.text]
    return message

def scream():
    message=""
    for i in range(500):
        message+="aaaaa"
    return message
