import serial
import csv
serBarCode = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
import datetime
import time

GIT_file = open("csv/GIT.csv", mode = "w")
PIT_file = open("csvPIT.csv", mode = "w")
WST_file = open("csv/WST.csv", mode = "w")
AFR_file = open("csv/AFR.csv", mode = "w")

GIT_writer = csv.writer(GIT_file, delimiter = ",")
PIT_writer = csv.writer(PIT_file, delimiter = ",")
WST_writer = csv.writer(WST_file, delimiter = ",")
AFR_writer = csv.writer(AFR_file, delimiter = ",")
while True:

    #read data from serial port
    data = serBarCode.readline().decode("UTF-8")
    #data = "1.2312321 AFR"

    if data[-3:] == "GIT": #gallons in tank
        GIT_writer.writerow([data[:-3],datetime.datetime.now()])
    elif data[-3:] == "PIT": #pump in time
        PIT_writer.writerow([data[:-3],datetime.datetime.now()])
    elif data[-3:] == "WST": #water sensor time
        WST_writer.writerow([data[:-3],datetime.datetime.now()])
    elif data[-3:] == "AFR": #average flow rate
        AFR_writer.writerow([data[:-3],datetime.datetime.now()])
    time.sleep(1)
GIT_writer.close()
PIT_writer.close()
WST_writer.close()
AFR_writer.close()