import requests
import sqlite3
import json



def get_neo_data(start_date, key):
    # date form: yyyy-mm-dd
    # key: api key
    # First API using, get rough data of asteroids near earth from the given start date to 7 days later
    # data from NASA NeoWs
    end_date = ''
    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key={}'.format(
        start_date, end_date, key
    )
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroids_all = json_data['near_earth_objects']

    asteroids_size_data = {}
    #################################################################
    # category asteroids data by date
    # structure:
    # {
    #    aid:{
    #       estimated_min,estimates_max
    #    },
    # }
    # asteroid data includes:
    #   aid: asteroid id
    #   estimated_min: estimated minimum diameter in meter
    #   estimated_max: estimated maximum diameter in meter
    ##################################################################
    for date in asteroids_all.items():
        for asteroid in date[1]:
            aid = asteroid['id']
            asteroids_size_data[aid] = {}
            asteroids_size_data[aid]['estimated_min'] = asteroid['estimated_diameter']['meters']['estimated_diameter_min']
            asteroids_size_data[aid]['estimated_max'] = asteroid['estimated_diameter']['meters']['estimated_diameter_max']

    return asteroids_size_data


def get_sentry_data(impact_p):
    # this function get asteroids which have potential future Earth impact events.
    #
    # impact_p limit data to those with a impact-probability (IP)
    # greater than or equal to this value
    # impact_p range: [-10,0]
    #
    # data from Sentry System API
    ip_min = '1e-{}'.format(impact_p)
    url = 'https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={}'.format(ip_min)
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroids_data = json_data['data']

    asteroids_size_data = {}
    #############################################################
    # structure:
    # {
    #    aid:{
    #       diameter, impact_probability
    #    },
    # }
    # asteroid data includes:
    #   aid: asteroid id
    #   impact_probability: probability of having impact event with earth
    #   diameter: in kilometer
    #############################################################
    for asteroid in asteroids_data:
        asteroids_size_data[asteroid['id']] = {
            'diameter': asteroid['diameter'],
            'impact_probability': asteroid['ip']
        }

    return asteroids_size_data


def get_ca_data(start_date):
    # start_date form: yyyy-mm-dd
    # Third API using, get rough data of asteroids near earth from the given start date to 60 days later
    # data from NASA NeoWs
    url = 'https://ssd-api.jpl.nasa.gov/cad.api?date-min={}&body=ALL'.format(start_date)
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    asteroid_data = json_data['data']

    asteroid_velocity_data = {}
    ############################################################
    # structure:
    # {
    #    designation:{
    #       velocity, body
    #    }
    # }
    # asteroid data includes:
    #   designation: use to recognize which asteroid it is, often same as name
    #   velocity: velocity relative to the approach body at close approach, in km/s
    #   body: name of the close-approach body, e.g., Earth
    ############################################################
    for asteroid in asteroid_data:
        asteroid_velocity_data[asteroid[0].strip()] = {
            'velocity': asteroid[7],
            'body': asteroid[10]
        }

    return asteroid_velocity_data


def store_neo_in_db(dic, db, sheet_name):
    ###############################
    # receive 3 arguments:
    #   dic: the neo dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS {}'.format(sheet_name))

    cur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            aid int,
            estimated_min float,
            estimated_max float
        )
        '''.format(sheet_name))
    conn.commit()

    # store one row each time
    for i in dic.items():
        cur.execute('''
            INSERT INTO {} (aid, estimated_min, estimated_max)
            VALUES ({},{},{});
            '''.format(sheet_name,
                       i[0],
                       i[1]['estimated_min'],
                       i[1]['estimated_max']))
        conn.commit()


def store_sentry_in_db(dic, db, sheet_name):
    ###############################
    # receive 3 arguments:
    #   dic: the sentry dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS {}'.format(sheet_name))

    cur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            aid varchar(255),
            diameter float,
            impact_probability varchar(255)
        )
        '''.format(sheet_name))
    conn.commit()

    # store one row each time
    for i in dic.items():
        cur.execute('''
            INSERT INTO {} (aid, diameter, impact_probability)
            VALUES ({},{},{});
            '''.format(sheet_name,
                       "'{}'".format(i[0]),
                       i[1]['diameter'],
                       i[1]['impact_probability']))
        conn.commit()


def store_cad_in_db(dic, db, sheet_name):
    ###############################
    # receive 3 arguments:
    #   dic: the sentry dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS {}'.format(sheet_name))

    cur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            designation varchar(255),
            velocity float,
            body varchar(255)
        )
        '''.format(sheet_name))
    conn.commit()

    # store one row each time
    for i in dic.items():
        cur.execute('''
            INSERT INTO {} (designation, velocity, body)
            VALUES ({},{},{});
            '''.format(sheet_name,
                       "'{}'".format(i[0]),
                       i[1]['velocity'],
                       "'{}'".format(i[1]['body'])))
        conn.commit()
