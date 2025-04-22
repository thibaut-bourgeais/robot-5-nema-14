#include "StepperAS5600.h"
#include "StepperManager.h"

const int enPin = 8;
const int stepXPin = 2;  //X.STEP
const int dirXPin = 5;   // X.DIR
const int stepYPin = 3;  //Y.STEP
const int dirYPin = 6;   // Y.DIR
const int stepZPin = 4;  //Z.STEP
const int dirZPin = 7;   // Z.DIR
const int sensorVcc = 12;


stepperAS5600 moteur(stepYPin, dirYPin, enPin, sensorVcc);  // STEP, DIR, VCC_AS5600, ENABLE
StepperManager manager;

void setup() {
  Serial.begin(115200);

  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);

  moteur.begin();
  moteur.setTargetAngle(90);  // position de consigne
  manager.addMotor(&moteur);
}

void loop() {
  manager.updateAll();
  handleBinarySerial();

  //delay(1); // boucle souple
}

void handleBinarySerial() {
  while (Serial.available() >= 6) {
    uint8_t id = Serial.read();
    uint8_t cmd = Serial.read();

    union { float f; uint8_t b[4]; } data;
    Serial.readBytes(data.b, 4);  // lecture du float

    stepperAS5600* m = manager.get(id);
    if (!m) return;

    switch (cmd) {
      case 0x01: m->setKp(data.f); break;
      case 0x02: m->setKi(data.f); break;
      case 0x03: m->setTargetAngle(data.f); break;
      case 0x04: m->setMaxStepRate(data.f); break;
    }
  }
}
