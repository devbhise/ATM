const int in1Pin = 8; // IN1 pin of L298N motor driver
const int in2Pin = 9; // IN2 pin of L298N motor driver
const int enPin = 10; // EN1 pin of L298N motor driver

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud
  pinMode(in1Pin, OUTPUT); // Set IN1 pin as an output
  pinMode(in2Pin, OUTPUT); // Set IN2 pin as an output
  pinMode(enPin, OUTPUT); // Set EN1 pin as an output
  digitalWrite(in1Pin, LOW); // Turn off the motor initially
  digitalWrite(in2Pin, LOW); // Turn off the motor initially
  analogWrite(enPin, 0); // Set motor speed to 0 initially
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming command

    if (command == "WITHDRAW") {
      // Turn on the motor
      digitalWrite(in1Pin, HIGH);
      digitalWrite(in2Pin, LOW);
      analogWrite(enPin, 255); // Set motor speed to maximum

      delay(1000); // Run the motor for 1 second (adjust as needed)

      // Turn off the motor
      digitalWrite(in1Pin, LOW);
      digitalWrite(in2Pin, LOW);
      analogWrite(enPin, 0); // Set motor speed to 0

      Serial.println("OK"); // Send the response back to the Python script
    }
  }
}