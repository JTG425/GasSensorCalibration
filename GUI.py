# This File should contain the main GUI Components for the project:
# 1. A Graphical Display of the Data, PPM vs Time.
# 2. A Status Indicator showing the following:
#    a. Green: Standby, Ready To Calibrate.
#    b. Yellow: Calibrating
#    c. Orange: : Calibrated, Ready to Release Into Disposal / Disposal In Progress
#    d. Red: Leak Detected, RUN.
# 3. A Plot Area that live updates based on Sensor level PPM vs Time.
# 4. A Clock that shows the current time.

import time                                         # Time Library
import random                                       # Random Number Library
import numpy as np                                  # Numpy Library (Statistical Functions)
from PyQt6.QtWidgets import *                       # PyQt6 Library (GUI)
from PyQt6.QtCore import *                          # PyQt6 Library (GUI)
from pyqtgraph import PlotWidget, plot              # pip install pyqt6, pip install pyqtgraph
from inputs.randomInputGen import randomInputGen    # Imports randomInputGen Class from inputs/randomInputGen.py

simulate = True;

randomInputGen()


# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibration GUI")
        # Window Size === Screen Size
        self.setFixedSize(QSize(1024, 600))
        
        # Applies Grid Layout to Window
        layout = QGridLayout()
        
        # Temp Function to Create Space for Event Log Menu
        def create_log(label):
            widget = QLabel(label)
            widget.setFrameShape(QFrame.Shape.Box)
            widget.setFrameShadow(QFrame.Shadow.Plain)
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return widget
        
        # Temp Function to Create Space for Status Widget
        def create_status(label):
            widget = QLabel(label)
            widget.setFrameShape(QFrame.Shape.Box)
            widget.setFrameShadow(QFrame.Shadow.Plain)
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return widget
        
        # Function to Create Clock Widget: Returns Current System Time
        def create_clock(label):
            widget = QLabel(label)                              # Using A Label (Text) To Display Time
            widget.setFrameShape(QFrame.Shape.Box)              # Creates Box Around Widget
            widget.setFrameShadow(QFrame.Shadow.Plain)          # Removes Shadow From Box
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)   # Aligns Text To Center
            
            # Want this to be in standard Time 
            widget.setText(time.strftime("%H:%M:%S"))
            return widget
        
        # Function to Create Graph Widget: Returns a Graph of Data Input
        def create_graph(data):
            widget = PlotWidget()
            widget.setLabel('left', 'PPM', units='PPM')
            widget.setLabel('bottom', 'Time', units='s')
            widget.showGrid(x=True, y=True)
            widget.setBackground('w')
            
            # array of time (s) of same length as data
            s = np.linspace(0, 100, len(data))
            
            widget.plot(s, data)        
            return widget
        

        data = open("data.txt", "r")
        dataARR = []
        for line in data.readlines():
            dataARR.append(float(line))
            
        layout.addWidget(create_log("Event Log"), 0, 0)
        layout.addWidget(create_status("Status"), 0, 3)
        layout.addWidget(create_graph(dataARR), 1, 1, 3, 3)
        layout.addWidget(create_clock("Clock"), 3, 0)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

app = QApplication([])

# Window Setup 
window = MainWindow()
window.show()

# Starts Event Loop
app.exec()

