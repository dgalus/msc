from app.scan import *
from app.database import *
import random
from random import randint
import json
import numpy as np
import matplotlib.pyplot as plt
import itertools

start_hour = 7
end_hour = 16

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

c = db.session.query(Computer).filter(Computer.ip == "10.200.240.151").first()
aut = json.loads(c.active_use_times)

#for i in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
    #if i == "sat" or i == "sun":
        #pass
    #else:
        #start_min = random.randrange(0, 60, 1)
        #end_min = random.randrange(0, 60, 1)
        #for t in range(start_hour*60+start_min, end_hour*60+end_min):
            #aut[i][t] += randint(0, 1)

#c.active_use_times = json.dumps(aut)
#db.session.commit()

arr = []
labels = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
labels_arr = []
for l in labels:
    arr.extend(aut[l])
    labels_arr.append(l + "\n00:00")
    for i in range(0, 720):
        labels_arr.append("")
    labels_arr.append("12:00")
    for i in range(0, 720):
        labels_arr.append("")

x = range(0, 1440*7)
y = arr
plt.title('Aktywność komputera w czasie')
plt.xlabel('Czas')
plt.ylabel('Aktywność')
plt.xticks(x, labels_arr)
plt.plot(x, y, linewidth=0.2)
plt.show()
plt.clf()