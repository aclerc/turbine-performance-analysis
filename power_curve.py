import lidar
import turbine
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

lidar_df = lidar.process("2025-09-21", "2025-12-24")
lidar_df = lidar.filter(lidar_df)
turbine_df = turbine.process(20250921, 20251223).collect()
print(f"lidar len {len(lidar_df)}")
print(f"turbine len {len(turbine_df)}")

def t_findVariable(opt):
    return turbine.findVariable(opt)

def l_findVariable(opt):
    return lidar.findVariable(opt)

def cp(printer=True, savefig=False):
    times = [i for i in range(0,100)]
    wind_speeds = (turbine_df["AcWindSp_AcWindSp"].to_list())[:100]
    power = (turbine_df["ActPower_Value"].to_list())[:100]
    pressures = (lidar_df["Air Density (kg/m3)"].to_list())[:100]
    cps = []
    A = np.pi * 961
    for i in range(0, len(times)):
        if (pressures[i] is None) or (wind_speeds[i] is None) or (wind_speeds[i]<2) or (power[i] is None):
            cps.append(None)
        else: 
            cps.append(2000*power[i]/(pressures[i]*A*(wind_speeds[i]**3)))
            if cps[i]>1 or cps[i]<0:
                cps.pop()
                cps.append(None)
    fig, ax = plt.subplots()
    S,P = np.meshgrid(wind_speeds, power)
    Z = (2000*P/(1.22*np.pi*961*S**3))
    for zrow in range(0, len(Z)):
        for z in range (0, len(Z[0])):
            if Z[zrow][z] > 0.59: Z[zrow][z] = 0.593
    plt.pcolormesh(S, P, Z, cmap='viridis', shading='auto')
    plt.colorbar()
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Power (kW)")
    plt.title("Cp as a function of Wind Speed and Power")
    if savefig: plt.savefig("CpWSP.png", bbox_inches='tight')
    if (printer):
        plt.show()
        #turbine.graph_data(xopt= times, findxopt=False, x_label="Time (minutes)", setxlabel=False,
        #    yopt=cps, findyopt=False, y_label="Coefficient of Power", si=5)
        '''wind_speeds, power = np.mgrid[:51, :51]
        Z = 2000*power/(1.22*A*(wind_speeds**3))
        fig, ax = plt.subplots(figsize=(6,3))
        pos = ax.imshow(Z, cmap='Blues', interpolation='none')
        cbar = fig.colorbar(pos, ax)
        cbar.minorticks_on()
        cbar.set_label("Cp")
        ax.set_xlabel("Wind Speed (m/s)")
        ax.set_ylabel("Power (kW)")
        ax.set_title("Cp as a function of Wind Speed and Power")
        plt.show()'''

def graph_power_curve(show=True, savefig=False):
    speds1=[]
    speds2=[]
    speds3=[]
    pows1 = []
    pows2 = []
    pows3 =[]
    for i in range(0,126920):
        if i%60 < 20:
            if turbine_df["AcWindSp_AcWindSp"][i] is None:
                speds1.append(None)
            else: speds1.append(turbine_df["AcWindSp_AcWindSp"][i])
            if turbine_df["ActPower_Value"][i] is None:
                pows1.append(None)
            else: pows1.append(turbine_df["ActPower_Value"][i])
        elif i%60 < 40:
            if turbine_df["AcWindSp_AcWindSp"][i] is None:
                speds2.append(None)
            else: speds2.append(turbine_df["AcWindSp_AcWindSp"][i])
            if turbine_df["ActPower_Value"][i] is None:
                pows2.append(None)
            else: pows2.append(turbine_df["ActPower_Value"][i])
        else:
            if turbine_df["AcWindSp_AcWindSp"][i] is None:
                speds3.append(None)
            else: speds3.append(turbine_df["AcWindSp_AcWindSp"][i])
            if turbine_df["ActPower_Value"][i] is None:
                pows3.append(None)
            else: pows3.append(turbine_df["ActPower_Value"][i])

    for i in range(len(speds1)-1, 0, -1):
        while speds1[i] == None: 
            del speds1[i]
            del pows1[i]
        while pows1[i] == None:
            del pows1[i]
            del speds1[i]
    for i in range(len(speds2)-1, 0, -1):
        while speds2[i] == None: 
            del speds2[i]
            del pows2[i]
        while pows2[i] == None:
            del pows2[i]
            del speds2[i]
    for i in range(len(speds3)-1, 0, -1):
        while speds3[i] == None: 
            del speds3[i]
            del pows3[i]
        while pows3[i] == None:
            del pows3[i]
            del speds3[i]

    plt.style.use("bmh")
    xy1 = np.vstack([speds1, pows1])
    z1 = gaussian_kde(xy1)(xy1)
    fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    sc1 = ax1.scatter(speds1, pows1, c=z1, s=5, cmap='plasma')
    plt.colorbar(sc1, label='Probability Density', ax=ax1)
    ax1.set_xlabel("Wind Speed (m/s)", fontsize=12)
    ax1.set_ylabel("Power (kW)", fontsize=12)
    ax1.set_title("First 20", fontsize=20)
    xy2 = np.vstack([speds2, pows2])
    z2 = gaussian_kde(xy2)(xy2)
    sc2 = ax2.scatter(speds2, pows2, c=z2, s=5, cmap='plasma')
    plt.colorbar(sc2, label='Probability Density', ax=ax2)
    ax2.set_xlabel("Wind Speed (m/s)", fontsize=12)
    ax2.set_ylabel("Power (kW)", fontsize=12)
    ax2.set_title("Mid 20", fontsize=20)
    xy3 = np.vstack([speds3, pows3])
    z3 = gaussian_kde(xy3)(xy3)
    sc3 = ax3.scatter(speds3, pows3, c=z3, s=5, cmap='plasma')
    plt.colorbar(sc3, label='Probability Density', ax=ax3)
    ax3.set_xlabel("Wind Speed (m/s)", fontsize=12)
    ax3.set_ylabel("Power (kW)", fontsize=12)
    ax3.set_title("Last 20", fontsize=20)
    plt.suptitle("Alta Power Curves")
    if savefig: plt.savefig(f"ALTAPowerCurve.png",bbox_inches='tight')
    if show: plt.show()

#turbine.gather_data60()
#turbine.graph_data(18,6)

#coefficient of power depends on pitch, TSR, sheer, veer, and misalignment angle
#plot theta vs. shear

'''time1 = l_findVariable(55)[0]
time2 = l_findVariable(55)[4*1440]
theShears = lidar.get_shear_veer(t1=time1, t2=time2, returnVar='shear', addNones=True)
theThetas = (t_findVariable(9))[15*1440:19*1440]
turbine.graph_data(xopt=theShears, yopt=theThetas, findxopt=False, findyopt=False,
                   x_label='Shear', y_label='Pitch (degrees)')'''

cp()