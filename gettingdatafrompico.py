import serial
import csv
serBarCode = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
import datetime
import time

GIT_file = open("csv/GIT.csv", mode = "a")
PIT_file = open("csv/PIT.csv", mode = "a")
WST_file = open("csv/WST.csv", mode = "a")
AFR_file = open("csv/AFR.csv", mode = "a")

GIT_writer = csv.writer(GIT_file, delimiter = ",")
PIT_writer = csv.writer(PIT_file, delimiter = ",")
WST_writer = csv.writer(WST_file, delimiter = ",")
AFR_writer = csv.writer(AFR_file, delimiter = ",")

while True:

    #read data from serial port
    data = serBarCode.readline().decode("UTF-8")
    #data = "1.5312321 AFR"

    if data[-3:] == "GIT": #gallons in tank
        GIT_writer.writerow([datetime.datetime.now() ,data[:-3]])
    elif data[-3:] == "PIT": #pump in time
        PIT_writer.writerow([datetime.datetime.now(), data[:-3]])
    elif data[-3:] == "WST": #water sensor time
        WST_writer.writerow([datetime.datetime.now(), data[:-3]])
    elif data[-3:] == "AFR": #average flow rate
        AFR_writer.writerow([datetime.datetime.now(), data[:-3]])
    else:
        pass
    time.sleep(1)
    
GIT_file.close()
PIT_file.close()
WST_file.close()
AFR_file.close()