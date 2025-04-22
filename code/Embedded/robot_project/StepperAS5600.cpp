//StepperAS5600.cpp

#include <Arduino.h>
#include "StepperAS5600.h"
#include <Wire.h>


stepperAS5600::stepperAS5600(uint8_t pinStep, uint8_t pinDir, uint8_t pinEnable, uint8_t vccAS5600, uint8_t i2cAddress = 0x36, float gearRatio = 1.0f)
  : pinStep(pinStep), pinDir(pinDir), pinEnable(pinEnable), vccAS5600(vccAS5600), i2cAddress(i2cAddress), gearRatio(gearRatio) {}

void stepperAS5600::begin() {
  pinMode(pinStep, OUTPUT);
  pinMode(pinDir, OUTPUT);
  pinMode(pinEnable, OUTPUT);
  pinMode(vccAS5600, OUTPUT);
  digitalWrite(vccAS5600, LOW);  // capteur off par défaut
  Wire.begin();
  lastUpdateMicros = micros();
  engage();
}

void stepperAS5600::setTargetAngle(float angleDeg) {
  targetAngle = fmod(angleDeg, 360.0f);
  if (targetAngle < 0) targetAngle += 360.0f;
}

void stepperAS5600::startSensorRead() {
  if (!sensorActive) {
    digitalWrite(vccAS5600, HIGH);
    sensorActivationTime = micros();
    sensorActive = true;
  }
}

bool stepperAS5600::isSensorActive() const {
  return sensorActive;
}

void stepperAS5600::update() {

  unsigned long now = micros();
  float dt = (now - lastUpdateMicros) / 1e6f;
  lastUpdateMicros = now;

  if (!sensorActive) {
    startSensorRead();  // Allume le capteur, démarre le timer
    return;             // On attend
  }

  // Attente non bloquante
  if (now - sensorActivationTime > turnOnTime * 1000) {
    // Lecture capteur + désactivation
    currentAngle = readAngle();
    digitalWrite(vccAS5600, LOW);
    sensorActive = false;
  }

  /*
  Serial.print("[DEBUG] Angle: ");
  Serial.println(currentAngle, 2);
  Serial.print(" | Target: ");
  Serial.println(targetAngle, 2);
  */

  float error = angleDifference(targetAngle, currentAngle);
  /*if (abs(error) < 1.0) {
    release();  // coupe le courant si bien positionné
  } else {
    engage();  // réactive si erreur trop grande
  }*/
  integral += error * dt;
  integral = constrain(integral, -integralLimit, integralLimit);

  float command = Kp * error + Ki * integral;
  command = constrain(command, -maxStepRate(), maxStepRate());

  if (abs(command) > 5.0f) {
    interval = 1e6 / abs(command);

    if (now - lastStepTime >= interval) {
      digitalWrite(pinDir, command > 0 ? LOW : HIGH);  // ← encore !
      stepMotor();                                     // ← encore !
      lastStepTime = now;
    }
    /*
    Serial.print("E=");
    Serial.print(error, 2);
    Serial.print(" C=");
    Serial.print(command, 2);
    Serial.print(" I=");
    Serial.println(interval);
    */
  }
}

float stepperAS5600::getLastAngle() const {
  return lastAngle;
}

float stepperAS5600::getTargetAngle() const {
  return targetAngle;
}


void stepperAS5600::release() {
  digitalWrite(pinEnable, HIGH);  // ou LOW selon ton driver
}

void stepperAS5600::engage() {
  digitalWrite(pinEnable, LOW);  // ou LOW selon ton driver
}

void stepperAS5600::stepMotor() {
  digitalWrite(pinStep, HIGH);
  delayMicroseconds(50);
  digitalWrite(pinStep, LOW);
  //delayMicroseconds(30);
}

void stepperAS5600::activateSensor() {
  digitalWrite(vccAS5600, HIGH);
}

void stepperAS5600::deactivateSensor() {
  digitalWrite(vccAS5600, LOW);
}

float stepperAS5600::readAngle() {
  for (int attempt = 0; attempt < maxAttempts; attempt++) {
    Wire.beginTransmission(i2cAddress);
    Wire.write(0x0E);  // ANGLE MSB
    Wire.endTransmission(false);
    Wire.requestFrom(i2cAddress, (uint8_t)2);

    if (Wire.available() >= 2) {
      uint16_t raw = (Wire.read() << 8) | Wire.read();
      float angle = (raw * 360.0f) / 4096.0f / gearRatio;
      lastAngle = angle;
      return angle;
    }

    delayMicroseconds(10);  // court délai avant de réessayer
  }

  // Après toutes les tentatives échouées
  Serial.println("[WARN] AS5600 read failed after 5 attempts.");
  return lastAngle;
}


float stepperAS5600::angleDifference(float target, float current) {
  float diff = target - current;
  if (diff > 180.0f) diff -= 360.0f;
  if (diff < -180.0f) diff += 360.0f;
  return diff;
}

float stepperAS5600::maxStepRate() const {
  return stepRateLimit;
}
