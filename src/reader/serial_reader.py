import serial
import serial.tools.list_ports
import time

def find_available_port():
    """
    Scans for available serial ports.
    Returns the port name (e.g., 'COM3') if found, else None.
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:

        print(f"Found Device: {port.device} - {port.description}")
        return port.device 
    return None

def connect_serial(port, baudrate=115200, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  
        
        ser.reset_input_buffer()
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to {port}: {e}")
        return None

def read_line(ser):
    if ser is None: return None, None
    
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if not line or "timestamp" in line:
                return None, None
                
            if ',' in line:
                timestamp_str, voltage_str = line.split(',')
                
                voltage_mv = float(voltage_str)
                voltage_v = voltage_mv / 1000.0 
                
                return int(timestamp_str), voltage_v
                
    except Exception as e:
        pass
        
    return None, None