import serial
serBarCode = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

while True:

    #read data from serial port
    data = serBarCode.readline()

    print(data)