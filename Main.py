from NASASpider import *
import os

# Global variables

NEO_API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = os.getcwd() + '\Asteroids_NASA.db'

# get necessary data and store them into database
'''store_neo_in_db(get_neo_data('2019-09-01', NEO_API_KEY), DB, 'NEO_2019_09_01')
store_neo_in_db(get_neo_data('2019-10-01', NEO_API_KEY), DB, 'NEO_2019_10_01')

start_date_1 = datetime.date(2018, 5, 1)
start_date_2 = datetime.date(2018, 10, 1)

store_cad_in_db(get_ca_data('2018-01-01'), DB, 'CAD_2018_01_01')
store_cad_in_db(get_ca_data('2019-03-01'), DB, 'CAD_2019_03_01')'''

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
def averageVelocity(body):
    count = 0
    total = 0
    for x in body:
        total += x[0]
        count +=1
    return (total/count)

conn = sqlite3.connect(DB)
cur = conn.cursor()
avgs= {}
Earth_avg = cur.execute("SELECT velocity FROM CAD_2018_01_01 WHERE body = 'Earth'")
Mars_avg = cur.execute("SELECT velocity FROM CAD_2018_01_01 WHERE body = 'Mars'")
Mercury_avg = cur.execute("SELECT velocity FROM CAD_2018_01_01 WHERE body = 'Mercury'")
Moon_avg = cur.execute("SELECT velocity FROM CAD_2018_01_01 WHERE body = 'Moon'")
Venus_avg = cur.execute("SELECT velocity FROM CAD_2018_01_01 WHERE body = 'Venus'")
outFile = open('calc.txt','w+')
outFile.write('Earth Average Velocities: ' + str(averageVelocity(Earth_avg)))
outFile.write('Mars Average Velocities: ' + str(averageVelocity(Mars_avg)))
outFile.write('Mercury Average Velocities: ' + str(averageVelocity(Mercury_avg)))
outFile.write('Moon Average Velocities: ' + str(averageVelocity(Moon_avg)))
outFile.write('Venus Average Velocities: ' + str(averageVelocity(Venus_avg)))
outFile.close()