import polars as pl 
import matplotlib.pyplot as plt
import numpy as np

def get_alta_file(date, #in YYYYMMDD format
                  read=False):
    if read: return pl.read_parquet(rf"C:\Users\lashe\packages\UROPFiles\cache\fl_resampled\ALTA2\1301257\{date}.parquet")
    return pl.scan_parquet(rf"C:\Users\lashe\packages\UROPFiles\cache\fl_resampled\ALTA2\1301257\{date}.parquet")
#Note: files were renamed by date

td60 = 0    
td60data = {}
def process(start=20250905, end=20260301):
    global td60
    files = []
    start = int(start)
    end = int(end)
    for i in range(5,27):
        if i<10: i = f"0{i}"
        date = f"202509{i}"
        if (int(date)>=start and int(date) <=end): files.append(get_alta_file(date))
    for i in range(2,32):
        if i<10: i = f"0{i}"
        date = f"202510{i}"
        if (int(date)>=start and int(date) <=end): files.append(get_alta_file(date))
    for i in range(1,31):
        if i<10: i = f"0{i}"
        date = f"202511{i}"
        if (int(date)>=start and int(date) <=end): files.append(get_alta_file(date))
    for i in range(1,32):
        if i<10: i = f"0{i}"
        date = f"202512{i}"
        if (int(date)>=start and int(date) <=end): files.append(get_alta_file(date))
    for i in range(1,32):
        if i<10: i = f"0{i}"
        date = f"202601{i}"
        if (int(date)>=start and int(date) <=end): files.append(get_alta_file(date))
    for i in range(1,29):
        if i<10: i = f"0{i}"
        date = f"202602{i}"
        if (int(date)>=start and int(date) <=end): files.append(get_alta_file(f"202602{i}"))
    if (20260301>=start and 20260301<=end): files.append(get_alta_file(f"20260301"))
    td60 = pl.concat(files)
    return td60

#similar to gather_data in lidar.py
def gather_data60(cols=[], printer=False, range=[0,0]):
    global td60
    global td60data 
    td60data = {
    'Metric' : [],
    'Average Value' : [],
    'Median' : [],
    'Minimum' : [],
    'Maximum' : [],
    'Standard Deviation' : []
    }   
    td60 = td60.collect()
    if cols==[] : cols = td60data["Metric"] = td60.columns
    else: td60data['Metric'] = cols
    if range==[0,0]: range = [0, len(td60[cols[0]])]
    for col in cols:
        row=0
        first_item = td60.item(row=row, column=col)
        while first_item is None and row < len(td60[col]-1):
            row+=1
            first_item = td60.item(row=row, column=col)
        if isinstance(first_item, (int, float)):
            td60data['Average Value'].append(td60[col][range[0]:range[1]].mean())
            td60data["Median"].append(td60[col][range[0]:range[1]].median())
            td60data['Minimum'].append(td60[col][range[0]:range[1]].min())
            td60data['Maximum'].append(td60[col][range[0]:range[1]].max())
            td60data['Standard Deviation'].append(td60[col][range[0]:range[1]].std())
        else:
            td60data["Average Value"].append(None)
            td60data["Median"].append(None)
            td60data["Minimum"].append(None)
            td60data["Maximum"].append(None)
            td60data["Standard Deviation"].append(None)
    td60data = pl.DataFrame(td60data)
    if printer: 
        with pl.Config(tbl_rows=-1):
            print(td60data)

#reservoir of variables

td60 = process()
dataset = {60:td60}
label = ''
def findVariable(opt, interval=60):
    global label
    if opt==1 or opt=='act_power':
        label = "Active Power (kW)"
        return (dataset[interval].select("ActPower_Value").collect())["ActPower_Value"].to_list()
    elif opt==2 or opt=='ws':
        label = "Wind Speed"
        return (dataset[interval].select("AcWindSp_AcWindSp").collect())["AcWindSp_AcWindSp"].to_list()
    elif opt==3 or opt=='temp':
        label = "Temperature"
        return (dataset[interval].select("AmbieTmp_Value").collect())["AmbieTmp_Value"].to_list()
    elif opt==4 or opt=='genrpm':
        label = "Generator RPM"
        return (dataset[interval].select("GenRpm_Value").collect())["GenRpm_Value"].to_list()
    elif opt==5 or opt=='mainsrpm':
        label = "Main Shaft RPM"
        return (dataset[interval].select("MainSRpm_Value").collect())["MainSRpm_Value"].to_list()
    elif opt==6 or opt=='pitchPosA':
        label = "Pitch Position A"
        return (dataset[interval].select("PitcPosA_Value").collect())["PitcPosA_Value"].to_list()
    elif opt==7 or opt=='pitchPosB':
        label = "Pitch Position B"
        return (dataset[interval].select("PitcPosB_Value").collect())["PitcPosB_Value"].to_list()
    elif opt==8 or opt=='pitchPosC':
        label = "Pitch Position C"
        return (dataset[interval].select("PitcPosC_Value").collect())["PitcPosC_Value"].to_list()
    elif opt==9 or opt=='pitchRefA':
        label = "Pitch Reference A"
        return (dataset[interval].select("PitcRefA_Value").collect())["PitcRefA_Value"].to_list()
    elif opt==10 or opt=='pitchRefB':
        label = "Pitch Reference B"
        return (dataset[interval].select("PitcRefB_Value").collect())["PitcRefB_Value"].to_list()
    elif opt==11 or opt=='pitchRefC':
        label = "Pitch Reference C"
        return (dataset[interval].select("PitcRefC_Value").collect())["PitcRefC_Value"].to_list()
    elif opt==12 or opt=='pwr_red': 
        label =  "Power Red"
        return (dataset[interval].select("PowerRed_PowerRed").collect())["PowerRed_PowerRed"].to_list()
    elif opt==13 or opt=='pwr_ref':
        label = "Power Reference"
        return (dataset[interval].select("PowerRef_PowerRef").collect())["PowerRef_PowerRef"].to_list()
    elif opt==14 or opt=='react_pwr':
        label = "Reactive Power"
        return (dataset[interval].select("ReactPwr_Value").collect())["ReactPwr_Value"].to_list()
    elif opt==15 or opt=='yaw_exec':
        label = "Yaw Exec"
        return (dataset[interval].select("YawExec_YawExec").collect())["YawExec_YawExec"].to_list()
    elif opt==16 or opt=='yaw_pos':
        label = "Yaw Position"
        return (dataset[interval].select("YawPos_Value").collect())["YawPos_Value"].to_list()
    elif opt==17 or opt=='time':
        label = "Time"
        return range(0, len((dataset[interval].select("timestamp").collect())["timestamp"].to_list()))
    elif opt==18 or opt=='timestamp':
        label = "Date"
        return (dataset[interval].select("timestamp").collect())["timestamp"].to_list()
    elif opt==19 or opt=='max_power':
        label = "Max Active Power"
        return (dataset[interval].select("max_ActPower_Value").collect())["max_ActPower_Value"].to_list()
    elif opt==20 or opt=='min_power':
        label = "Min Active Power"
        return (dataset[interval].select("min_ActPower_Value").collect())["min_ActPower_Value"].to_list()
    elif opt==21 or opt=='air_density':
        label = "Air Density"
        return (dataset[interval].select("air_density").collect())["air_density"].to_list()
    elif opt==22 or opt=='HHws':
        label = "Calibrated LiDAR HH ws"
        return (dataset[interval].select("calibrated lidar HH ws").collect())["calibrated lidar HH ws"].to_list()
    elif opt==23 or opt=='wtg_TSR':
        label = "WTG STR"
        return (dataset[interval].select("wtg_TSR").collect())["wtg_TSR"].to_list()
    elif opt==24 or opt=='lidar_TSR':
        label = "LiDAR STR"
        return (dataset[interval].select("lidar_TSR").collect())["lidar_TSR"].to_list()
    elif opt==25 or opt=='lidar_Cp':
        label = "LiDAR Cp"
        return (dataset[interval].select("lidar_Cp").collect())["lidar_Cp"].to_list()
    elif opt==26 or opt=='yaw_error':
        label = "Yaw Error"
        return (dataset[interval].select("lidar measured yaw error").collect())["lidar measured yaw error"].to_list()

#graphs data, see lidar.py for further explanation
def graph_data(xopt, yopt, findxopt=True, findyopt=True, 
               y_vals2=[], y_vals3=[], y_vals4=[], y_vals5=[], y_vals6=[],
               savefig=False, show=True, setxlabel=True, x_label='', y_label='',
               hue='purple', si=3, ax=0):
    if ax==0: fig, ax=plt.subplots(figsize=(6,3))
    plt.style.use('bmh')
    if findxopt: x_vals = findVariable(xopt)
    else: x_vals=xopt
    if x_label == '': xlabel = label
    else: xlabel = x_label
    if setxlabel==True:
        ax.set_xlabel(xlabel, fontsize=12)
    elif not x_label=='':
        ax.set_xlabel(x_label, fontsize=12)
        xlabel = x_label
    if findyopt: y_vals = findVariable(yopt)
    else: y_vals=yopt
    if y_label=='': ylabel = label
    else: ylabel=y_label
    ax.set_ylabel(ylabel,fontsize=12) 
    ax.set_title(f"{ylabel} vs. {xlabel}",fontsize=24)
    ax.scatter(x_vals, y_vals, color=hue, cmap='Purples', s=si)
    if not y_vals2==[]: ax.scatter(x_vals, y_vals2, color='blue', s=si)
    if not y_vals3==[]: ax.scatter(x_vals, y_vals3, color='green', s=si)
    if not y_vals4==[]: ax.scatter(x_vals, y_vals4, color='olive', s=si)
    if not y_vals5==[]: ax.scatter(x_vals, y_vals5, color='orange', s=si)
    if not y_vals6==[]: ax.scatter(x_vals, y_vals6, color='red', s=si)
    xlabel = xlabel.replace(" ","")
    ylabel = ylabel.replace(" ","")
    if savefig: plt.savefig(f"{ylabel}Vs{xlabel}.png",bbox_inches='tight')
    if show: plt.show()

#creates subplots as described in function body
def graph_multiple(savefig=False, show=True):
    fig, axs = plt.subplots(2, figsize=(10, 6), sharex=True)
    graph_data(xopt=17, yopt=1, ax=axs[0], show=False, setxlabel=False, hue='blue')
    graph_data(xopt=18, yopt=1, ax=axs[1], show=False)
    if savefig: plt.savefig('WindSpeed&ActPowerVsTime.png', bbox_inches='tight')
    if show: plt.show()

#converts a timestamp into index (index 0 is 2025-09-05 00:00:00)
def convert_timestamp(time1, interval=60, time2=''):
    START_YEAR = 2025
    START_MONTH = 9
    START_DAY = 5
    START_HOUR = 0
    START_MINUTE = 0
    year = int(time1[:4])
    month = int(time1[5:7])
    day = int(time1[8:10])
    hour = int(time1[11:13])
    minute = int(time1[14:16])
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
    index = time/interval*60
    if time2=='': return index
    return list(range(int(index), int(convert_timestamp(time1=time2, interval=interval))))

#crude plot of daytime vs. nighttime power production to determine any significant diurnal effects
def plot_by_time():
    nights = findVariable(18)
    speeds = findVariable(2)
    night_vals = []
    day_vals = []
    for i in range(146260):
        string = str(nights[i])
        if convert_timestamp(string)%1440 < 270 or convert_timestamp(string)%1440 >= 1230:
            night_vals.append(speeds[i])
            day_vals.append(None)
        else:
            day_vals.append(speeds[i])
            night_vals.append(None)
    fig, axs = plt.subplots(2, figsize=(10, 6))
    graph_data(xopt=range(5000), yopt=findVariable(2)[:5000], ax=axs[0], show=False, findxopt=False, findyopt=False, setxlabel=False, hue='blue')
    graph_data(xopt=range(5000), yopt=day_vals[:5000], y_vals2=night_vals[:5000], findxopt=False, findyopt=False, ax=axs[1], show=False, x_label='time')
    plt.show()

#more relevant for wake steering analysis
def plot_yaw_change(savefig=False, show=True):
    yaw = findVariable("yaw_pos")
    fig, ax = plt.subplots(figsize=(9,3))
    plt.style.use('bmh')
    points = []
    colors = []
    yaw1 = round(yaw[0], 2)
    yaw2 = round(yaw[1], 2)
    points.append(yaw1)
    points.append(yaw2)
    r=0; g = 0; b = 1
    colors.append((r,g,b))
    r=1
    colors.append((r,g,b))
    for i in range(2, len(yaw)):
        if not yaw[i]==None:
            yaw1 = yaw2
            yaw2 = round(yaw[i], 2)
            points.append(yaw2)
        else: points.append(None)
        if yaw2 == yaw1: r = 1
        elif abs(yaw2-yaw1) <= .1: r = 0.5
        else: r = 0
        colors.append((r,g,b))
    ax.scatter(findVariable(18), points, c=colors, marker='*', s=2)
    ax.set_xlabel('Time (sec)', fontsize=12)
    ax.set_ylabel('Yaw Position (deg)', fontsize=12)
    ax.set_title('Yaw Position vs. Time')
    if savefig: plt.savefig('YawPosVsTime.png', bbox_inches='tight')
    if show: plt.show()

#plots the change in pitch from minute to minute
def plot_pitch_change(savefig=False, show=True):
    pitch = findVariable("pitchRefA")
    fig, ax = plt.subplots(figsize=(9,3))
    plt.style.use('bmh')
    points = []
    colors = []
    pitch1 = round(pitch[0], 2)
    pitch2 = round(pitch[1], 2)
    points.append(pitch1)
    points.append(pitch2)
    r=0; g = 0; b = 1
    colors.append((r,g,b,.05))
    r=1
    colors.append((r,g,b,.05))
    for i in range(2, len(pitch)):
        if not pitch[i]==None:
            pitch1 = pitch2
            pitch2 = round(pitch[i], 2)
            points.append(pitch2)
        else: points.append(None)
        if pitch2 == pitch1: r = 1
        elif abs(pitch2-pitch1) <= .1: r = 0.5
        else: r = 0
        colors.append((r,g,b,.05))
    ax.scatter(findVariable(18), points, c=colors, marker='+')
    ax.set_xlabel('Time (sec)', fontsize=12)
    ax.set_ylabel('Pitch Position (deg)', fontsize=12)
    ax.set_title('Pitch Position vs. Time')
    if savefig: plt.savefig('PitchPosVsTime.png', bbox_inches='tight')
    if show: plt.show()

if __name__ == "main":
    process("20250921", "20250923")
    x_vals = findVariable(18)
    all_powers = findVariable(1)
    begin = []
    mid = []
    end = []
    for i in range(0, len(x_vals)):
        if (i%60) <20:
            begin.append(all_powers[i])
            mid.append(None)
            end.append(None)
        else: 
            begin.append(None)
            if (i%60) <40:
                mid.append(all_powers[i])
                end.append(None)
            else:
                mid.append(None)
                end.append(all_powers[i])
    graph_data(xopt=18, yopt=begin, findyopt=False, y_vals4=mid, y_vals6=end, y_label="Power")

td60 = process()
gather_data60(printer=True)