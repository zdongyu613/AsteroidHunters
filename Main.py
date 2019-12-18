from NASASpider import *
import os

# Global variables
NEO_API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = os.getcwd() + '\Asteroids_NASA.db'

# get necessary data and store them into database

start_date_1 = datetime.date(2018, 5, 1)
start_date_2 = datetime.date(2018, 10, 1)

# NEO data
for i in range(10):
    date = start_date_1 + datetime.timedelta(days=i)
    store_neo_in_db(get_neo_data(date, KEY), DB, 'NEO_2018_05')

for i in range(10):
    date = start_date_2 + datetime.timedelta(days=i)
    store_neo_in_db(get_neo_data(date, KEY), DB, 'NEO_2018_10')

# Sentry data
for i in range(7):
    store_sentry_in_db(get_sentry_data(6), DB, 'larger_than_1e6')

for i in range(7):
    store_sentry_in_db(get_sentry_data(5), DB, 'larger_than_1e5')

# Close-Approach data
for i in range(8):
    date = start_date_1 + datetime.timedelta(weeks=i)
    store_cad_in_db(get_ca_data(date), DB, 'CAD_2018_05')

for i in range(8):
    date = start_date_2 + datetime.timedelta(weeks=i)
    store_cad_in_db(get_ca_data(date), DB, 'CAD_2018_10')

# calculation and plotting
