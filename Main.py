from NASASpider import *
import os

# Global variables
NEO_API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = os.getcwd() + '\Asteroids_NASA.db'

# get necessary data and store them into database
store_neo_in_db(get_neo_data('2019-09-01', NEO_API_KEY), DB, 'NEO_2019_09_01')
store_neo_in_db(get_neo_data('2019-10-01', NEO_API_KEY), DB, 'NEO_2019_10_01')

store_sentry_in_db(get_sentry_data(6), DB, 'larger_than_1e6')
store_sentry_in_db(get_sentry_data(5), DB, 'larger_than_1e5')

store_cad_in_db(get_ca_data('2018-01-01'), DB, 'CAD_2018_01_01')
store_cad_in_db(get_ca_data('2019-03-01'), DB, 'CAD_2019_03_01')

# calculation and plotting

