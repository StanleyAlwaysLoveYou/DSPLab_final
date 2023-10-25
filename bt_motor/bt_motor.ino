
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
  R_servo.attach(10);
}


// main loop - oscillate L and R servos accordingly
void loop (void){
  if (btSerial.available()) {
    command = btSerial.read();

    if (char(command) == 'L') {
      if (L_increasing) {
        L_pos++;
      } else {
        L_pos--;
      }
    Serial.print("left: ");  // Debug
    Serial.println(L_pos);
    } else if (char(command) == 'R') {
      if (R_increasing) {
        R_pos++;
      } else {
        R_pos--;
      }
    Serial.print("right: ");
    Serial.println(R_pos);
    }
  }

  // Servos work by pulse width modulation,
  // so continuously write their position
  L_servo.write(L_pos);
  R_servo.write(R_pos);
  delay(10);

  if (L_pos == 0) {
    L_increasing = true;
  } else if (L_pos == 180) {
    L_increasing = false;
  }

  if (R_pos == 0) {
    R_increasing = true;
  } else if (R_pos == 180) {
    R_increasing = false;
  }
}  // end of loop
