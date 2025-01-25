import requests
from datetime import datetime, timedelta, timezone
import re

from config import WEATHER_CLIENT_SECRET


def extract_city(text):
    '''Extract city name from text using regular expressions'''

    text_patterns = {
        r'weather [a-z]{2,4} ([\w-]+(?:[\s|-]\w+)*)',
        r'weather (\w{3,})',
        r'forecast [a-z]{2,4} ([\w-]+(?:[\s|-]\w+)*)',
        r'forecast (\w{3,})',
        r'temperature [a-z]{2,4} ([\w-]+(?:[\s|-]\w+)*)',
        r'temperature (\w{3,})',
    }
    
    for pattern in text_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def get_weather_data(city):
    '''Display the weather information according to the city input by user'''
    
    weather_data = None
    # get city from user message

    if not WEATHER_CLIENT_SECRET:
        raise ValueError("API key is missing.")

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_CLIENT_SECRET}&units=metric'

    try:
        response = requests.get(url)
        print(response)

        if response.status_code == 200:
            data = response.json()
            print(f"request weather data, successful!")

            country = data['sys']['country']
            temperature = round(data['main']['temp'])
            feels_like = round(data['main']['feels_like'])
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = round(float(data['wind']['speed'])*3.6) # per Km/h
            clouds = data['clouds']['all'] # need to check percentage and display a reuls type :'cloudy, sunny' etc....

            # time zone data
            timezone_offset = data['timezone'] # in seconds
            city_timezone = timezone(timedelta(seconds=timezone_offset))
            
            sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=city_timezone) #  .strftime('%H:%M:%S ')
            sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=city_timezone) #   .strftime('%H:%M:%S (%p)')
            daylight_duration = sunset - sunrise # .strftime('%H:%M:%S')
            
            # calculate daylight duration in hours and minutes
            daylight_hours = daylight_duration.seconds // 3600
            daylight_minutes = (daylight_duration.seconds % 3600) // 60

            weather_data = {
                'city': city,
                'country': country,
                'temperature': temperature,
                'feels_like': feels_like,
                'description': description,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'sunrise': sunrise.strftime('%H:%M'),
                'sunset': sunset.strftime('%H:%M'),
                'clouds': clouds,
                'daylight_hours': daylight_hours,
                'daylight_minutes': daylight_minutes,
                
            }

            formatted_weather_data = format_weather_data(weather_data)

            return  formatted_weather_data
        else:
            return 'error. Failed to fetch weather data.'

    except Exception as e:
        print(f"Error occurred while fetching weather data: {str(e)}")
        return 'error. Failed to fetch weather data due to an error. please try again'


def format_weather_data(weather_data):
    '''Format the weather data in a readable format'''

    return (
        f"🌍  Here is the weather for:\n\n           {weather_data['city']} ({weather_data['country']})\n\n"
        f"🌡️  *Temperature*:   {weather_data['temperature']}°C\n"
        f"🌈  *Conditions*:   {weather_data['description']}\n"
        f"💧  *Humidity*:   {weather_data['humidity']}%\n"
        f"🌞  *Daylight*:   {weather_data['daylight_hours']}h:{weather_data['daylight_minutes']}min\n"
        f"🌅  *sunrise*:   {weather_data['sunrise']}\n"
        f"🌇  *sunset*:   {weather_data['sunset']}\n"
        f"🪁 *windspeed*: {weather_data['wind_speed']}Km/h\n" 
        )
