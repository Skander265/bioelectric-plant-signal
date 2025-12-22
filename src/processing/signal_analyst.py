import numpy as np

class SignalAnalyst:
    def __init__(self):
        self.threshold = 1.0 
        self.recording = False
        self.buffer = [] 
        
    def update(self, voltage):
        if not self.recording:
            if voltage > self.threshold:
                self.recording = True
                self.buffer = [voltage]
                return "Recording..."
            return "Scanning"

        else:
            self.buffer.append(voltage)
            
            # Stop recording if signal drops or gets too long
            if (len(self.buffer) > 10 and voltage < self.threshold) or len(self.buffer) > 100:
                result = self.analyze_features(self.buffer)
                self.recording = False
                self.buffer = [] 
                return result
                
            return "Recording..."

    def analyze_features(self, data):
        data_array = np.array(data)
        peak = np.max(data_array)
        duration = len(data_array)
                
        # Rule 1: It's a TOUCH if it's sharp and high
        if peak > 2.0 and duration < 25:
            return "ACTION: INTRUDER_ALARM"
        
        # Rule 2: It's NOISE if it's long and low
        elif duration >= 25:
             return "IGNORE: Background Noise"
        
        else:
            # If it failed, tell us which rule broke
            reasons = []
            if peak <= 2.0: reasons.append(f"Weak Signal ({peak:.2f}V)")
            if duration >= 25: reasons.append(f"Too Long ({duration}ms)")
            
            return f"REJECTED: {', '.join(reasons)}"