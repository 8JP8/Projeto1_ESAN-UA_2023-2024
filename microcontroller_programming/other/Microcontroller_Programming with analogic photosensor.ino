// Define pins for three LEDs
int led2Pin = P2_4; // RED LED
int led1Pin = P2_5; // GREEN LED
int led3Pin = P1_5; // BLUE LED's

int sensorPin = A0; // Analog pin for photoelectric sensor

// Variables to store PWM values for each LED
int led1PWM = 0;
int led2PWM = 0;
int led3PWM = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize PWM pins for LEDs
  analogWrite(led1Pin, led1PWM);
  analogWrite(led2Pin, led2PWM);
  analogWrite(led3Pin, led3PWM);
}

void loop() {
  // Read photoelectric sensor state
  int sensorValue = analogRead(sensorPin);

  // Send sensor state to Python script
  Serial.print("SENSOR,");
  Serial.println(sensorValue);

  // Check for serial data
  if (Serial.available() > 0) {
    // Read the incoming data
    String data = Serial.readStringUntil('\n');

    // Parse the command
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      String component = data.substring(0, commaIndex);
      String valueStr = data.substring(commaIndex + 1);
      int value = valueStr.toInt();

      // Update PWM values based on the received command
      if (component == "LED1") {
        led1PWM = value;
        analogWrite(led1Pin, led1PWM);
      } else if (component == "LED2") {
        led2PWM = value;
        analogWrite(led2Pin, led2PWM);
      } else if (component == "LED3") {
        led3PWM = value;
        analogWrite(led3Pin, led3PWM);
      }
    }
  }
}
