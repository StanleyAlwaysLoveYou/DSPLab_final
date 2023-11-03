
#include <Adafruit_MotorShield.h>
#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial btSerial(11, 12); // RX, TX

Servo L_servo;
Servo R_servo;

int L_pos = 0;    
int R_pos = 0;

bool L_increasing = true;
bool R_increasing = true;

int command;
int movement;

const int trigPin1 = 3;
const int echoPin1 = 4;
const int trigPin2 = 5;
const int echoPin2 = 6;

float duration, distance, tempdistance;

void setup (void)
{
  pinMode(LED_BUILTIN, OUTPUT);

  // Setup and flush the serials to begin
  btSerial.begin(38400);
  Serial.begin(9600);
  btSerial.flush();
  Serial.flush();

  // attach to pins 9 (servo outputs)
  L_servo.attach(9);
  L_servo.write(90);

  // Setup the ultrasomic sensor
  pinMode (trigPin1, OUTPUT);
  pinMode (echoPin1, INPUT);
  pinMode (trigPin2, OUTPUT);
  pinMode (echoPin2, INPUT);

  command = 's';
  movement = 's';

}


void loop (void){
  if (btSerial.available()) {
    command = btSerial.read();
    //Serial.println(char(command));

    // --------------check obstacles--------------------
    if (char(command) == 'r') {
      Serial.println("command: right");
      L_servo.write(0);
      delay(1000);
      
      distance = sonor_detect(trigPin1, echoPin1);
      if (distance < 10) movement = 's';
      else movement = 'r';
    }
    if (char(command) == 'l') {
      Serial.println("command: left");
      L_servo.write(180);
      delay(1000);
      
      distance = sonor_detect(trigPin1, echoPin1);
      if (distance < 10) movement = 's';
      else movement = 'l';
    }
    if (char(command) == 'f') {
      Serial.println("command: forward");
      
      distance = sonor_detect(trigPin1, echoPin1);
      if (distance < 10) movement = 's';
      else movement = 'f';
    }
    if (char(command) == 'b') {
      Serial.println("command: backward");

      distance = sonor_detect(trigPin2, echoPin2);
      if (distance < 10) movement = 's';
      else movement = 'b';
    }
    if (char(command) == 's') {
      Serial.println("command: stop");
      movement = 's';
    }
    //Serial.print("L position: ");
    //Serial.println(L_pos);
  }

  L_servo.write(90);
  delay(10);

  // --------------move--------------------

  Serial.print("movement: ");
  Serial.println(char(movement));

  if (char(movement) == 'r') {

    movement = 's';
  }
  if (char(movement) == 'l') {

    movement = 's';
  }
  if (char(movement) == 'f') {
    
    distance = sonor_detect(trigPin1, echoPin1);
    if (distance < 10) movement = 's';
    else movement = 'f';
  }
  if (char(movement) == 'b') {
    
    distance = sonor_detect(trigPin2, echoPin2);
    if (distance < 10) movement = 's';
    else movement = 'b';
  }
  if (char(movement) == 's') {
    movement = 's';
  }
  
  delay(1000);

}  // end of loop

int sonor_detect(int trigPin, int echoPin) {
  //send the wave
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //read echopin
  duration = pulseIn(echoPin, HIGH);
  tempdistance = (duration*.0343)/2;

  Serial.print("Distance: ");
  Serial.println(tempdistance);
  return tempdistance;  
}
