
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

void setup (void)
{
  pinMode(LED_BUILTIN, OUTPUT);

  // Setup and flush the serials to begin
  btSerial.begin(38400);
  Serial.begin(9600);
  btSerial.flush();
  Serial.flush();

  // attach to pins 9 and 10 (servo outputs)
  L_servo.attach(9);
  L_servo.write(90);

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
    }
    if (char(command) == 'l') {
      Serial.println("command: left");
      L_servo.write(180);
      delay(1000);
    }
    if (char(command) == 'f') {
      Serial.println("command: forward");
    }
    if (char(command) == 'b') {
      Serial.println("command: backward");
    }
    if (char(command) == 's') {
      Serial.println("command: stop");
    }
    //Serial.print("L position: ");
    //Serial.println(L_pos);
  }

  L_servo.write(90);

  // --------------move--------------------

  
  delay(50);

}  // end of loop
