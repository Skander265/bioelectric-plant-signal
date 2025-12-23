from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class PlantBioLauncher(QtWidgets.QDialog):
    def __init__(self, current_config):
        super().__init__()
        self.config = current_config
        self.launch_approved = False #tracks if user clicked "Start"

        self.setWindowTitle("Botanical Intrusion Interface - Setup")
        self.resize(800, 900)
        self.setStyleSheet("""
            QDialog { 
                background-color: #1e1e1e; 
                color: #e0e0e0; 
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel { 
                color: #e0e0e0; 
                font-size: 36px; 
            }
            /* Group Box Styling */
            QGroupBox { 
                border: 2px solid #333; 
                border-radius: 8px; 
                margin-top: 20px; 
                font-weight: bold; 
                font-size: 34px;
                color: #00FF00; 
                padding-top: 20px;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 15px; 
                padding: 0 5px; 
                background-color: #1e1e1e;
            }
            /* Radio Button & Input Styling */
            QRadioButton { 
                spacing: 10px; 
                font-size: 35px;
                padding: 5px;
                color: white;           
            }
            QRadioButton::indicator { 
                width: 20px; 
                height: 20px; 
            }
            QSpinBox { 
                background-color: #333; 
                color: #00FF00; 
                font-size: 36px; 
                padding: 8px; 
                border: 1px solid #555; 
                border-radius: 4px; 
                font-weight: bold;
            }
            /* Button Styling */
            QPushButton { 
                background-color: #006600; 
                color: white; 
                border-radius: 8px; 
                padding: 15px; 
                font-size: 38px; 
                font-weight: bold; 
                letter-spacing: 1px;
            }
            QPushButton:hover { 
                background-color: #008800; 
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)

        #1 Title/Welcome
        title = QtWidgets.QLabel("🌱 Botanical Intrusion Detector")
        title.setStyleSheet("font-size: 34px; font-weight: bold; color: #00FF00; margin-bottom: 10px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QtWidgets.QLabel("configure your session parameters")
        subtitle.setStyleSheet("color: #aaaaaa; font-style: italic;")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle)

        #2 Mode Selection (Train vs Monitor)
        mode_group = QtWidgets.QGroupBox("Session Mode")
        mode_layout = QtWidgets.QVBoxLayout()
        
        self.radio_monitor = QtWidgets.QRadioButton("MONITOR (Load Existing Models)")
        self.radio_monitor.setChecked(not self.config['force_retrain'])
        self.radio_monitor.setToolTip("Use previously trained AI models. Ready instantly.")
        
        self.radio_train = QtWidgets.QRadioButton("CALIBRATE (Retrain AI)")
        self.radio_train.setChecked(self.config['force_retrain'])
        self.radio_train.setToolTip("Delete old models and learn from scratch.")
        
        mode_layout.addWidget(self.radio_monitor)
        mode_layout.addWidget(self.radio_train)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        #3 Sensor Configuration
        sensor_group = QtWidgets.QGroupBox("Network Topology")
        sensor_layout = QtWidgets.QFormLayout()
        
        self.leaf_spinner = QtWidgets.QSpinBox()
        self.leaf_spinner.setRange(1, 100)
        self.leaf_spinner.setValue(self.config['leaf_sensor_count'])
        self.leaf_spinner.setStyleSheet("background-color: #444; color: white; padding: 5px;")
        
        sensor_layout.addRow("Number of Leaf Nodes:", self.leaf_spinner)
        sensor_group.setLayout(sensor_layout)
        layout.addWidget(sensor_group)

        #4 Filter Settings
        filter_group = QtWidgets.QGroupBox("Signal Processing")
        filter_layout = QtWidgets.QFormLayout()
        
        self.smooth_spinner = QtWidgets.QSpinBox()
        self.smooth_spinner.setRange(1, 50)
        self.smooth_spinner.setValue(self.config['filter_window_size'])
        self.smooth_spinner.setStyleSheet("background-color: #444; color: white; padding: 5px;")

        self.chk_audio = QtWidgets.QCheckBox("Enable Bio-Synth Audio")
        self.chk_audio.setChecked(self.config.get('enable_audio', False))
        self.chk_audio.setStyleSheet("font-size: 35px; color: #00FF00; spacing: 10px;")
        self.chk_audio.setToolTip("Generates real-time audio based on plant voltage.")
        
        filter_layout.addRow("Smoothing Window:", self.smooth_spinner)
        filter_layout.addRow(self.chk_audio)

        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        # Spacer
        layout.addStretch()

        #5 Start Button
        self.btn_start = QtWidgets.QPushButton("INITIALIZE SYSTEM")
        self.btn_start.clicked.connect(self.start_system)
        layout.addWidget(self.btn_start)

    def start_system(self):
        self.config['leaf_sensor_count'] = self.leaf_spinner.value()
        self.config['filter_window_size'] = self.smooth_spinner.value()
        self.config['force_retrain'] = self.radio_train.isChecked()
        self.config['enable_audio'] = self.chk_audio.isChecked()
        
        self.launch_approved = True
        self.accept() 