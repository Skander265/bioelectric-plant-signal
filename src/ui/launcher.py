from PyQt5 import QtWidgets, QtCore, QtGui
import sys

APP_NAME = "Bio-Telemetry Interface"

class PlantBioLauncher(QtWidgets.QDialog):
    def __init__(self, current_config):
        super().__init__()
        self.config = current_config
        self.launch_approved = False 

        self.setWindowTitle(f"{APP_NAME} - Setup")
        self.resize(650, 800)
        
        self.setStyleSheet("""
            QDialog { 
                background-color: #121212; 
                color: #e0e0e0; 
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel { 
                color: #e0e0e0; 
                font-size: 36px; 
            }
            /* Group Box */
            QGroupBox { 
                border: 1px solid #333; 
                border-radius: 6px; 
                margin-top: 24px; 
                font-weight: bold; 
                font-size: 34px;
                color: #00FF99; /* Neon Green Title */
                background-color: #1a1a1a;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px; 
            }
            
            /* Inputs & Spinners */
            QSpinBox { 
                background-color: #222; 
                color: #00FF99; 
                font-size: 38px; 
                padding: 8px; 
                border: 1px solid #444; 
                border-radius: 4px; 
                font-weight: bold;
            }
            QRadioButton { 
                spacing: 12px; 
                font-size: 35px;
                color: #ccc;
                padding: 8px;
            }
            QRadioButton::indicator { 
                width: 18px; 
                height: 18px; 
                border-radius: 9px;
                border: 2px solid #555;
            }
            QRadioButton::indicator:checked { 
                background-color: #00FF99;
                border-color: #00FF99;
            }
            
            /* Checkbox */
            QCheckBox {
                font-size: 35px;
                color: #ccc;
                spacing: 10px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px; height: 18px;
                border: 2px solid #555; border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #00CCFF; /* Cyan for Audio */
                border-color: #00CCFF;
            }

            /* Main Button */
            QPushButton { 
                background-color: #006644; 
                color: white; 
                border-radius: 6px; 
                padding: 15px; 
                font-size: 30px; 
                font-weight: bold; 
                border: 1px solid #008855;
            }
            QPushButton:hover { 
                background-color: #009966; 
                border-color: #00FF99;
                color: #ffffff;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QtWidgets.QLabel(f"🌿 {APP_NAME}")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #00FF99; margin-bottom: 5px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QtWidgets.QLabel("System Configuration & Topology")
        subtitle.setStyleSheet("color: #666; font-size: 14px; font-style: italic; margin-bottom: 20px;")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle)

        mode_group = QtWidgets.QGroupBox("OPERATIONAL MODE")
        mode_layout = QtWidgets.QVBoxLayout()
        mode_layout.setSpacing(5)
        mode_layout.setContentsMargins(15, 25, 15, 15)
        
        self.radio_monitor = QtWidgets.QRadioButton("MONITOR (Active Security)")
        self.radio_monitor.setChecked(not self.config['force_retrain'])
        
        self.radio_train = QtWidgets.QRadioButton("CALIBRATE (Model Retraining)")
        self.radio_train.setChecked(self.config['force_retrain'])
        
        mode_layout.addWidget(self.radio_monitor)
        mode_layout.addWidget(self.radio_train)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        sensor_group = QtWidgets.QGroupBox("NETWORK TOPOLOGY")
        sensor_layout = QtWidgets.QFormLayout()
        sensor_layout.setContentsMargins(15, 25, 15, 15)
        sensor_layout.setSpacing(15)
        
        self.leaf_spinner = QtWidgets.QSpinBox()
        self.leaf_spinner.setRange(1, 100)
        self.leaf_spinner.setValue(self.config['leaf_sensor_count'])
        
        lbl_leaf = QtWidgets.QLabel("Leaf Nodes:")
        sensor_layout.addRow(lbl_leaf, self.leaf_spinner)
        sensor_group.setLayout(sensor_layout)
        layout.addWidget(sensor_group)

        filter_group = QtWidgets.QGroupBox("PROCESSING & FEEDBACK")
        filter_layout = QtWidgets.QFormLayout()
        filter_layout.setContentsMargins(15, 25, 15, 15)
        filter_layout.setSpacing(15)
        
        self.smooth_spinner = QtWidgets.QSpinBox()
        self.smooth_spinner.setRange(1, 50)
        self.smooth_spinner.setValue(self.config['filter_window_size'])
        
        self.chk_audio = QtWidgets.QCheckBox("Enable Bio-Synth Audio")
        self.chk_audio.setChecked(self.config.get('enable_audio', False))
        
        lbl_smooth = QtWidgets.QLabel("Smoothing Factor:")
        filter_layout.addRow(lbl_smooth, self.smooth_spinner)
        filter_layout.addRow(self.chk_audio)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        layout.addStretch()

        self.btn_start = QtWidgets.QPushButton(f"INITIALIZE SYSTEM")
        self.btn_start.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_start.clicked.connect(self.start_system)
        layout.addWidget(self.btn_start)

    def start_system(self):
        self.config['leaf_sensor_count'] = self.leaf_spinner.value()
        self.config['filter_window_size'] = self.smooth_spinner.value()
        self.config['force_retrain'] = self.radio_train.isChecked()
        self.config['enable_audio'] = self.chk_audio.isChecked()
        
        self.launch_approved = True
        self.accept()