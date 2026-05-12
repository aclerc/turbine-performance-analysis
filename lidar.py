import matplotlib.pyplot as plt
from windrose import WindroseAxes
import numpy as np
import polars as pl
import pandas as pd
import numbers
from pathlib import Path
from lidar_analysis.lidar_analysis_funcs import get_zx_lidar_data
from foreach import foreach #parallel computing function developed by a Howland Lab alumni

#leftover framework from sample dataset when I was testing various intervals
ld60 = 0
ld120 = 0
ld300 = 0
ld60data = {}
ld120data = {}
ld300data = {}

#gathers data for designated time interval
def process(start = "2025-06-05", end = "2026-02-04"):
    global data
    zx_device_id = 2429  # 2429 is Altahullion 2 ground mounted LiDAR
    start_dt = pd.Timestamp(start)
    end_dt_excl = pd.Timestamp(end)
    return get_zx_lidar_data(
        zx_device_id=zx_device_id,
        start_dt=start_dt,
        end_dt_excl=end_dt_excl,
        cache_dir=None,
    )
data = pl.from_pandas(process(start="2025-09-20", end="2025-09-24")) 
#We typically work in Polars, but can discuss if Pandas is preferred

def filter(filtered_data_df=data, remerge=True):
    global data
    filtered_data = []
    all_times = filtered_data_df['Time and Date']
    used_times = []
    for row in range(0, len(data)):
        if not str(all_times[row])[:16] in used_times:
            used_times.append(str(all_times[row])[:16])
            filtered_data_df['Time and Date'][row] = f"{filtered_data_df['Time and Date'][row][:16]}:00"
            filtered_data.append(data[row])
    filtered_data_df = pl.concat(filtered_data)
    if remerge: data=filtered_data_df
    return filtered_data_df

#runs fundamental stats of data, useful for discovering outliers
metadata = {}
def gather_data(cols=[], #can gather stats for specific variables only
                printer=False #printer controls whether result is displayed to screen
                ):
    global data
    global metadata
    metadata = {
    'Metric' : [],
    'Average Value' : [],
    'Median' : [],
    'Minimum' : [],
    'Maximum' : [],
    'Standard Deviation' : [],
    '5% Value' : [],
    '95% Value': []
    }
    #data = data.collect()
    if cols==[] : cols = metadata['Metric'] = data.columns
    else: metadata['Metric'] = cols
    for col in cols:
        row=0
        first_item = data.item(row=row, column=col)
        while first_item is None and row < len(data[col]-1):
            row+=1
            first_item = data.item(row=row, column=col)
        if isinstance(first_item, (int, float)):
            metadata['Average Value'].append(data[col].mean())
            metadata['Median'].append(data[col].median())
            metadata['Minimum'].append(data[col].min())
            metadata['Maximum'].append(data[col].max())
            metadata['Standard Deviation'].append(data[col].std())
            metadata['5% Value'].append(data[col].quantile(.05))
            metadata['95% Value'].append(data[col].quantile(.95))
        else:
            metadata["Average Value"].append(None)
            metadata['Median'].append(None)
            metadata["Minimum"].append(None)
            metadata["Maximum"].append(None)
            metadata["Standard Deviation"].append(None)
            metadata["5% Value"].append(None)
            metadata["95% Value"].append(None)
    metadata = pl.DataFrame(metadata)
    if printer: 
        with pl.Config(tbl_rows=-1):
            print(metadata)

#findVariable is a (albeit lengthy) shortcut function to navigate variables in the dataset
#see graph_data function for examples of usage
dataset = {60:ld60, 120:ld120, 300:ld300, 0:data}
label = ''
def findVariable(opt, interval=0):
    global label
    if opt==1 or opt=='wd18':
        label = "Wind Direction at 18m"
        return (dataset[interval]["Wind Direction (deg) at 18m"]).to_list()
    elif opt==2 or opt=='ws18':
        label = "Horiz. Wind Speed at 18m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 18m"]).to_list()
    elif opt==3 or opt=='wd28':
        label = "Wind Direction at 28m"
        return (dataset[interval]["Wind Direction (deg) at 28m"]).to_list()
    elif opt==4 or opt=='ws28':
        label = "Horiz. Wind Speed at 28m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 28m"]).to_list()
    elif opt==5 or opt=='wd38':
        label = "Wind Direction at 38m"
        return (dataset[interval]["Wind Direction (deg) at 38m"]).to_list()
    elif opt==6 or opt=='ws38':
        label = "Horiz. Wind Speed at 38m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 38m"]).to_list()
    elif opt==7 or opt=='wd48':
        label = "Wind Direction at 48m"
        return (dataset[interval]["Wind Direction (deg) at 48m"]).to_list()
    elif opt==8 or opt=='ws48':
        label = "Horiz. Wind Speed at 48m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 48m"]).to_list()
    elif opt==9 or opt=='wd58':
        label = "Wind Direction at 58m"
        return (dataset[interval]["Wind Direction (deg) at 58m"]).to_list()
    elif opt==10 or opt=='ws58':
        label = "Horiz. Wind Speed at 58m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 58m"]).to_list()
    elif opt==11 or opt=='wd68':
        label = "Wind Direction at 68m"
        return (dataset[interval]["Wind Direction (deg) at 68m"]).to_list()
    elif opt==12 or opt=='ws68':
        label = "Horiz. Wind Speed at 68m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 68m"]).to_list()
    elif opt==13 or opt=='wd78':
        label = "Wind Direction at 78m"
        return (dataset[interval]["Wind Direction (deg) at 78m"]).to_list()
    elif opt==14 or opt=='ws78':
        label = "Horiz. Wind Speed at 78m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 78m"]).to_list()
    elif opt==15 or opt=='wd88':
        label = "Wind Direction at 88m"
        return (dataset[interval]["Wind Direction (deg) at 88m"]).to_list()
    elif opt==16 or opt=='ws88':
        label = "Horiz. Wind Speed at 88m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 88m"]).to_list()
    elif opt==17 or opt=='wd98':
        label = "Wind Direction at 98m"
        return (dataset[interval]["Wind Direction (deg) at 98m"]).to_list()
    elif opt==18 or opt=='ws98':
        label = "Horiz. Wind Speed at 98m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 98m"]).to_list()
    elif opt==19 or opt=='wd141':
        label = "Wind Direction at 141m"
        return (dataset[interval]["Wind Direction (deg) at 141m"]).to_list()
    elif opt==20 or opt=='ws141':
        label = "Horiz. Wind Speed at 141m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 141m"]).to_list()
    elif opt==21 or opt=='wd203':
        label = "Wind Direction at 203m"
        return (dataset[interval]["Wind Direction (deg) at 203m"]).to_list()
    elif opt==22 or opt=='ws203':
        label = "Horiz. Wind Speed at 203m"
        return (dataset[interval]["Horizontal Wind Speed (m/s) at 203m"]).to_list()
    elif opt==23 or opt=='vws18':
        label = "Vert. Wind Speed at 18m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 18m"]).to_list()
    elif opt==24 or opt=='vws28':
        label = "Vert. Wind Speed at 28m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 28m"]).to_list()
    elif opt==25 or opt=='vws38':
        label = "Vert. Wind Speed at 38m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 38m"]).to_list()
    elif opt==26 or opt=='vws48':
        label = "Vert. Wind Speed at 48m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 48m"]).to_list()
    elif opt==27 or opt=='vws58':
        label = "Vert. Wind Speed at 58m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 58m"]).to_list()
    elif opt==28 or opt=='vws68':
        label = "Vert. Wind Speed at 68m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 68m"]).to_list()
    elif opt==29 or opt=='vws78':
        label = "Vert. Wind Speed at 78m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 78m"]).to_list()
    elif opt==30 or opt=='vws88':
        label = "Vert. Wind Speed at 88m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 88m"]).to_list()
    elif opt==31 or opt=='vws98':
        label = "Vert. Wind Speed at 98m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 98m"]).to_list()
    elif opt==32 or opt=='vws141':
        label = "Vert. Wind Speed at 141m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 141m"]).to_list()
    elif opt==33 or opt=='vws203':
        label = "Vert. Wind Speed at 203m"
        return (dataset[interval]["Vertical Wind Speed (m/s) at 203m"]).to_list()
    elif opt==34 or opt=='mwd':
        label = "Met Wind Direction"
        return (dataset[interval]["Met Wind Direction (deg)"]).to_list()
    elif opt==35 or opt=='GPS':
        label = "GPS"
        return (dataset[interval]["GPS"]).to_list()
    elif opt==36 or opt=='status':
        label = "Status Flags"
        return (dataset[interval]["Status Flags"]).to_list()
    elif opt==37 or opt=='info':
        label = "Info. Flags"
        return (dataset[interval]["Info. Flags"]).to_list()
    elif opt==38 or opt=='checksum':
        label = "Checksum"
        return "save your sanity and don't use this column"
    elif opt==39 or opt=='air_density':
        label = "Air Density"
        return (dataset[interval]["Air Density (kg/m3)"]).to_list()
    elif opt==40 or opt=='fog':
        label = "Fog"
        return (dataset[interval]["Fog"]).to_list()
    elif opt==41 or opt=='raining':
        label = "Raining"
        return (dataset[interval]["Raining"]).to_list()
    elif opt==42 or opt=='met_humidity':
        label = "Met Humidity"
        return (dataset[interval]["Met Humidity (%)"]).to_list()
    elif opt==43 or opt=='pressure':
        label = "Met Pressure"
        return (dataset[interval]["Met Pressure (mbar)"]).to_list()
    elif opt==44 or opt=='mws':
        label = "Met Wind Speed"
        return (dataset[interval]["Met Wind Speed (m/s)"]).to_list()
    elif opt==45 or opt=='air_temp':
        label = "Met Air Temp."
        return (dataset[interval]["Met Air Temp. (C)"]).to_list()
    elif opt==46 or opt=='tilt':
        label = "Met Tilt"
        return (dataset[interval]["Met Tilt (deg)"]).to_list()
    elif opt==47 or opt=='compass':
        label = "Met Compass Bearing"
        return (dataset[interval]["Met Compass Bearing (deg)"]).to_list()
    elif opt==48 or opt=='pod_humidity (%)':
        label = "Pod Humidity"
        return (dataset[interval]["Pod Humidity (%)"]).to_list()
    elif opt==49 or opt=='low_temp':
        label = "Lower Temp."
        return (dataset[interval]["Lower Temp. (C)"]).to_list()
    elif opt==50 or opt=='up_temp':
        label = "Upper Temp."
        return (dataset[interval]["Upper Temp. (C)"]).to_list()
    elif opt==51 or opt=='generator':
        label = "Generator"
        return (dataset[interval]["Generator (V)"]).to_list()
    elif opt==52 or opt=='battery':
        label = "Battery"
        return (dataset[interval]["Battery (V)"]).to_list()
    elif opt==53 or opt=='time_date':
        label = "Time and Date"
        return (dataset[interval]["Time and Date"]).to_list()
    elif opt==54 or opt=='timestamp':
        label = 'timestamp'
        times = data["Time and Date"]
        for i in range(0, len(times)):
            stre = data["Time and Date"][i]
            stre = (
                int(stre[:4]) + int(stre[5:7])/100 + int(stre[8:10])/10**4 + 
                int(stre[11:13])/10**6
            )
            times[i] = stre
        return times
    else:
        label = "Timestamp"
        return (dataset[interval]["Timestamp (s)"]).to_list()

#plots windrose from lists of wind speed and direction over time
def myPlotWindRose(savefig=False, show=True, 
                   height=18, title="default", legend=True,
                   ws=[-1], wd=[361], nsector=32,
                   ax = WindroseAxes.from_ax(), interval=0):
    if ws==[-1]:
        ws = findVariable(f'ws{height}', interval)
    if wd==[361]:
        wd = findVariable(f'wd{height}', interval)
    i = len(ws)-1
    while i>=0:
        if not isinstance(ws[i], numbers.Real) or not isinstance(wd[i], numbers.Real):
            del ws[i]
            del wd[i]
        i=i-1
    ax.bar(wd, ws, nsector=nsector, bins=np.arange(0,20,2), normed=True, opening=1, edgecolor='white')
    if legend:
        ax.set_legend(
            title = r"$m \cdot s^{-1}$", bbox_to_anchor=(1.15, -0.1), loc="lower right"
        )
    if title=="default":
        ax.set_title(f"Wind Rose Plot for {height}m")
    elif not (title==""): 
        ax.set_title(title)
    if savefig: plt.savefig(savefig, bbox_inches='tight')
    if show: plt.show()

#plots the windrose at each height
def plot_all_heights(savefig=False, show=True):
    fig, ((ax1,ax2,ax3,ax4), (ax5,ax6,ax7,ax8), (ax9,ax10,ax11,ax12)) = plt.subplots(3, 4, figsize=(20, 10), subplot_kw={'projection': 'windrose'})
    myPlotWindRose(show=False, legend=False, height=18, ax=ax1)
    myPlotWindRose(show=False, legend=False, height=28, ax=ax2)
    myPlotWindRose(show=False, legend=False, height=38, ax=ax3)
    myPlotWindRose(show=False, legend=False, height=48, ax=ax4)
    myPlotWindRose(show=False, legend=False, height=58, ax=ax5)
    myPlotWindRose(show=False, legend=False, height=68, ax=ax6)
    myPlotWindRose(show=False, legend=False, height=78, ax=ax7)
    myPlotWindRose(show=False, legend=False, height=88, ax=ax8)
    myPlotWindRose(show=False, legend=False, height=98, ax=ax9)
    myPlotWindRose(show=False, legend=False, height=141, ax=ax10)
    myPlotWindRose(show=False, legend=False, height=203, ax=ax11)
    myPlotWindRose(show=False, legend=False, ws=findVariable('mws'), wd=findVariable('mwd'), title="Met", ax=ax12)
    plt.tight_layout(pad=0)
    plt.subplots_adjust(wspace=0, hspace=0)
    if savefig: plt.savefig(savefig, bbox_inches='tight')
    if show: plt.show()

#plots the windroses specified in the function
def plot_multiple(savefig=False, show=True, h1=18, h2=18):
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5), subplot_kw={'projection': 'windrose'})
    myPlotWindRose(show=False, height=h1, interval=0, ax=ax1, title=f"Wind at {h1}m")
    myPlotWindRose(show=False, height=h2, interval=0, ax=ax2, title=f"Wind at {h2}m")
    if savefig: plt.savefig(savefig, bbox_inches='tight')
    if show: plt.show()

#converts a timestamp into index (index 0 is 2025-09-05 00:00:00), needs updating for new data
def convert_timestamp(time, interval, time2=''):
    START_YEAR = 2025
    START_MONTH = 9
    START_DAY = 5
    START_HOUR = 0
    START_MINUTE = 0
    year = int(time[:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = int(time[11:13])
    minute = int(time[14:16])
    time = (minute-START_MINUTE)
    time += 60*(hour-START_HOUR)
    time += 1440*(day-START_DAY)
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month > START_MONTH:
        temp = START_MONTH
        while temp < month:
            time += month_lengths[temp-1]*1440
            temp += 1
    elif month < START_MONTH:
        temp = month
        while temp < START_MONTH:
            time -= month_lengths[temp-1]*1440
            temp += 1
    time += 525600*(year-START_YEAR)
    for yr in range(START_YEAR+1, year):
        if yr % 4 == 0 and not yr % 1000 == 0: time += 1440
    if START_YEAR % 4 == 0 and not START_YEAR % 1000 == 0 and START_MONTH <= 2: time += 1440
    if year % 4 == 0 and not year % 1000 == 0 and month > 2: time+=1440
    index = time/interval*60
    if time2=='': return index
    #If only one time is given, the function will return the index of that time 
    return list(range(int(index), int(convert_timestamp(time1=time2, interval=interval))))
    #Otherwise, it will return a list of every index between the start and finish times

def convert_timestamp2(time, time2=''): #updated version\
    START_YEAR = 2025
    START_MONTH = 6
    START_DAY = 5
    START_HOUR = 12
    START_MINUTE = 24
    START_SECOND = 23
    year = int(time[:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = int(time[11:13])
    minute = int(time[14:16])
    second = int(time[17:19])
    time = (second-START_SECOND)/60
    time += (minute-START_MINUTE)
    time += 60*(hour-START_HOUR)
    time += 1440*(day-START_DAY)
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month > START_MONTH:
        temp = START_MONTH
        while temp < month:
            time += month_lengths[temp-1]*1440
            temp += 1
    elif month < START_MONTH:
        temp = month
        while temp < START_MONTH:
            time -= month_lengths[temp-1]*1440
            temp += 1
    time += 525600*(year-START_YEAR)
    for yr in range(START_YEAR+1, year):
        if yr % 4 == 0 and not yr % 1000 == 0: time += 1440
    if START_YEAR % 4 == 0 and not START_YEAR % 1000 == 0 and START_MONTH <= 2: time += 1440
    if year % 4 == 0 and not year % 1000 == 0 and month > 2: time+=1440
    index = 820067063+round(time*60)
    if time2=='': return index
    return list(range(int(index), int(convert_timestamp(time1=time2))))

#Graphs data in pretty much any way you can imagine
def graph_data(xopt, yopt, #x-values and y-values, generally input as the opt for findVariable
               findxopt=True, findyopt=True, #set to false if an actual list is given for xopt or yopt, respectively
               y_vals2=[], y_vals3=[], y_vals4=[], y_vals5=[], y_vals6=[], #to plot multiple lists on y-axis of one graph
               savefig=False, show=True, #saves figure as file, displays figure on screen, respectively
               hue='purple', ax=0, setxlabel=True, x_label='', y_label=''):
    if ax==0: fig, ax=plt.subplots(figsize=(6,3))
    plt.style.use('bmh')
    if findxopt: x_vals = findVariable(xopt)
    else: x_vals=xopt
    xlabel = label
    if setxlabel==True:
        ax.set_xlabel(label, fontsize=12)
    elif not x_label=='':
        ax.set_xlabel(x_label, fontsize=12)
    if findyopt: y_vals = findVariable(yopt)
    else: y_vals=yopt
    ylabel = label
    ax.set_ylabel(label,fontsize=12) 
    if not y_label=='':
        ylabel = y_label
        ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(f"{ylabel} vs. {xlabel}",fontsize=24)
    ax.scatter(x_vals, y_vals, color=hue, cmap='Purples', s=2)
    if not y_vals2==[]: ax.scatter(x_vals, y_vals2, color='blue', s=2)
    if not y_vals3==[]: ax.scatter(x_vals, y_vals3, color='green', s=2)
    if not y_vals4==[]: ax.scatter(x_vals, y_vals4, color='yellow', s=2)
    if not y_vals5==[]: ax.scatter(x_vals, y_vals5, color='orange', s=2)
    if not y_vals6==[]: ax.scatter(x_vals, y_vals6, color='red', s=2)
    xlabel = xlabel.replace(" ","")
    ylabel = ylabel.replace(" ","")
    if savefig: 
        name = fr"{ylabel}Vs{xlabel}.png"
        plt.savefig(name,bbox_inches='tight')
    if show: plt.show()

#creates subplots as specified in the function body
def graph_multiple(savefig=False, show=True):
    fig, axs = plt.subplots(2, figsize=(10, 6), sharex=True)
    global ld60
    ld60 = pl.scan_parquet("UROPFiles/2429/Wind_2429@Y2025_M09_D05.parquet")
    sample = pl.scan_parquet(r"UROP_Sample_Data\resampled_60s_lidar_data.parquet")
    print(len(findVariable(54)))
    graph_data(54,14, ax=axs[0], show=False)
    ld60=sample
    graph_data(xopt=findVariable(54)[:148320], yopt=14, findxopt=False, ax=axs[1], show=False)
    if savefig: plt.savefig('WindSpeed&ActPowerVsTime.png', bbox_inches='tight')
    if show: plt.show()

#helper method to handle non-averaged data
def time_index(timestamp):
    times = findVariable(55)
    low = 0
    high = len(times)-1
    index = -1
    while low <= high:
        mid = int((low+high)/2)
        if times[mid] == timestamp:
            index=mid
            break
        elif times[mid] < timestamp:
            low = mid+1
        else:
            high = mid-1
    return index

#calculates wind speed shear at a designated time
def shear(time, timestampy='', find_close_time=True):
    if not timestampy == '': 
        timestamp=timestampy
        index = time_index(timestampy)
    else: 
        timestamp = convert_timestamp2(time)
        index = time_index(time)
    print(index)
    if index == -1: 
        if find_close_time: shear(time=0, timestampy=timestamp+1)
        else: return None
    wind_speeds = []
    heights = [18,28,38,48,58,68,78,88,98,141,203]
    for i in range(1,10):
        speed = findVariable(f"ws{i}8")[index]
        if speed is None: 
            heights.remove(i*10+8)
        else: wind_speeds.append(speed)
    speed = findVariable("ws141")[index]
    if speed is None: 
        heights.remove(141)
    else: wind_speeds.append(speed)
    speed = findVariable("ws203")[index]
    if speed is None: heights.remove(203)
    else: wind_speeds.append(speed)
    print(heights)
    print(wind_speeds)
    shears = []
    if len(heights)>1:
        z_ref = heights[0]
        U_ref = wind_speeds[0]
        for i in range(1, len(heights)):
            shears.append(np.log(wind_speeds[i]/U_ref)/np.log(heights[i]/z_ref))
        return np.mean(shears)
    return None

#calculates wind direction shear (veer) at a designated time
def veer(time, timestampy='', find_close_time=True):
    if not timestampy == '': 
        timestamp=timestampy
        index = time_index(timestampy)
    else: 
        timestamp = convert_timestamp2(time)
        index = time_index(time)
    print(index)
    if index == -1: 
        if find_close_time: veer(time=0, timestampy=timestamp+1)
        else: return None
    wind_degs = []
    heights = [18,28,38,48,58,68,78,88,98,141,203]
    for i in range(1,10):
        deg = findVariable(f"wd{i}8")[index]
        if deg is None: 
            heights.remove(i*10+8)
        else: wind_degs.append(deg)
    deg = findVariable("wd141")[index]
    if deg is None: 
        heights.remove(141)
    else: wind_degs.append(deg)
    deg = findVariable("wd203")[index]
    if deg is None: heights.remove(203)
    else: wind_degs.append(deg)
    print(heights)
    print(wind_degs)
    if len(heights)>1:
        m, b = np.polyfit(heights, wind_degs, 1)
        return m
    return None

#not priority, just trying to visualize some of the more unusual wind fields
def visualize_wind_field():
    ax = plt.figure().add_subplot(projection='3d')
    # Make the grid
    x, y, z = np.meshgrid([0],[0],[18,28,38,48,58,68,78,88,98,141,203])
    # Make the direction data for the arrows
    u = [0.0005]
    v = [0.0005*z/10]
    w = [0]
    ax.quiver(x, y, z, u, v, w, length=1)
    plt.show()

#gets shear and veer in a designated time interval
def get_shear_veer(t1, t2, returnVar = None, show=True, addNones=False):
    print("starting function now")
    x=[]
    y=[]
    y2=[]
    for t in range(t1, t2):
        if time_index(t) >= 0:
            shear_val = shear(time=0, timestampy=t, find_close_time=False)
            if not shear_val is None or addNones:
                x.append(t)
                y.append(shear_val)
            veer_val = veer(time=0, timestampy=t, find_close_time=False)
            if not veer_val is None:
                y2.append(veer_val)
    if returnVar == 'shear': return y
    print("list of veers")
    print(y2)
    if returnVar == 'veer': return y2
    if show:
        graph_data(xopt=x, yopt=y, y_vals3=y2, findxopt=False, findyopt=False, 
            x_label="Time (s)", y_label="Shear and Veer", savefig=True)

#faster version of get_shear_veer using foreach parallel computing
instantx=[]
instanty=[]
instanty2=[]
def instant_get_shear_veer(t):
    global instantx
    global instanty
    global instanty2
    if time_index(t) >= 0:
        shear_val = shear(time=0, timestampy=t, find_close_time=False)
        if not shear_val is None:
            instantx.append(t)
            instanty.append(shear_val)
        veer_val = veer(time=0, timestampy=t, find_close_time=False)
        if not veer_val is None:
            instanty2.append(veer_val)
'''if __name__ == 'main':
    foreach(instant_get_shear_veer, [*range(841360774, 841363199)])
graph_data(xopt=instantx, yopt=instanty, y_vals3=instanty2, findxopt=False, findyopt=False, 
            x_label="Time (s)", y_label="Shear and Veer")'''

data = pl.from_pandas(process(start="2025-09-20", end="2025-09-24")) 
#timestamp of 2025-09-20 00:00:00 is 829353600
#timestamp of 2025-09-23 23:59:59 is 829699199
print(data['Horizontal Wind Speed (m/s) at 48m'].median())