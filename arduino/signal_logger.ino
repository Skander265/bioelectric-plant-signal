const int pins[] = {A0, A1, A2}; //3 pins for 3 sensors
const int numSensors = 3;

void setup() {
  Serial.begin(115200);
}

void loop() {
  unsigned long currentTime = millis();
  Serial.print(currentTime);

  for (int i = 0; i < numSensors; i++) {
    int raw = analogRead(pins[i]);
    float voltage = (raw / 1023.0) * 5.0; //convert to volt
    Serial.print(",");
    Serial.print(voltage);
  }
  Serial.println(); 
  delay(10);
}