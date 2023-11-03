const int trigPin1 = 3;
const int echoPin1 = 4;

float duration, distance, tempdistance;


void setup() {
  // put your setup code here, to run once:
  pinMode (trigPin1, OUTPUT);
  pinMode (echoPin1, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  distance = sonor_detect(trigPin1, echoPin1);
  Serial.print("Distance: ");
  Serial.println(distance);
  delay(50);
}

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

  return tempdistance;  
}
