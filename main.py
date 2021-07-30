import pandas as pd
import matplotlib.pyplot as plt


def CleanUpBatteryLogs(file, headers):
    #read in the data:
    df = pd.read_csv(file, names=headers, delimiter='\t')

    df = df.iloc[1:, :]
    df = df.astype(float)
    #print(df)
    return df

def Find_100_SOC_Trigger(df):
    if (df['Voltage']/7 > 4.10 AND df[104/25]) OR (df['Voltage']/7 > 4.20) OR (df['Current'] > -1):
        SOC = 100
    elif :
       
    
    return

def CleanUpManualLogs(file):
    headers = ['Date Time','Charge/Discharge Cycle','Current Benchtop','Voltage Benchtop','Voltage Multimeter',
               'Current Multimeter','Notes','VB1 AR Bat','VB2 AR Bat','IB1 AR Bat','IB2 AR Bat','IB1 AR bench',
               'IB2 AR Bench','VB1 AR Bench','VB2 AR bench']
    df = pd.read_csv(file, names=headers, delimiter='\t')
    df['Date Time'] = df['Date Time'].apply(time_convert)
    # df['Time'] = df['Time'].dt.hour * 3600 + df['Time'].dt.minute * 60
    offset = df['Date Time'][0]
    df['Date Time'] -= offset
    return df

def time_convert(x):
    times = x.split(':')
    return (60*int(times[0])+int(times[1]))*60


headers = ['Batt ID #',	'Voltage','Batt Temp [C]','H/S Temp [C]','Current [A]','SOC','Time','Byte E Bit Map','Byte F Bit Map','Byte G Bit Map','Byte H Bit Map']
#df1 = pd.read_csv('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\StartFullDrainBat9_Cleaned.tsv',names=headers, delimiter='\t')

#df2 = pd.read_csv('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\StartFullDrainBat8_Cleaned.tsv',names=headers, delimiter='\t')
df1= CleanUpBatteryLogs('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\StartFullDrainBat9_Cleaned.tsv', headers)
df2= CleanUpBatteryLogs('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\StartFullDrainBat8_Cleaned.tsv', headers)

#df2= CleanUpBatteryLogs('C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\HIWIND Battery Data\\2021-07-26-10-25-Serial-2.log', headers)
df3 = CleanUpManualLogs("C:/Users\mjeffers\Documents\Output Folder-20210729T173049Z-001\Output Folder\Manually Collected Data.csv")

print(df3['Date Time'])
print(df3['Current Benchtop'])
# plot

# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# # make a plot
line1 = ax.plot(df1.Time, df1.Voltage,color="tab:red", label="Voltage As Reported by Bat1")
line2 = ax.plot(df2.Time, df2.Voltage,color="tab:orange", label="Voltage As Reported by Bat2")
line3 = ax.plot(df3['Date Time'], df3['Current Benchtop'], color="tab:green", label="Voltage As Reported by Benchtop")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.grid(color='gray', linestyle='-', linewidth=1)


#Plot The SOC
ax2 = ax.twinx()
line4 = ax2.plot(df1.Time, df1.SOC,color="tab:blue", label="State of Charge as Reported by Bat1")
line5 = ax2.plot(df2.Time, df2.SOC,color="tab:purple", label="State of Charge as Reported by Bat2")
ax2.set_ylabel("SOC (%)")

plt.title("Battery Drain Taken 7/28 - 7/29")

lines = line1+line2+line3+line4+line5
labs = [l.get_label() for l in lines]
ax.legend(lines, labs, loc=0)
plt.show()
# plt.plot(x1,y1, label='Bat1')
# plt.plot(x2,y2, label='Bat2')
# plt.plot(x1, soc1, label='State of Charge')
# plt.plot(x2,soc2, label='State of Charge Batt2')
# # beautify the x-labels
#
# plt.gcf().autofmt_xdate()
# plt.show()
