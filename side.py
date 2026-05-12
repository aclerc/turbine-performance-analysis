import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np
import random

s=[i for i in range(1, 26)]
fake_powers=[i for i in range(1, 26)]
p=[]
for pow in fake_powers:
    power = (pow**3)*(random.uniform(0.09, 0.59))/2*1.22*np.pi*961/1000
    if power > 1400: p.append(1400)
    else: p.append(power)

S,P = np.meshgrid(s,p)
Z = (2000*P/(1.22*np.pi*961*S**3))
for zrow in range(0, len(Z)):
    for z in range (0, len(Z[0])):
        if Z[zrow][z] > 0.59: Z[zrow][z] = 0.593

plt.contourf(S, P, Z)
plt.colorbar()
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Power (kW)")
plt.title("Cp as a function of Wind Speed and Power")
plt.show()