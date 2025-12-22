import threading
import queue
import time
import matplotlib.pyplot as plt

import plot.live_plot as live_plot
import utils.noise_filter as noise_filter
import processing.signal_analyst as signal_analyst
import reader.serial_reader as serial_reader  
import reader.mock_reader as mock_reader  

#  WORKER THREAD 
def data_worker(data_queue, stop_event):
    detected_port = serial_reader.find_available_port()
    
    if detected_port:
        print(f"Hardware Detected on {detected_port}. Starting SERIAL mode.")
        mode = 'SERIAL'
        source = serial_reader.connect_serial(detected_port)
    else:
        print("No Hardware Found. Starting MOCK mode.")
        mode = 'MOCK'
        source = mock_reader.MockReader()

    filter_tool = noise_filter.MovingAverageFilter(window_size=5)
    brain = signal_analyst.SignalAnalyst()
    
    print("Worker thread active...")

    while not stop_event.is_set():
        # Read Data based on mode
        if mode == 'SERIAL':
            t, v = serial_reader.read_line(source)
        else:
            t, v = source.read_line()

        if v is None: 
            time.sleep(0.001) # Prevent CPU spiking on empty reads
            continue

        # Process Data
        smooth_v = filter_tool.apply(v)
        status = brain.update(smooth_v)

        # Send to GUI
        packet = {
            'time': t, 
            'voltage': smooth_v, 
            'status': status
        }
        data_queue.put(packet)

def main():
    fig, ax, line, x_data, y_data = live_plot.setup_plot()
    
    # Setup Threading
    data_queue = queue.Queue()
    stop_event = threading.Event()

    worker = threading.Thread(target=data_worker, args=(data_queue, stop_event))
    worker.daemon = True 
    worker.start()

    print(f"Starting Plant Security System...")
    alarm_count = 0

    try:
        while True:
            while not data_queue.empty():
                packet = data_queue.get()
                t = packet['time']
                v = packet['voltage']
                status = packet['status']

                # Update Graph
                live_plot.update_plot(fig, ax, line, x_data, y_data, t, v)
                
                # Update Status / Security System
                if "ACTION: INTRUDER_ALARM" in status:
                    ax.set_title(f"SECURITY ALERT TRIGGERED!", color='red', fontsize=14, fontweight='bold')
                    alarm_count += 1
                    print(f"ALARM! Voltage: {v:.2f}V | Total Events: {alarm_count}")
                    
                elif "REJECTED" in status:
                    ax.set_title(f"Filtered: {status}", color='orange', fontsize=10)
                elif "IGNORE" in status:
                    ax.set_title("Status: Environment Noise Ignored", color='gray')
                elif "Scanning" in status:
                    if "ALERT" not in ax.get_title():
                        ax.set_title(f"System Armed. Intrusions: {alarm_count}", color='green')

            plt.pause(0.05) 

    except KeyboardInterrupt:
        print("\nStopping...")
        stop_event.set()
        worker.join()

if __name__ == "__main__":
    main()