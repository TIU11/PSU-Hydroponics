// pins to controll each hardware device
int pump = 3;
int sol = 4;
int water = 5;
int nut = 6;
int sensorPin = 2;
int sensorInterrupt = 0;  // 0 = digital pin 2

// timings and other stuff:
int how_many_nutrients = 5 // in mL
int time_for_nut_pump = how_many_nutrients * 1000; // peristaltic pump dispenses 1 ml per second (1000 is in miliseconds)

int floodTime = 5 * 60 * 1000; // 5 minutes (in miliseconds), time water stays on roots of plantsbefore draining
int floodWait =  3 * 60 * 60 * 1000; // 3 Hours (in miliseconds), time between floods
int interval = 12 * 60 * 60 * 1000; //  12 hours (in miliseconds), time between acvtive and inactive periods
unsigned long previousMillis = 0; //  Tracks the time since last event fired
bool active_period = true;

// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow. These are variables for later
float calibrationFactor = 4.5;
volatile byte pulseCount = 0;
float flowRate = 0.0;
unsigned int flowMilliLitres = 0;
unsigned int totalMilliLitres = 0;
unsigned long old_time_for_hall_sensor = 0;

void setup() {
  // defines if the pins are taking in or letting out signals
  pinMode(pump, OUTPUT);
  pinMode(sol, OUTPUT);
  pinMode(water, INPUT);
  pinMode(nut, OUTPUT);

  // turns off pumps and solinoid just to be safe
  digitalWrite(pump, 0);
  digitalWrite(sol, 0);

  // turns on and off nutrient pump for predefined amount of time
  digitalWrite(nut, 0);
  delay(time_for_nut_pump);
  digitalWrite(nut, 1);

  Serial.begin(9600); //for communicating data

  // defines hall_efect sensor pins and turns it on
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);


  // The Hall-effect sensor is connected to pin 2 which uses interrupt 0.
  // Configured to trigger on a FALLING state change (transition from HIGH
  // state to LOW state)
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);

}

void loop() {
  unsigned long currentMillis = millis();  // Get snapshot of time

  if (active_period == true){ // whether or not we are giving the plant water for 12 hours (day-night cycle)
    // How much time has passed, accounting for rollover with subtraction! (https://www.baldengineer.com/arduino-how-do-you-reset-millis.html)
    // Stops the water cycling for 12 hours if its been running for 12 hours
    if ((unsigned long)(currentMillis - previousMillis) >= interval) {
      active_period = false;
      previousMillis = currentMillis; //  resets the time we are counting to
    }
    //if it hasnt been 12 hours yet....
    else{
      addWater(); // start water cycle that goes every 3 hours (or whatever you change it to)
    }

  else{
    // How much time has passed, accounting for rollover with subtraction! (https://www.baldengineer.com/arduino-how-do-you-reset-millis.html)
    // Starts the water cycle again after 12 hours if its been 12 hours
    if ((unsigned long)(currentMillis - previousMillis) >= interval) {
      active_period = true;
      previousMillis = currentMillis; // Resets the time we are counting to

      // Turns on and off nutrient pump for predefined amount of time
      digitalWrite(nut, 0);
      delay(time_for_nut_pump);
      digitalWrite(nut, 1);
    }

  }

}

void addWater() {
  //


  // keeps filling the planet container
  while (digitalRead(water) == 1){ // keep looping this code untill water hits the water sensor
    // keep the pump on and the solenoid valve open
    digitalWrite(pump, 1);
    digitalWrite(sol, 1);

    //code by codebender_cc on instructables --------------------------------------------------------------------------------
    if((millis() - oldTime) > 1000){    // Only process counters once per second

    // Disable the interrupt while calculating flow rate and sending the value to
    // the host
    detachInterrupt(sensorInterrupt);

    // Because this loop may not complete in exactly 1 second intervals we calculate
    // the number of milliseconds that have passed since the last execution and use
    // that to scale the output. We also apply the calibrationFactor to scale the output
    // based on the number of pulses per second per units of measure (litres/minute in
    // this case) coming from the sensor.
    flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;

    // Note the time this processing pass was executed. Note that because we've
    // disabled interrupts the millis() function won't actually be incrementing right
    // at this point, but it will still return the value it was set to just before
    // interrupts went away.
    oldTime = millis();

    // Divide the flow rate in litres/minute by 60 to determine how many litres have
    // passed through the sensor in this 1 second interval, then multiply by 1000 to
    // convert to millilitres.
    flowMilliLitres = (flowRate / 60) * 1000;

    // Add the millilitres passed in this second to the cumulative total
    totalMilliLitres += flowMilliLitres;

    unsigned int frac;

    // Print the flow rate for this second in litres / minute
    Serial.print("Flow rate: ");
    Serial.print(int(flowRate));  // Print the integer part of the variable
    Serial.print("L/min");
    Serial.print("\t"); 		  // Print tab space

    // Print the cumulative total of litres flowed since starting
    Serial.print("Output Liquid Quantity: ");
    Serial.print(totalMilliLitres);
    Serial.println("mL");
    Serial.print("\t"); 		  // Print tab space
	  Serial.print(totalMilliLitres/1000);
	  Serial.print("L");


    // Reset the pulse counter so we can start incrementing again
    pulseCount = 0;

    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
    //---------------------------------------------------------------------------------------------------------------------
  }
  // turn the pump off and close the solenoid valve
  digitalWrite(pump, 0);
  digitalWrite(sol, 0);

  delay(floodTime); // keeps roots wet for the time we defined earlier

  digitalWrite(sol, 1); // opens the solenoid valve to drain the water

  delay(35 *1000); //  wait 35 seconds (in miliseconds) for the water to completly drain

  digitalWrite(sol, 0); // close solenoid valve to stop draining

  delay(floodWait); // waits for a certain amount of time till this code might run again
}

void pulseCounter() // for other code to work
{
  // Increment the pulse counter
  pulseCount++;
}
