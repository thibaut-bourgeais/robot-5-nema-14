//StepperManager.cpp

#include <Arduino.h>
#include <Vector.h>
#include "StepperManager.h"

void StepperManager::addMotor(stepperAS5600* motor) {
  if (motorCount < MAX_MOTORS) {
    motors[motorCount++] = motor;
  }
}

void StepperManager::updateAll() {
  if (motorCount == 0) return;

  stepperAS5600* current = motors[currentMotorIndex];
  current->update();

  if (!current->isSensorActive()) {
    currentMotorIndex = (currentMotorIndex + 1) % motorCount;
  }
}

stepperAS5600* StepperManager::get(uint8_t id) {
  if (id >= motorCount) return nullptr;
  return motors[id];
}
