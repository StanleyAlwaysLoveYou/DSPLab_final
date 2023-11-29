
#include <Adafruit_MotorShield.h>
#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial btSerial(11, 12); // RX, TX

Servo L_servo;
Servo R_servo;

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *LBmotor = AFMS.getMotor(1);
Adafruit_DCMotor *LFmotor = AFMS.getMotor(2);
Adafruit_DCMotor *RFmotor = AFMS.getMotor(3);
Adafruit_DCMotor *RBmotor = AFMS.getMotor(4);

int L_pos = 0;    

int command;
int movement;

const int trigPin1 = 3;
const int echoPin1 = 4;
const int trigPin2 = 5;
const int echoPin2 = 6;

 /*********** parameters **********/
const int motorspeed = 80;
const int spinspeed = 200;

const int spin_duration = 400;

const int threshold = 15;
const int spin_threshold = 25;

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

  // Setup the motors
  if (!AFMS.begin()) {
    Serial.println("Could not find the motr shield");
    while(1);
  }
  LFmotor -> setSpeed(motorspeed);
  LFmotor -> run(RELEASE);
  RFmotor -> setSpeed(motorspeed);
  RFmotor -> run(RELEASE);
  RBmotor -> setSpeed(motorspeed);
  RBmotor -> run(RELEASE);
  LBmotor -> setSpeed(motorspeed);
  LBmotor -> run(RELEASE);

  Serial.println("Complete setup!");

}


void loop (void){
  if (btSerial.available()) {
    command = btSerial.read();
    //Serial.println(char(command));

    LFmotor -> run(RELEASE);
    RFmotor -> run(RELEASE);
    LBmotor -> run(RELEASE);
    RBmotor -> run(RELEASE);

    // --------------check obstacles--------------------
    if (char(command) == 'r') {
      Serial.println("command: right");

      distance = sonor_detect(trigPin1, echoPin1);
      if (distance < threshold-12) movement = 's';
      else {
        L_servo.write(0);
        delay(1000);
      
        distance = sonor_detect(trigPin1, echoPin1);
        if (distance < spin_threshold) movement = 's';
        else movement = 'r';
      }
      
    }
    if (char(command) == 'l') {
      Serial.println("command: left");

      distance = sonor_detect(trigPin1, echoPin1);
      if (distance < threshold-12) movement = 's';
      else {
        L_servo.write(180);
        delay(1000);
      
        distance = sonor_detect(trigPin1, echoPin1);
        if (distance < spin_threshold) movement = 's';
        else movement = 'l';
      }
      
    }
    if (char(command) == 'f') {
      Serial.println("command: forward");
      
      distance = sonor_detect(trigPin1, echoPin1);
      if (distance < threshold) movement = 's';
      else movement = 'f';
    }
    if (char(command) == 'b') {
      Serial.println("command: backward");

      distance = sonor_detect(trigPin2, echoPin2);
      if (distance < threshold) movement = 's';
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
    delay(500);
    LFmotor -> setSpeed(spinspeed);
    LBmotor -> setSpeed(spinspeed);
    RFmotor -> setSpeed(spinspeed);
    RBmotor -> setSpeed(spinspeed);
    LFmotor -> run(FORWARD);
    LBmotor -> run(FORWARD);
    RFmotor -> run(BACKWARD);
    RBmotor -> run(BACKWARD);
    delay(spin_duration);
    LFmotor -> run(RELEASE);
    LBmotor -> run(RELEASE);
    RFmotor -> run(RELEASE);
    RBmotor -> run(RELEASE);
    LFmotor -> setSpeed(motorspeed);
    LBmotor -> setSpeed(motorspeed);
    RFmotor -> setSpeed(motorspeed);
    RBmotor -> setSpeed(motorspeed);

    movement = 's';
  }
  if (char(movement) == 'l') {
    delay(500);
    LFmotor -> setSpeed(spinspeed);
    LBmotor -> setSpeed(spinspeed);
    RFmotor -> setSpeed(spinspeed);
    RBmotor -> setSpeed(spinspeed);
    LFmotor -> run(BACKWARD);
    LBmotor -> run(BACKWARD);
    RFmotor -> run(FORWARD);
    RBmotor -> run(FORWARD);
    delay(spin_duration);
    LFmotor -> run(RELEASE);
    LBmotor -> run(RELEASE);
    RFmotor -> run(RELEASE);
    RBmotor -> run(RELEASE);
    LFmotor -> setSpeed(motorspeed);
    LBmotor -> setSpeed(motorspeed);
    RFmotor -> setSpeed(motorspeed);
    RBmotor -> setSpeed(motorspeed);
    
    movement = 's';
  }
  if (char(movement) == 'f') {
    LFmotor -> run(FORWARD);
    RFmotor -> run(FORWARD);
    LBmotor -> run(FORWARD);
    RBmotor -> run(FORWARD);
    
    distance = sonor_detect(trigPin1, echoPin1);
    if (distance < threshold) movement = 's';
    else movement = 'f';
  }
  if (char(movement) == 'b') {
    LFmotor -> run(BACKWARD);
    RFmotor -> run(BACKWARD);
    LBmotor -> run(BACKWARD);
    RBmotor -> run(BACKWARD);
    
    distance = sonor_detect(trigPin2, echoPin2);
    if (distance < threshold) movement = 's';
    else movement = 'b';
  }
  if (char(movement) == 's') {
    LFmotor -> run(RELEASE);
    RFmotor -> run(RELEASE);
    LBmotor -> run(RELEASE);
    RBmotor -> run(RELEASE);
    
    movement = 's';
  }

  delay(200);

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
