from statistics import *
import numpy as np
import matplotlib.pyplot as plt
import math


def sigmoid(a, b, x):
    try:
        return 1./(1+math.exp(-1.*a*(x-b)))
    except:
        return 0
        
a = 0.9
b = 5

res = []
for i in range(-5, 17):
	res.append(sigmoid(a, b, i))


_, ax = plt.subplots()
ax.plot(range(-5, 17), res, linewidth=0.7, alpha=1)
plt.show()
plt.clf()
