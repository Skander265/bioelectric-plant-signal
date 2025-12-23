from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
from utils import logger

class PlantMonitorWindow(QtWidgets.QMainWindow):
    def __init__(self, data_queue, stop_event, leaf_count, total_sensors):
        super().__init__()
        self.data_queue = data_queue
        self.stop_event = stop_event
        self.leaf_count = leaf_count
        self.total_sensors = total_sensors
        
        self.logger = logger.EventLogger()
        self.alarm_count = 0

        self.setWindowTitle(f"Botanical Intrusion Detector ({self.leaf_count} Leaf Node Superposition)")
        self.resize(1000, 900)
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Header
        self.status_label = QtWidgets.QLabel("Network Status: MONITORING")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FF00; padding: 10px;")
        main_layout.addWidget(self.status_label)

        # --- PLOT SETUP ---
        self.curves = [] 
        self.data_buffers = [np.zeros(500) for _ in range(self.total_sensors)]
        
        #ROOT PLOT 
        self.root_plot = pg.PlotWidget(title="ROOT SYSTEM (Channel 1)")
        self.root_plot.setYRange(0, 5)
        self.root_plot.showGrid(x=True, y=True, alpha=0.3)
        root_curve = self.root_plot.plot(pen=pg.mkPen(color='#FFA500', width=2))
        self.curves.append(root_curve)
        main_layout.addWidget(self.root_plot)

        #STEM PLOT
        self.stem_plot = pg.PlotWidget(title="MAIN STEM (Channel 2)")
        self.stem_plot.setYRange(0, 5)
        self.stem_plot.showGrid(x=True, y=True, alpha=0.3)
        stem_curve = self.stem_plot.plot(pen=pg.mkPen(color='#00CCFF', width=2))
        self.curves.append(stem_curve)
        main_layout.addWidget(self.stem_plot)

        #LEAVES PLOT (Superposed)
        self.leaf_plot = pg.PlotWidget(title=f"LEAF NETWORK ({self.leaf_count} Superposed Sensors)")
        self.leaf_plot.setYRange(0, 5)
        self.leaf_plot.showGrid(x=True, y=True, alpha=0.3)
        
        for i in range(self.leaf_count):
            leaf_curve = self.leaf_plot.plot(pen=pg.mkPen(color=(0, 255, 0, 180), width=1)) 
            self.curves.append(leaf_curve)
            
        main_layout.addWidget(self.leaf_plot)

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(16)

    def update_gui(self):
        while not self.data_queue.empty():
            packet = self.data_queue.get()
            voltages = packet['voltages']
            statuses = packet['statuses']

            for i in range(self.total_sensors):
                self.data_buffers[i] = np.roll(self.data_buffers[i], -1)
                self.data_buffers[i][-1] = voltages[i]
                
                # check alarms
                self.check_status(i, statuses[i])

        for i in range(self.total_sensors):
            self.curves[i].setData(self.data_buffers[i])

    def check_status(self, idx, status_dict):
        event_type = status_dict.get("type", "UNKNOWN")
        
        if event_type == "ALARM":
            location = self.get_location_name(idx)
            self.status_label.setText(f"ANOMALY DETECTED: {location}")
            self.status_label.setStyleSheet("color: red; font-size: 24px; font-weight: bold;")
            self.logger.log_event(f"ALARM_{location}", status_dict['peak'], status_dict['duration'])
            
        elif event_type == "LEARNING":
            msg = status_dict.get("message", "Calibrating...")
            self.status_label.setText(f"TRAINING: {msg}")
            self.status_label.setStyleSheet("color: yellow; font-size: 18px;")
            
        elif event_type == "CALIBRATION_COMPLETE":
            self.status_label.setText("MODEL TRAINED")
            self.status_label.setStyleSheet("color: #00FF00; font-size: 18px; font-weight: bold;")

    def get_location_name(self, idx):
        if idx == 0: return "ROOT"
        elif idx == 1: return "STEM"
        else: return f"LEAF {idx-1}"

    def closeEvent(self, event):
        self.stop_event.set()
        event.accept()