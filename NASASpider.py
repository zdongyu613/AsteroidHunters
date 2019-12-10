import requests
import sqlite3
import json
import os

# Global variables
NEO_API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = os.getcwd() + '\Asteroids_NASA.db'


def get_neo_data(start_date, end_date=''):
    # date form: yyyy-mm-dd
    # the default end date is 7 days after start date
    # First API using, get rough data of asteroids near earth in given date range
    # data from NASA NeoWs
    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key={}'.format(
        start_date, end_date, NEO_API_KEY
    )
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroids_all = json_data['near_earth_objects']

    asteroids_size_data = {}
    #################################################################
    # category asteroids data by date
    # structure:
    # {
    #   yyyy-mm-dd:{
    #     asteroid_name:{
    #       estimated_min,estimate_max,is_potentially_hazardous
    #     },
    #   },
    # }
    # asteroid data includes:
    #   name: name of asteroid in NASA data
    #   estimated_min: estimated minimum diameter in meter
    #   estimated_max: estimated maximum diameter in meter
    #   is_potentially_hazardous: whether the NEO is potentially hazardous asteroid, in boolean,
    #       True for hazardous, False for not hazardous
    ##################################################################
    for date in asteroids_all.items():
        asteroids_size_data[date[0]] = {}
        for asteroid in date[1]:
            name = asteroid['name']
            asteroids_size_data[date[0]][name] = {}
            asteroids_size_data[date[0]][name]['estimated_min'] = asteroid['estimated_diameter']['meters']['estimated_diameter_min']
            asteroids_size_data[date[0]][name]['estimated_max'] = asteroid['estimated_diameter']['meters']['estimated_diameter_max']
            asteroids_size_data[date[0]][name]['is_potentially_hazardous'] = asteroid['is_potentially_hazardous_asteroid']

    return asteroids_size_data


def get_sentry_data():
    # this function get all asteroids which have potential future Earth impact events.
    # data from Sentry System API
    url = 'https://ssd-api.jpl.nasa.gov/sentry.api'
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroids_data = json_data['data']

    asteroids_size_data = {'all_potential_impact': {}}
    #############################################################
    # structure:
    # {
    #   all_potential_impact:{
    #       asteroid_name:{
    #           diameter, designation
    #       }
    #   }
    # }
    # asteroid data includes:
    #   asteroid_name: asteroid full name
    #   diameter: in kilometer
    #   designation: often same as asteroid's name
    #############################################################
    for asteroid in asteroids_data:
        asteroids_size_data['all_potential_impact'[asteroid['fullname']]] = {
            'diameter': asteroid['diameter'],
            'designation': asteroid['des']
        }

    return asteroids_size_data


def store_in_db(dic, db):
    ###############################
    # receive 2 arguments:
    #   dic: the dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    ###############################
    conn = sqlite3.connect(db)
    cur = conn.cursor()


if __name__ == '__main__':
    print(os.getcwd())
