import time
from machine import Pin
#-------------------------------------------------------------------------------------------------------------------------------------
# pins to controll each hardware device and defines if the pins are taking in or letting out signals
pump = Pin(0,Pin.OUT)
sol = Pin(1,Pin.OUT)
water = Pin(1,Pin.IN)
nut = Pin(2,Pin.OUT)
hall_sensor = Pin(4,Pin.IN,Pin.PULL_DOWN)

callBack = hall_sensor.irq(trigger = Pin.IRQ_FALLING)

# timings and other stuff:
how_many_nutrients = 5 # in mL
time_for_nut_pump = how_many_nutrients # peristaltic pump dispenses 1 ml per second

floodTime = 5 * 60 # 5 minutes (in seconds), time water stays on roots of plantsbefore draining
floodWait =  3 * 60 * 60 # 3 Hours (in seconds), time between floods
interval = 12 * 60 * 60 #  12 hours (in seconds), time between acvtive and inactive periods
active_period = "yes" #to give the plant water or not
there_is_power = True #to make the program allways run

# turns off pumps and solinoid just to be safe
pump.off()
sol.off()

# turns on and off nutrient pump for predefined amount of time
nut.on()
time.sleep(time_for_nut_pump)
nut.off()

time_last_checked = time.time()

#--------------------------------------------------------------------------------------------------------------------------------------

def addWater():
    #keeps filling the planet container
    while water.value() == 1: #keep looping this code untill water hits the water sensor
        #keep the pump on and the solenoid valve open
        pump.on()
        sol.on()

    #turn the pump off and close the solenoid valve
    pump.off()
    sol.off()

    time.sleep(floodTime) #keeps roots wet for the time we defined earlier

    sol.on() #opens the solenoid valve to drain the water

    time.sleep(35) #wait 35 seconds for the water to completly drain

    sol.off() #close solenoid valve to stop draining

    time.sleep(floodWait) #waits for a certain amount of time till this code might run again



#--------------------------------------------------------------------------------------------------------------------------------------
# always loop this code over and over again
while there_is_power:
    print(callBack.tally())
    current_time = time.time() # get current timer

    if active_period == "yes": # whether or not we are giving the plant water for 12 hours (day-night cycle)

        #--------------------------------------------------------------------------------------------
        if current_time - time_last_checked >= interval: # Stops the water cycling for 12 hours if its been running for 12 hours
            active_period = "no"
            time_last_checked = current_time # resets the time we are counting to

        else: #if it hasnt been 12 hours yet....
            addWater() # starts water cycle that goes every 3 hours (or whatever you change it to)
        #--------------------------------------------------------------------------------------------

    else:

        #--------------------------------------------------------------------------------------------
        if current_time - time_last_checked >= interval: # Stops the water cycling for 12 hours if its been running for 12 hours
            active_period = "yes"
            time_last_checked = current_time # resets the time we are counting to

            # turns on and off nutrient pump for predefined amount of time
            nut.on()
            time.sleep(time_for_nut_pump)
            nut.off()

        else: #if it hasnt been 12 hours yet....
            pass #do nothing!!!!
