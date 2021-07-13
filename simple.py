import time
from machine import Pin
#-------------------------------------------------------------------------------------------------------------------------------------
# pins to controll each hardware device and defines if the pins are taking in or letting out signals

pump = Pin(0,Pin.OUT) #assigns pin 0 to the solenoid/pump


pump.on() #turns on pump


time.sleep(15) #wait for 15 seconds


pump.off() # turn off pump
