#include <Servo.h>

Servo servo;

const int trigPin = 7;
const int echoPin = 6;
const int servoPin = 9;

unsigned long lastMeasure = 0;

void setup()
{
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  servo.attach(servoPin);
  servo.write(0);

  Serial.begin(115200);
}

void loop()
{
  // Send ultrasonic distance to the computer every 100 ms.
  if (millis() - lastMeasure >= 100)
  {
    lastMeasure = millis();

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);

    digitalWrite(trigPin, LOW);

    unsigned long duration = pulseIn(echoPin, HIGH, 30000);

    if (duration > 0)
    {
      float distance = duration * 0.0343 / 2.0;

      // Serial protocol: D:<distance_cm>
      Serial.print("D:");
      Serial.println(distance);
    }
  }

  // Receive servo commands from ROS 2 through the serial bridge.
  if (Serial.available())
  {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Expected command: S:<angle>, e.g. S:90
    if (command.startsWith("S:"))
    {
      int angle = command.substring(2).toInt();
      angle = constrain(angle, 0, 180);
      servo.write(angle);
    }
  }
}
