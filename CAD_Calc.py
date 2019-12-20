from NASASpider import *
import os
import matplotlib.pyplot as plt
import numpy as np

NEO_API_KEY = 'jvZwakvScvkB3hk3XIAKmoYcQULwIkpPreD7JnHj'
DB = os.getcwd() + '/Asteroids_NASA.db'

def averageVelocity(body):
    count = 0
    total = 0
    for x in body:
        total += x[0]
        if len(x) > 1:
            total += x[1]
            count += 1
        count += 1
    return total/count


conn = sqlite3.connect(DB)
cur = conn.cursor()

avg1 = {}
avg2 = {}

Earth_vals = cur.execute("""SELECT CAD_2018_05.velocity, CAD_2018_10.velocity FROM CAD_2018_05
JOIN CAD_2018_10 ON CAD_2018_05.body = CAD_2018_05.body WHERE CAD_2018_05.body = 'Earth' AND  CAD_2018_10.body = 'Earth'""").fetchall()
Moon_vals = cur.execute("""SELECT CAD_2018_05.velocity, CAD_2018_10.velocity FROM CAD_2018_05
JOIN CAD_2018_10 ON CAD_2018_05.body = CAD_2018_05.body WHERE CAD_2018_05.body = 'Moon' AND  CAD_2018_10.body = 'Moon'""").fetchall()
Mars_vals1 = cur.execute("SELECT velocity FROM CAD_2018_05 WHERE body = 'Mars'").fetchall()
Mercury_vals1 = cur.execute("SELECT velocity FROM CAD_2018_05 WHERE body = 'Mercury'").fetchall()
Venus_vals1 = cur.execute("SELECT velocity FROM CAD_2018_05 WHERE body = 'Venus'").fetchall()
Mars_vals2 = cur.execute("SELECT velocity FROM CAD_2018_10 WHERE body = 'Mars'").fetchall()
Mercury_vals2 = cur.execute("SELECT velocity FROM CAD_2018_10 WHERE body = 'Mercury'").fetchall()
Venus_vals2 = cur.execute("SELECT velocity FROM CAD_2018_10 WHERE body = 'Venus'").fetchall()

avg1['Mercury'] = str(averageVelocity(Mercury_vals1))
avg1['Venus'] = str(averageVelocity(Venus_vals1))
avg1['Moon'] = str(averageVelocity(Moon_vals))
avg1['Earth'] = str(averageVelocity(Earth_vals))
avg1['Mars'] = str(averageVelocity(Mars_vals1))
avg2['Mercury'] = str(averageVelocity(Mercury_vals2))
avg2['Venus'] = str(averageVelocity(Venus_vals2))
avg2['Moon'] = str(averageVelocity(Moon_vals))
avg2['Earth'] = str(averageVelocity(Earth_vals))
avg2['Mars'] = str(averageVelocity(Mars_vals2))

with open('CAD_Calc.txt', 'w+') as outfile:
    outfile.write('Average velocities, in km/s, of close-approach objects in May 2018:')
    json.dump(avg1,outfile)
    outfile.write('\n')
    outfile.write('Average velocities, in km/s, of close-approach objects in October 2018:')
    json.dump(avg2,outfile)
outfile.close()

bodies = avg1.keys()
velocities1 = [float(i) for i in avg1.values()]
velocities2 = [float(i) for i in avg2.values()]

velocities1 = [round(x,2) for x in velocities1]
velocities2 = [round(x,2) for x in velocities2]

x = np.arange(len(bodies))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, velocities1, width, label='May 2018', color = (0.1, 0.2, 0.3, 0.3))
rects2 = ax.bar(x + width/2, velocities2, width, label='October 2018', color = (0.2, 0.4, 0.6, 0.6))

ax.set_ylabel('Velocity (km/s)')
ax.set_title('Average Velocity of Close-Approach Objects Near Plantery Bodies')
ax.set_xticks(x)
ax.set_xticklabels(bodies)
ax.set_yticks([0,5,10,15,20,25,30,35,40])
ax.set_yticklabels([0,5,10,15,20,25,30,35,40])
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()