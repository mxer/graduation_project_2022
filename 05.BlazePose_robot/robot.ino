#include <Servo.h>

Servo coreservo; //Name the Servo

int x=0;

void setup() {
  /*Attach the named servo object to Digital IO 13, use following syntax: 
  servoname.attach(Pin#, minimum Pulse width (ms), maximum pulse width (ms)); 
  if you want to define the pulse widths for your motor*/
  Serial.begin(115200);
  Serial.setTimeout(1);
  coreservo.attach(10);
}

void loop() {
  /* If you wanted to read the angle of your servo at any given time, use servoname.read();
   * If you wanted to write a pulse of a certain width use servoname.writemicroseconds(value in microseconds);
   */
  while (!Serial.available());
  x = Serial.readString().toInt();
  coreservo.write(x);
  //delay(100); 
}
