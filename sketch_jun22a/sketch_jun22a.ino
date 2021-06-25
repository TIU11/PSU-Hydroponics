// pins to controll each hardware device
int pump = 3;
int sol = 4;
int water = 5;
int nut = 6;

// timings and other stuff:
int how_many_nutrients = 5 // in mL
int time_for_nut_pump = how_many_nutrients * 1000; // peristaltic pump dispenses 1 ml per second (1000 is in miliseconds)

int floodTime = 5 * 60 * 1000; // 5 minutes (in miliseconds), time water stays on roots of plantsbefore draining
int floodWait =  3 * 60 * 60 * 1000; // 3 Hours (in miliseconds), time between floods
int interval = 12 * 60 * 60 * 1000; //  12 hours (in miliseconds), time between acvtive and inactive periods
unsigned long previousMillis = 0; //  Tracks the time since last event fired
bool active_period = true;

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
  // keeps filling the planet container
  while (digitalRead(water) == 1){ // keep looping this code untill water hits the water sensor
    // keep the pump on and the solenoid valve open
    digitalWrite(pump, 1);
    digitalWrite(sol, 1);
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
