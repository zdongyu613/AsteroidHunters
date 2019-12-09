import requests
import sqlite3
import json
import os.path

# Global variables
API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = 'Asteroids.db'


def get_asteroids_data(start_date, end_date=''):
    # date form: yyyy-mm-dd
    # the default end date is 7 days after start date
    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key={}'.format(
        start_date, end_date, API_KEY
    )
    raw_data = requests.get(url).text
    json_data = json.loads(raw_data)
