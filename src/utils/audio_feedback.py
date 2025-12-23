import threading
import time
import winsound

class AudioSynthesizer:
    def __init__(self):
        self.active = False
        self.current_voltage = 0.5
        self.thread = None
        self.running = False

    def start(self):
        """Starts the audio engine in a background thread."""
        if not self.active:
            self.active = True
            self.running = True
            self.thread = threading.Thread(target=self._audio_loop)
            self.thread.daemon = True  # Kills thread if app closes
            self.thread.start()
            print("Audio Engine Started")

    def stop(self):
        """Stops the audio engine."""
        self.running = False
        self.active = False

    def update_voltage(self, voltage):
        """Updates the target pitch based on sensor voltage."""
        self.current_voltage = voltage

    def _audio_loop(self):
        """Internal loop that generates sound."""
        while self.running:
            # Formula: 
            target_freq = int(100 + (self.current_voltage * 300))
            
            #Safety Limits for frequency
            if target_freq < 40: target_freq = 40
            if target_freq > 5000: target_freq = 5000
            
            # 3. Play Sound
            try:
                winsound.Beep(target_freq, 100)
            except RuntimeError:
                pass 
            
