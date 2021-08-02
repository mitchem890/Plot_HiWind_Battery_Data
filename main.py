import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

#Create DataFrames from the 3 main components of the Acquisition
def Create_Bat1_Bat2_Man_DataFrame(Bat1_file, Bat2_file, Man_file):
    Battery1 = CleanUpBatteryLogs(Bat1_file)
    Battery2 = CleanUpBatteryLogs(Bat2_file)
    ManualLog = CleanUpManualLogs(Man_file)
    return Battery1, Battery2, ManualLog



def CreateChargingChart(Charging_Bat1, Charging_Bat2, Manual_Log, PlotCalculatedSOC = False):

    # create figure and axis objects with subplots()
    fig, ax = plt.subplots()
    line1 = ax.plot(Charging_Bat1.Time, Charging_Bat1.Voltage, color="tab:red", label="Voltage As Reported by Bat1")
    line2 = ax.plot(Charging_Bat2.Time, Charging_Bat2.Voltage, color="tab:orange", label="Voltage As Reported by Bat2")
    line3 = ax.plot(Manual_Log['Date Time'], Manual_Log['Current Benchtop'], color="tab:green",
                    label="Voltage As Reported by Benchtop")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.grid(color='gray', linestyle='-', linewidth=1)

    # Plot The SOC
    ax2 = ax.twinx()
    line4 = ax2.plot(Charging_Bat1.Time, Charging_Bat1.SOC, color="tab:blue", label="State of Charge as Reported by Bat1")
    line5 = ax2.plot(Charging_Bat2.Time, Charging_Bat2.SOC, color="tab:purple", label="State of Charge as Reported by Bat2")
    ax2.set_ylabel("SOC (%)")

    if PlotCalculatedSOC:
        Charging = Find_100_SOC_Trigger(Charging_Bat1)
        ax3 = ax.twinx()
        ax3.set_ylim([-0.5,1.5])
        line6 = ax3.plot(Charging.Time, Charging['set_100_SOC'], label="Calculated soc 100")
        line5 = line5+ line6
    plt.title("Battery Drain Taken 7/28 - 7/29")

    lines = line1 + line2 + line3 + line4 + line5
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=0)
    plt.show()


#Create a Cleaned Dataframe From a csv of a battery log
def CleanUpBatteryLogs(file):

    headers = ['Batt ID #', 'Voltage', 'Batt Temp [C]', 'H/S Temp [C]', 'Current', 'SOC', 'Time', 'Byte E Bit Map',
               'Byte F Bit Map', 'Byte G Bit Map', 'Byte H Bit Map']
    df = pd.read_csv(file, names=headers, delimiter='\t')
    df = df.iloc[1:, :]
    df = df.astype(float)
    return df

def Find_100_SOC_Trigger(df):
    #print("Firtst Condition")
    np.set_printoptions(threshold=sys.maxsize)
    #print(np.where((df['Voltage']/7 > 4.10) & (df['Current'] < 4.16), True, False))
  #  print("Second Condition")
    #print(np.where(df['Voltage']/7 > 4.20, True, False))
    print("Third Condition")
    print(np.where(df['Current'] < 1, 1, 0))
    df['set_100_SOC'] = np.where(((df['Voltage']/7 > 4.10) & (df['Current'] < (4.16)) | (df['Voltage']/7 > 4.20) | (df['Current'] > -1)), 1, 0)
    return df

#Create a dataframe from a cleaned up
def CleanUpManualLogs(file):
    headers = ['Date Time','Charge/Discharge Cycle','Voltage Benchtop','Current Benchtop','Voltage Multimeter',
               'Current Multimeter','Notes','VB1 AR Bat','VB2 AR Bat','IB1 AR Bat','IB2 AR Bat','IB1 AR bench',
               'IB2 AR Bench','VB1 AR Bench','VB2 AR bench']
    df = pd.read_csv(file, names=headers, delimiter='\t')
    df['Date Time'] = df['Date Time'].apply(time_convert)
    # df['Time'] = df['Time'].dt.hour * 3600 + df['Time'].dt.minute * 60
    offset = df['Date Time'][0]
    df['Date Time'] -= offset
    return df

#Convert Hours:Mins to sec
def time_convert(x):
    times = x.split(':')
    return (60*int(times[0])+int(times[1]))*60



#df2 = pd.read_csv('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\StartFullDrainBat8_Cleaned.tsv',names=headers, delimiter='\t')
Discharging_Bat1 = 'C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\StartFullDrainBat9_Cleaned.tsv'
Discharging_Bat2 = 'C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\StartFullDrainBat8_Cleaned.tsv'
Charging_Bat1 = "C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Compiled_Charge_Data_7_30.txt"
Charging_Bat2 = "C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Compiled_Charge_Data_7_30_Bat2.txt"
Discharge_Manual_Log = "C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\Manually Collected Data.csv"
Charge_Manual_Log = "C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Charge_Manual_Log.tsv"


bat1_df, bat2_df, man_df = Create_Bat1_Bat2_Man_DataFrame(Charging_Bat1,Charging_Bat2,Charge_Manual_Log)
CreateChargingChart(bat1_df, bat2_df, man_df, True)