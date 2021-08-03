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



def CreateChargingChart(Charging_Bat1, Charging_Bat2, Manual_Log, PlotCalculatedSOC = False, Title="Battery Data Plot"):

    # create figure and axis objects with subplots()
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    line1 = ax.plot(Charging_Bat1.Time, Charging_Bat1.Voltage, color="tab:red", label="Voltage As Reported by Bat1")
    line2 = ax2.plot(Charging_Bat1.Time, Charging_Bat1.SOC, color="tab:blue",
                         label="State of Charge as Reported by Bat1")
    line = line1 + line2
    if Charging_Bat2 is not None:
        line3 = ax.plot(Charging_Bat2.Time, Charging_Bat2.Voltage, color="tab:orange", label="Voltage As Reported by Bat2")
        line4 = ax2.plot(Charging_Bat2.Time, Charging_Bat2.SOC, color="tab:purple", label="State of Charge as Reported by Bat2")
        line = line + line3+ line4
    if Manual_Log is not None:
        line5 = ax.plot(Manual_Log['Date Time'], Manual_Log['Current Benchtop'], color="tab:green",
                        label="Voltage As Reported by Benchtop")
        line= line + line5

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    ax.grid(color='gray', linestyle='-', linewidth=1)

    # Plot The SOC

    ax2.set_ylabel("SOC (%)")

    if PlotCalculatedSOC:
        Charging = Find_100_SOC_Trigger(Charging_Bat1)
        ax3 = ax.twinx()
        ax3.set_ylim([-0.5,1.5])
        line6 = ax3.plot(Charging.Time, Charging['set_100_SOC'], label="Calculated soc 100")
        line5 = line5+ line6
    plt.title(Title)

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
    headers = ['Date Time','Current','Voltage Benchtop','Current Benchtop','Voltage Multimeter',
               'Current Multimeter','Notes','VB1 AR Bat','VB2 AR Bat','IB1 AR Bat','IB2 AR Bat','IB1 AR bench',
               'IB2 AR Bench','VB1 AR Bench','VB2 AR bench']
    df = pd.read_csv(file, names=headers, delimiter='\t')
    df['Date Time'] = df['Date Time'].apply(time_convert)
    # df['Time'] = df['Time'].dt.hour * 3600 + df['Time'].dt.minute * 60
    offset = df['Date Time'][0]
    df['Date Time'] -= offset
    df['Date Time'] += 1440
    return df

#Convert Hours:Mins to sec
def time_convert(x):
    times = x.split(':')
    return (60*int(times[0])+int(times[1]))*60

def getMeasurmentVarianceCharging(Battery, Manual_log, Current = False):

    print("Voltage Reported by Bat - Voltage Measured")
    results_df = pd.DataFrame(columns=('Time', 'Voltage Reported by Bat', 'Voltage Measured', "Voltage Reported by Bat - Voltage Measured",
                                       "Current Reported by Batt", "Current Measured",  "Current Reported by Bat - Current Measured"))
    for index, row in Manual_log.iterrows():
        Sampled_Time = row['Date Time']
        Sampled_Voltage = row['Current Benchtop']
        Sampled_Current = row['Voltage Benchtop']

        index_closest_to_sampled_time = Battery['Time'].sub(Sampled_Time).abs().idxmin()
        Reported_Voltage = Battery.at[index_closest_to_sampled_time, 'Voltage']
        Reported_Current = Battery.at[index_closest_to_sampled_time, 'Current']
        results_df.loc[index] = [Sampled_Time, Reported_Voltage, Sampled_Voltage,
                                 Reported_Voltage - Sampled_Voltage,
                                 Reported_Current, Sampled_Current, Reported_Current - Sampled_Current ]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    results_df.to_csv(r"C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Charging_Report.csv", index=False)
    print(results_df)

def getMeasurmentVarianceDischarging(Battery1, Battery2, Manual_log, Current = False):

    print("Voltage Reported by Bat - Voltage Measured")
    results_df = pd.DataFrame(columns=('Time', 'Voltage Reported by Bat1', 'Voltage Reported by Bat2','Voltage Measured',
                                       "Average Voltage Reported by Bat - Voltage Measured",
                                       "Current Reported by Batt1", "Current Reported by Batt2", "Current Measured",
                                       "Current Reported by Bat1 + Current Reported by Bat2  - Current Measured"))
    for index, row in Manual_log.iterrows():
        Sampled_Time = row['Date Time']
        Sampled_Voltage = row['Voltage Benchtop']
        Sampled_Current = row['Current']

        index1_closest_to_sampled_time = Battery1['Time'].sub(Sampled_Time).abs().idxmin()
        Reported_Voltage1 = Battery1.at[index1_closest_to_sampled_time, 'Voltage']
        Reported_Current1 = Battery1.at[index1_closest_to_sampled_time, 'Current']

        index2_closest_to_sampled_time = Battery2['Time'].sub(Sampled_Time).abs().idxmin()
        Reported_Voltage2 = Battery2.at[index2_closest_to_sampled_time, 'Voltage']
        Reported_Current2 = Battery2.at[index2_closest_to_sampled_time, 'Current']

        results_df.loc[index] = [Sampled_Time, Reported_Voltage1, Reported_Voltage1, Sampled_Voltage,
                                 (sum([Reported_Voltage1, Reported_Voltage2])/2) - Sampled_Voltage,
                                 Reported_Current1, Reported_Current2, Sampled_Current, abs(Reported_Current1) + abs(Reported_Current2) - Sampled_Current ]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    results_df.to_csv(r"C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Disharging_Report.csv", index=False)
    print(results_df)




#df2 = pd.read_csv('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\StartFullDrainBat8_Cleaned.tsv',names=headers, delimiter='\t')
Title = "Battery Drain Taken 7/28 - 7/29"
Discharging_Bat1 = 'C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\StartFullDrainBat9_Cleaned.tsv'
Discharging_Bat2 = 'C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\StartFullDrainBat8_Cleaned.tsv'
Discharge_Manual_Log = "C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\Manually Collected Data.csv"


Title = "Charging Battery Data Taken 7/29 - 7-30"
Charging_Bat1 = "C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Compiled_Charge_Data_7_30.txt"
Charging_Bat2 = "C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Compiled_Charge_Data_7_30_Bat2.txt"
Charge_Manual_Log = "C:/Users\mjeffers\Downloads\HIWIND Battery Data\HIWIND Battery Data\Charge_Manual_Log.tsv"


#bat1_df, bat2_df, man_df = Create_Bat1_Bat2_Man_DataFrame(Discharging_Bat1,Discharging_Bat2,Discharge_Manual_Log)
bat1_df, bat2_df, man_df = Create_Bat1_Bat2_Man_DataFrame(Charging_Bat1,Charging_Bat2,Charge_Manual_Log)

CreateChargingChart(bat1_df, bat2_df, man_df,Title=Title)

#Average Voltage difference Between Measured and telemetry
getMeasurmentVarianceCharging(bat2_df, man_df)

#getMeasurmentVarianceDischarging(bat1_df, bat2_df, man_df)