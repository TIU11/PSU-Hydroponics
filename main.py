import time
from machine import Pin
#import logging
import uasyncio as asyncio
from WaterPump.WaterPumps.flowMeters import flowMeter

#-------------------------------------------------------------------------------------------------------------------------------------
# pins to controll each hardware device and defines if the pins are taking in or letting out signals

pump = Pin(0,Pin.OUT)
sol = Pin(1,Pin.OUT)
water = Pin(2,Pin.IN)
nut = Pin(3,Pin.OUT)
hall_sensor_flow = Pin(4,Pin.OUT)
hall_sensor_data = Pin(5,Pin.IN)

# timings and other stuff:
how_many_nutrients = 5 # in mL
time_for_nut_pump = how_many_nutrients # peristaltic pump dispenses 1 ml per second

floodTime = 5 #* 60 # 5 minutes (in seconds), time water stays on roots of plantsbefore draining
floodWait =  3 #* 60 * 60 # 3 Hours (in seconds), time between floods
interval = 12 * 60 * 60 #  12 hours (in seconds), time between acvtive and inactive periods
active_period = "yes" #to give the plant water or not
there_is_power = True #to make the program allways run

mainFlowMeter = flowMeter(flowPin=5, rate=4.8)
global flowCount
flowCount = 0




# turns off pumps and solinoid just to be safe
pump.off()
sol.off()

# turns on and off nutrient pump for predefined amount of time
nut.on()
time.sleep(time_for_nut_pump)
nut.off()

#--------------------------------------------------------------------------------------------------------------------------------------
time_last_checked = time.time()
def callbackflow(p):
    """Add on to Counter """
    global flowCount
    flowCount += 1
    print("""callback count: %s""" % (flowCount))
#--------------------------------------------------------------------------------------------------------------------------------------
def addWater():
    global flow_per_second
    #keeps filling the planet container

    mainFlowMeter.counterPin.irq(trigger=mainFlowMeter.counterPin.IRQ_RISING, handler=callbackflow)
    while water.value() == 1: #keep looping this code untill water hits the water sensor
        #keep the pump on and the solenoid valve open
        pump.on()
        sol.on()
        hall_sensor_flow.on()

        '''if hall_sensor_data.value() == 1:
            flowCount += 1'''
        
        main_loop = asyncio.get_event_loop()

        main_loop.create_task(mainFlowMeter.monitorFlowMeter())

        main_loop.run_forever()

    #turn the pump off and close the solenoid valve
    main_loop.close()

    '''flowCount = flowCount/(ending_time-starting_time)
    flowCount = (flowCount* 60)/4.8'''
    pump.off()
    sol.off()
    hall_sensor_flow.off()
    # print(str(flowCount) + " l/m")

    time.sleep(floodTime) #keeps roots wet for the time we defined earlier

    sol.on() #opens the solenoid valve to drain the water

    time.sleep(13) #wait 35 seconds for the water to completly drain

    sol.off() #close solenoid valve to stop draining

    time.sleep(floodWait) #waits for a certain amount of time till this code might run again



main_loop = asyncio.get_event_loop()

#load flow monitor task
main_loop.create_task(mainFlowMeter.monitorFlowMeter())#--------------------------------------------------------------------------------------------------------------------------------------
# always loop this code over and over again
while there_is_power:

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
