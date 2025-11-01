#include <Wire.h>
#include <SoftwareSerial.h>
// Bluetooth TX/RX
SoftwareSerial bt(10, 11); // RX | TX
// MPU6050 registers
#define MPU_ADDR 0x68
#define REG_PWR_MGMT_1 0x6B
#define REG_ACCEL_XOUT_H 0x3B
#define REG_GYRO_XOUT_H  0x43
// Sensitivities
const float ACCEL_SENS = 16384.0;
const float GYRO_SENS  = 131.0;
// Orientation variables
float roll = 0.0f, pitch = 0.0f, yaw = 0.0f;
float gx_bias = 0, gy_bias = 0, gz_bias = 0;
unsigned long lastMicros = 0;
const float alpha = 0.98f;
int16_t read16(int reg) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 2, true);
  int16_t hi = Wire.read();
  int16_t lo = Wire.read();
  return (hi << 8) | lo;
}
void readMPU(float &ax, float &ay, float &az, float &gx, float &gy, float &gz) {
  int16_t rawAX = read16(REG_ACCEL_XOUT_H);
  int16_t rawAY = read16(REG_ACCEL_XOUT_H + 2);
  int16_t rawAZ = read16(REG_ACCEL_XOUT_H + 4);
  int16_t rawGX = read16(REG_GYRO_XOUT_H);
  int16_t rawGY = read16(REG_GYRO_XOUT_H + 2);
  int16_t rawGZ = read16(REG_GYRO_XOUT_H + 4);
  ax = (float)rawAX / ACCEL_SENS;
  ay = (float)rawAY / ACCEL_SENS;
  az = (float)rawAZ / ACCEL_SENS;
  gx = (float)rawGX / GYRO_SENS - gx_bias;
  gy = (float)rawGY / GYRO_SENS - gy_bias;
  gz = (float)rawGZ / GYRO_SENS - gz_bias;
}
void calibrateGyro(int samples = 500) {
  long sumX = 0, sumY = 0, sumZ = 0;
  for (int i = 0; i < samples; i++) {
    int16_t rawGX = read16(REG_GYRO_XOUT_H);
    int16_t rawGY = read16(REG_GYRO_XOUT_H + 2);
    int16_t rawGZ = read16(REG_GYRO_XOUT_H + 4);
    sumX += rawGX;
    sumY += rawGY;
    sumZ += rawGZ;
    delay(2);
  }
  gx_bias = (sumX / (float)samples) / GYRO_SENS;
  gy_bias = (sumY / (float)samples) / GYRO_SENS;
  gz_bias = (sumZ / (float)samples) / GYRO_SENS;
}
void setup() {
  Serial.begin(38400);
  bt.begin(38400);
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(REG_PWR_MGMT_1);
  Wire.write(0x00);
  Wire.endTransmission(true);
  delay(100);
  calibrateGyro(600);
  float ax, ay, az, gx, gy, gz;
  readMPU(ax, ay, az, gx, gy, gz);
  roll  = atan2(ay, az) * 180.0 / PI;
  pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;
  lastMicros = micros();
}
void loop() {
  float ax, ay, az, gx, gy, gz;
  readMPU(ax, ay, az, gx, gy, gz);
  unsigned long now = micros();
  float dt = (now - lastMicros) / 1e6;
  lastMicros = now;
  float acc_roll  = atan2(ay, az) * 180.0 / PI;
  float acc_pitch = atan2(-ax, sqrt(ay*ay + az*az)) * 180.0 / PI;
  roll  = alpha * (roll + gx * dt) + (1 - alpha) * acc_roll;
  pitch = alpha * (pitch + gy * dt) + (1 - alpha) * acc_pitch;
  yaw   += gz * dt;
  // Send via Bluetooth as CSV
  bt.print(pitch, 3); bt.print(',');
  bt.print(roll, 3); bt.print(',');
  bt.println(yaw, 3);
  delay(10);
}