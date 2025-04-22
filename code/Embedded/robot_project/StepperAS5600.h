//StepperAS5600.h

#ifndef STEPPER_AS5600_H
#define STEPPER_AS5600_H

#include <Arduino.h>

class stepperAS5600 {
public:
  stepperAS5600(uint8_t pinStep, uint8_t pinDir, uint8_t pinEnable, uint8_t vccAS5600, uint8_t i2cAddress = 0x36, float gearRatio = 1.0f);

  void begin();
  void setTargetAngle(float angleDeg);
  float getTargetAngle() const;
  float getLastAngle() const;
  void update();
  void release();
  void engage();
  bool isSensorActive() const;
  void setKp(float val) {
    Kp = val;
  }
  void setKi(float val) {
    Ki = val;
  }
  void setMaxStepRate(float val) {
    stepRateLimit = val;
  }


private:
  uint8_t pinStep, pinDir, vccAS5600;
  int8_t pinEnable;
  uint8_t i2cAddress;
  float gearRatio;
  float targetAngle = 0.0f;
  float lastAngle = 0.0f;

  float stepRateLimit = 2000.0f;
  float Kp = 200.0f;
  float Ki = 5.0f;
  float integral = 0.0f;
  float integralLimit = 100.0f;
  unsigned long interval = 0;

  unsigned long lastStepTime = 0;
  unsigned long lastUpdateMicros = 0;

  bool sensorActive = false;
  unsigned long sensorActivationTime = 0;
  unsigned int maxAttempts = 5;
  unsigned int turnOnTime = 1000;  // µs
  float currentAngle = 0;

  void stepMotor();
  void activateSensor();
  void deactivateSensor();
  float readAngle();
  void startSensorRead();
  float angleDifference(float target, float current);
  float maxStepRate() const;
};

#endif
