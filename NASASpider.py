import requests
import sqlite3
import json
import os.path

# Global variables
API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = 'Asteroids_NASA.db'


def get_asteroids_data(start_date, end_date=''):
    # date form: yyyy-mm-dd
    # the default end date is 7 days after start date
    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key={}'.format(
        start_date, end_date, API_KEY
    )
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroids_all = json_data['near_earth_objects']

    asteroids_size_data = {}
    # sort asteroids data by date
    # structure:
    # {
    #   yyyy-mm-dd:{
    #     asteroid_id:{
    #       name,estimated_min,estimate_max,is_potentially_hazardous
    #     }
    #   }
    # }
    # asteroid data includes:
    #   id: aid below, as the key of each dictionary elements
    #   name: name in NASA data
    #   estimated minimum diameter: estimated_min below, in meter
    #   estimated maximum diameter: estimated_max below, in meter
    #   is potentially hazardous asteroid: is_potentially_hazardous below, in boolean,
    #       True for hazardous, False for not hazardous
    for date in asteroids_all.items():
        asteroids_size_data[date[0]] = {}
        for asteroid in date[1]:
            aid = asteroid['id']
            asteroids_size_data[date[0]][aid] = {}
            asteroids_size_data[date[0]][aid]['name'] = asteroid['name']
            asteroids_size_data[date[0]][aid]['estimated_min'] = asteroid['estimated_diameter']['meters']['estimated_diameter_min']
            asteroids_size_data[date[0]][aid]['estimated_max'] = asteroid['estimated_diameter']['meters']['estimated_diameter_max']
            asteroids_size_data[date[0]][aid]['is_potentially_hazardous'] = asteroid['is_potentially_hazardous_asteroid']

    return asteroids_size_data


if __name__ == '__main__':
    data = get_asteroids_data('2019-09-16')
    print(data)
