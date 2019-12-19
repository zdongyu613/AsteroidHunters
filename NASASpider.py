import requests
import sqlite3
import json
import datetime

KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'

def get_neo_data(day_date, key):
    # day_date: datetime.date object, datetime.date(year,month,day)
    # key: api key
    # First API using, get rough data of asteroids near earth from the given start date to 1 days later
    # data from NASA NeoWs
    end_date = day_date + datetime.timedelta(days=1)

    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key={}'.format(
        day_date, end_date, key
    )
    print('Connecting NeoWs...')
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    try:
        asteroids_all = json_data['near_earth_objects']
    except KeyError:
        print('No data received, please check your day date info and api key.')
        return {}

    asteroids_size_data = {}
    #################################################################
    # category asteroids data by date
    # structure:
    # {
    #    aid:{
    #       estimated_min,estimated_max
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

    print('NeoWs data successfully collected. Data start from {} to {}'.format(day_date, end_date))

    return asteroids_size_data


def get_sentry_data(impact_p):
    # this function get asteroids which have potential future Earth impact events.
    #
    # impact_p limit data to those with a impact-probability (IP)
    # greater than or equal to this value
    # impact_p range: [0, 10]
    #
    # data from Sentry System API
    ip_min = '1e-{}'.format(impact_p)
    url = 'https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={}'.format(ip_min)
    print('Connecting Sentry...')
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    try:
        asteroids_data = json_data['data']
    except KeyError:
        print('No data received, please check your impact probability input,'
              ' which should be the minus log of real probability.')
        return {}

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

    print('Sentry data successfully collected. Asteroid with impact-probability greater than 1e-{}'.format(impact_p))
    print('\n')

    return asteroids_size_data


def get_ca_data(start_date):
    # start_date: datetime.date object
    # Third API using, get rough data of asteroids near earth from the given start date to 1 week later
    # data from JPL's Small-Body DataBase
    end_date = start_date + datetime.timedelta(weeks=1)

    url = 'https://ssd-api.jpl.nasa.gov/cad.api?date-min={}&date-max={}&body=ALL'.format(start_date, end_date)
    print('Connecting SBDB Close-Approach Data...')
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
    try:
        asteroids_data = json_data['data']
    except KeyError:
        print('No data received, please check your start date.')
        return {}

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
    for asteroid in asteroids_data:
        asteroid_velocity_data[asteroid[0].strip()] = {
            'velocity': asteroid[7],
            'body': asteroid[10]
        }

    print('Close-Approach Data from {} to {} successfully collected.'.format(start_date, end_date))
    print('\n')

    return asteroid_velocity_data


def store_neo_in_db(dic, db, sheet_name):
    ###############################
    # receive 3 arguments:
    #   dic: the neo dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################
    print('Connecting database: {}...'.format(db))
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            aid int UNIQUE,
            estimated_min float,
            estimated_max float
        )
        '''.format(sheet_name))
    conn.commit()

    # store one row each time
    print('Storing NEO data...')
    count = 0
    for i in dic.items():
        cur.execute('''
            REPLACE INTO {} (aid, estimated_min, estimated_max)
            VALUES ({},{},{});
            '''.format(sheet_name,
                       i[0],
                       i[1]['estimated_min'],
                       i[1]['estimated_max']))
        conn.commit()
        count += 1
        if count >= 20:
            break

    print('Success, {} items stored in {}.'.format(count, sheet_name))
    print('\n')


def store_sentry_in_db(dic, db, sheet_name):
    ###############################
    # receive 3 arguments:
    #   dic: the sentry dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################
    print('Connecting database: {}...'.format(db))
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            aid varchar(255) UNIQUE,
            diameter float,
            impact_probability varchar(255)
        )
        '''.format(sheet_name))
    conn.commit()

    # store one row each time
    print('Storing Sentry data...')
    count = 0
    for i in dic.items():
        try:
            cur.execute('''
                INSERT INTO {} (aid, diameter, impact_probability)
                VALUES ({},{},{});
                '''.format(sheet_name,
                           "'{}'".format(i[0]),
                           i[1]['diameter'],
                           i[1]['impact_probability']))
            conn.commit()
            count += 1
        except:
            continue
        if count >= 20:
            break
    print('Success. {} new data stored in {}'.format(count,sheet_name))
    print('\n')


def store_cad_in_db(dic, db, sheet_name):
    ###############################
    # receive 3 arguments:
    #   dic: the sentry dictionary you want to store into database
    #       dictionary key should be the unique id of each row
    #   db: database file path
    #   sheet_name: name of table in which data stored
    ###############################
    print('Connecting database: {}...'.format(db))
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS {} (
            designation varchar(255) UNIQUE,
            velocity float,
            body varchar(255)
        )
        '''.format(sheet_name))
    conn.commit()

    # store one row each time
    print('Storing Close-Approach Data...')
    count = 0
    for i in dic.items():
        cur.execute('''
            REPLACE INTO {} (designation, velocity, body)
            VALUES ({},{},{});
            '''.format(sheet_name,
                       "'{}'".format(i[0]),
                       i[1]['velocity'],
                       "'{}'".format(i[1]['body'])))
        conn.commit()
        count += 1
        if count >= 20:
            break
    print('Success, {} items stored in {}.'.format(count, sheet_name))

