import time
import numpy as np
import random

class MockReader:
    def __init__(self):
        self.start_time = int(time.time() * 1000)
        self.tick = 0

    def read_line(self):
        voltage = np.random.normal(0.5, 0.05)
        
        if self.tick % 50 == 0 and random.random() > 0.7:
            event_type = random.choice(['spike', 'wobble'])
            self.inject_event(event_type)

        if hasattr(self, 'active_event') and len(self.active_event) > 0:
            voltage += self.active_event.pop(0)

        self.tick += 1
        time.sleep(0.05) # Simulate hardware delay
        
        current_time = int(time.time() * 1000) - self.start_time
        return current_time, voltage

    def inject_event(self, type):
        if type == 'spike':
            # Create a sharp triangle wave (Touch)
            # Goes up fast, comes down fast. High amplitude.
            self.active_event = list(np.concatenate([np.linspace(0, 3.0, 5), np.linspace(3.0, 0, 10)]))
        
        elif type == 'wobble':
            # Create a slow sine wave (Wind/Noise)
            # Lower amplitude, lasts longer.
            x = np.linspace(0, 4*np.pi, 40)
            self.active_event = list(np.sin(x) * 0.8)