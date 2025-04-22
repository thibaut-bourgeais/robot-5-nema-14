//StepperManager.h

#ifndef STEPPER_MANAGER_H
#define STEPPER_MANAGER_H

#include <Arduino.h>
#include "StepperAS5600.h"

#define MAX_MOTORS 4

class StepperManager {
public:
  void addMotor(stepperAS5600* motor);
  void updateAll();
  stepperAS5600* get(uint8_t id);


private:
  stepperAS5600* motors[MAX_MOTORS];
  uint8_t motorCount = 0;
  uint8_t currentMotorIndex = 0;
};

#endif
