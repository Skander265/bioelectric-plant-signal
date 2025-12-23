import csv
import time
import os
import datetime

class EventLogger:
    def __init__(self, folder_name="log"):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created new log directory: {folder_name}/")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filepath = os.path.join(folder_name, f"session_{timestamp}.csv")
        
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Event_Type", "Peak_Voltage", "Duration_ms"])
            
        print(f"Logging session started: {self.filepath}")

    def log_event(self, event_type, peak, duration):
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.writer(f)
            
            log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            writer.writerow([log_time, event_type, f"{peak:.2f}", duration])
