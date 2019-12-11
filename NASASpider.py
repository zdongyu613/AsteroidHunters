import requests
import sqlite3
import json
import os

# Global variables
NEO_API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = os.getcwd() + '\Asteroids_NASA.db'


def get_neo_data(start_date):
    # date form: yyyy-mm-dd
    # First API using, get rough data of asteroids near earth from the given start date to 7 days later
    # data from NASA NeoWs
    end_date = ''
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
    #    asteroid_name:{
    #       estimated_min,estimate_max,is_potentially_hazardous
    #    },
    # }
    # asteroid data includes:
    #   name: name of asteroid in NASA data
    #   estimated_min: estimated minimum diameter in meter
    #   estimated_max: estimated maximum diameter in meter
    #   is_potentially_hazardous: whether the NEO is potentially hazardous asteroid, in boolean,
    #       True for hazardous, False for not hazardous
    ##################################################################
    for date in asteroids_all.items():
        for asteroid in date[1]:
            name = asteroid['name']
            asteroids_size_data[name] = {}
            asteroids_size_data[name]['estimated_min'] = asteroid['estimated_diameter']['meters']['estimated_diameter_min']
            asteroids_size_data[name]['estimated_max'] = asteroid['estimated_diameter']['meters']['estimated_diameter_max']
            asteroids_size_data[name]['is_potentially_hazardous'] = asteroid['is_potentially_hazardous_asteroid']

    return asteroids_size_data


def get_sentry_data(impact_p):
    # this function get asteroids which have potential future Earth impact events.
    #
    # impact_p limit data to those with a impact-probability (IP)
    # greater than or equal to this value
    # impact_p range: [-10,0]
    #
    # data from Sentry System API
    ipmin = '1e-{}'.format(impact_p)
    url = 'https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={}'.format(ipmin)
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroids_data = json_data['data']

    asteroids_size_data = {}
    #############################################################
    # structure:
    # {
    #    name:{
    #       diameter, designation
    #    },
    # }
    # asteroid data includes:
    #   name: asteroid full name
    #   designation: use to recognize which asteroid it is, often same as name
    #   diameter: in kilometer
    #############################################################
    for asteroid in asteroids_data:
        asteroids_size_data[asteroid['fullname']] = {
            'diameter': asteroid['diameter'],
            'designation': asteroid['des']
        }

    return asteroids_size_data


def get_ca_data(start_date):
    # start_date form: yyyy-mm-dd
    # Third API using, get rough data of asteroids near earth from the given start date to 60 days later
    # data from NASA NeoWs
    url = 'https://ssd-api.jpl.nasa.gov/cad.api?date-min={}&body=ALL&fullname=true'.format(start_date)
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroid_data = json_data['data']

    asteroid_velocity_data = {}
    ############################################################
    # structure:
    # {
    #    name:{
    #       velocity, body, designation
    #    }
    # }
    # asteroid data includes:
    #   name: asteroid full name
    #   designation: use to recognize which asteroid it is, often same as name
    #   velocity: velocity relative to the approach body at close approach, in km/s
    #   body: name of the close-approach body, e.g., Earth
    ############################################################
    for asteroid in asteroid_data:
        asteroid_data[asteroid[11].strip()] = {
            'velocity': asteroid[7],
            'body': asteroid[10],
            'designation': asteroid[0]
        }

    return asteroid_velocity_data


def store_neo_in_db(dic, db, sheet_name):
    ###############################
    # receive 2 arguments:
    #   dic: the neo dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS {}(
        estimated_min ,
        estimate_max,
        is_potentially_hazardous
    )
    '''.format(sheet_name))




if __name__ == '__main__':
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS test(
        name TEXT,
        diameter INT
    )
    ''')
