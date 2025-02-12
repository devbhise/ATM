#include <Servo.h>

Servo cashMotor;

void setup() {
    cashMotor.attach(9);
    pinMode(13, OUTPUT);
}

void loop() {
    if (Serial.available()) {
        char command = Serial.read();
        if (command == 'W') {
            digitalWrite(13, HIGH);
            cashMotor.write(90);
            delay(2000);
            cashMotor.write(0);
            digitalWrite(13, LOW);
        }
    }
}

