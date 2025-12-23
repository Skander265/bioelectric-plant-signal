// --- CONFIGURATION ---
const int pins[] = {A0, A1, A2, A3, A4, A5}; 

// auto calculate how many sensors are in the list above
const int numSensors = sizeof(pins) / sizeof(pins[0]);

void setup() {
  Serial.begin(115200);
}

void loop() {
  unsigned long currentTime = millis();
  Serial.print(currentTime);

  // loop automatically adjusts to however many sensors 
  for (int i = 0; i < numSensors; i++) {
    int raw = analogRead(pins[i]);
    float voltage = (raw / 1023.0) * 5.0; 
    
    Serial.print(",");
    Serial.print(voltage);
  }
  
  Serial.println(); 
  delay(10); // 100 samples per second
}