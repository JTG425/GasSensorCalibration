import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QPalette, QShowEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MakeGraph(QWidget):
    graphBackground = "#f9fafc"
    graphLine = "#063e78"
    borders = "#3b4045"
    
    time = {}  # Time points
    data = {}  # Data points
    eventTime = {} # Event Time Points
    eventData = {} # Event Data Points
    
    def __init__(self, parent=None):
        super(MakeGraph, self).__init__(parent)
        self.eventTimeValue = None
        self.showLive = True
        self.eventDataValues = {}
        self.eventDateValue = None
        self.gridLayout = QGridLayout
        self.counter = 0
        self.eventCounter = 0
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.figure.patch.set_facecolor(self.graphBackground)
        self.ax.set_facecolor(self.graphBackground)
        self.ax.set_title('Concentration In PPM')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('PPM')

        self.tempLiveData()
        
    def tempLiveData(self):
        for i in range(1, 100):
            self.time[i] = i
            self.data[i] = 0
        
        self.showLiveGraph()
        

    def showLiveGraph(self):
        self.timer = QTimer(self)  # QTimer to update the graph
        self.timer.timeout.connect(self.updateLiveGraph)
        self.timer.start(1000)  # Start the timer with 1-second intervals
        
        print("Live graph shown")
        
    def updateLiveGraph(self):
        if self.showLive:
            if self.counter < len(self.time):
                time_keys = list(self.time.keys())[:self.counter + 1]
                data_values = [self.data[key] for key in time_keys]
                self.ax.plot(time_keys, data_values, '-o', color=self.graphLine)
                self.canvas.draw()  # Update the canvas with the new plot
                self.counter += 1
            else:
                self.timer.stop()  # Stop the timer if all points are plotted
        else:
            return

            
            

    def setEventTime(self, time):
        self.eventTimeValue = time

    def setEventData(self, data):
        self.eventDataValues = data
    
    def setEventDate(self, date):
        self.eventDateValue = date

    def showEventLog(self):
        self.showLive = False
        self.dataReady = False
        self.timer.stop()
        self.ax.clear()
        self.counter = 0
        self.eventCounter = 0
        self.ax.set_title(f'Calibration Performed On {self.eventDateValue}')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('PPM')
        
        if self.eventTimeValue is None or self.eventDataValues == [] or self.eventDateValue is None:
            print("No data to show")
        else:
            for i in range(self.eventTimeValue):
                self.eventTime[i] = i
                self.eventData[i] = self.eventDataValues[i]   
            print(self.eventData)
            self.dataReady = True
            if self.dataReady:
                self.eventTimer = QTimer(self)  # QTimer to update the graph
                self.eventTimer.timeout.connect(self.updateEventGraph)
                self.eventTimer.start(100)  # Update The Plot every 10
                print(f"{self.eventDateValue} Data Plotting...")
            
    def updateEventGraph(self):
        if self.eventCounter < len(self.eventTime):
            time_keys2 = list(self.eventTime.keys())[:self.eventCounter + 1]
            data_values2 = [self.eventData[key] for key in time_keys2]
            self.ax.plot(time_keys2, data_values2, '-o', color=self.graphLine)
            self.canvas.draw()  # Update the canvas with the new plot                
            self.eventCounter += 1
        else:
            self.timer.stop()  # Stop the timer if all points are plotted
