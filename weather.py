import requests
import json
from pprint import pprint
from datetime import datetime, timedelta


def get_weather():
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=37.8807787&lon=-122.09509510000001&units=imperial&appid=2d437a6de5acb92ba7ad7c205b3d8b4e'
    response = requests.get(url)
    response_json = response.json()

    weather_list = []
    list = []
    for x in response_json['daily']:
        day = datetime.fromtimestamp(x['dt']).strftime('%a, %dth')
        temp = x['temp']['day']
        temp_min = str(x['temp']['min'])
        temp_max = str(x['temp']['max'])
        icon = x['weather'][0]['icon']
        list = [day, temp, temp_max, temp_min, icon]
        weather_list.append(list)
    return weather_list
