
int pump = 3;
int sol = 4;
int water = 5;
int nut = 6;
void setup() {
  pinMode(pump,OUTPUT);
  pinMode(sol,OUTPUT);
  pinMode(water,INPUT);
  pinMode(nut,OUTPUT);
  digitalWrite(pump,0);
  digitalWrite(sol,0);
  
  digitalWrite(nut,0);
  delay(2000);
  digitalWrite(nut,1);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(sol,1);
  digitalWrite(pump,1);
  addWater();

}

void addWater(){
  while(digitalRead(water) == 0){
    digitalWrite(pump,0);
      digitalWrite(sol,0);

      delay(5000);
      digitalWrite(sol,1);

      delay(40000);
      
      digitalWrite(sol,0);
      
      delay(7000);
  }
}



