import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import pyqtgraph as pg
import time

class MakeGraph(QWidget):
    graphBackground = "#232629"
    graphLine = "#063e78"
    borders = "#3b4045"
    
    time = {}  # Time points
    data = {}  # Data points
    eventTime = {}  # Event Time Points
    eventData = {}  # Event Data Points
    sensor_address = 0x50

    
    def __init__(self, parent=None):
        super(MakeGraph, self).__init__(parent)
        self.eventTimeValue = None
        self.showLive = True
        self.disposal = False
        self.eventDataValues = {}
        self.eventDateValue = None
        
        self.timer = QTimer(self)  # QTimer to update the graph
        self.timer.timeout.connect(self.updateLiveGraph)
        
        self.counter = 0
        self.eventCounter = 0
        self.operation = "standby"
        self.initUI()

        
    def initUI(self):
        layout = QVBoxLayout(self) 
        self.graphFrame = QFrame()
        self.graphFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.graphFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.graphFrame.setStyleSheet(
            f"background-color: {self.graphBackground};"
            f"border: 1px solid {self.borders};"
            "padding: 10px;"
        )
    
        # Create a layout for the graphFrame
        self.graphFrameLayout = QVBoxLayout(self.graphFrame)  
        self.graphFrame.setLayout(self.graphFrameLayout)

        self.graphWidget = pg.PlotWidget()
        self.graphFrameLayout.addWidget(self.graphWidget)  # Add the graphWidget to the graphFrame's layout
        self.graphFrameLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the graphWidget to the center

        self.graphWidget.setBackground(self.graphBackground)
        self.graphWidget.setFixedWidth(1024)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle('<span style="font-size: 24pt">Concentration In PPM</span>', color='w')
        
        # Increase the font size for axis labels
        axisFont = QFont()
        axisFont.setPixelSize(24)  # Set the desired font size
        self.graphWidget.getPlotItem().getAxis('left').setTickFont(axisFont)
        self.graphWidget.getPlotItem().getAxis('bottom').setTickFont(axisFont)
        self.graphWidget.setLabel('left', 'PPM', **{'font-size': '24pt'},  **{'color': 'w'})
        self.graphWidget.setLabel('bottom', 'Time (s)', **{'font-size': '24pt'},  **{'color': 'w'})

        self.graphWidget.getPlotItem().layout.setContentsMargins(0, 0, 0, 25)  # Left, Top, Right, Bottom margins
        
        
        layout.addWidget(self.graphFrame)  # Add the graphFrame to the main layout
            
    def showStandByGraph(self):
        print("Standby mode activated")
        
    def handleAbort(self):
        print("Abort button pressed")
        self.showLive = False
        self.timer.stop()
        self.graphWidget.clear()
        self.counter = 0
         
        
    # This Function Will Be where the sensor Input will be processed.
    # For now, it will be a temporary function to test the graph.
    # It should also Write the data to a file for future Event Log Use.
    def tempLiveData(self):
        self.graphWidget.clear()
        self.counter = 0
        self.showLive = True
        for i in range(1, 100):
            self.time[i] = i
            self.data[i] = i^2
        with open('logs/events.txt', 'a') as file:
            for key in self.time.keys():
                file.write(f"{key},{self.data[key]} ")
        
        
        self.showLiveGraph()
        
        
        
    # This Function Will Recieve Data from the sensor and update the graph
    # def recieveSensorData(self, time, data):
    #     self.graphWidget.clear()


        
            
    def showLiveGraph(self):
        if self.showLive and self.disposal == False:
            # sensor_value = data[0] << 8 | data[1]
            # self.data[self.counter] = sensor_value
            # self.time[self.counter] = self.counter
            self.timer.start(1000)  # Start the timer with 1-second intervals
            # self.updateLiveGraph()
            print("Live graph shown")
            self.counter += 1
        elif self.disposal == True:
            print("calling Disposal")
            self.timer.stop()
            self.tempDisposal()
        else:
            self.timer.stop()
            
    def handleDisposalClick(self):
        print("Disposal button pressed")
        self.disposal = True
        self.showLiveGraph()    
        
    
    def tempDisposal(self):
        print("creating disposal graph")
        if self.disposal:
            print("Disposal mode activated")
            lastPPM = self.data[self.counter - 1]
            for i in range(self.counter+1, self.counter + 100):
                self.time[i] = i
                self.data[i] = lastPPM - (i - self.counter)
                if self.data[i] < 0:
                    self.data[i] = 0
                    
            self.timer.start(1000)
        
        
    def updateLiveGraph(self):
        if self.showLive:
            if self.counter < len(self.time):
                time_keys = list(self.time.keys())[:self.counter + 1]
                data_values = [self.data[key] for key in time_keys]
                self.graphWidget.plot(time_keys, data_values, pen=pg.mkPen(self.graphLine, width=8))
                self.counter += 1
            else:
                self.timer.stop()
        else:
            return
        
    def handleEventClicked(self):
        print("Event button pressed")
        self.showLive = False
        self.timer.stop()
            
        self.graphWidget.clear()
        self.counter = 0
        self.eventCounter = 0
        self.eventTimer = QTimer(self)
        self.eventTimer.timeout.connect(self.updateEventGraph)
        self.showEventLog()

    def setEventTime(self, time):
        self.eventTimeValue = time

    def setEventData(self, data):
        self.eventDataValues = data
    
    def setEventDate(self, date):
        self.eventDateValue = date

    def showEventLog(self):
        self.graphWidget.setTitle(f'<span style="font-size: 24pt">Calibration Performed on {self.eventDateValue}</span>', color='w')
        
        if self.eventTimeValue is None or self.eventDataValues == [] or self.eventDateValue is None:
            print("No data to show")
        else:
            for i in range(self.eventTimeValue):
                self.eventTime[i] = i
                self.eventData[i] = self.eventDataValues[i]   
            print(self.eventData)
            self.eventTimer.start(100)  # Update The Plot every 100ms
            print(f"{self.eventDateValue} Data Plotting...")
            
    def updateEventGraph(self):
        if self.eventCounter < len(self.eventTime):
            time_keys2 = list(self.eventTime.keys())[:self.eventCounter + 1]
            data_values2 = [self.eventData[key] for key in time_keys2]
            self.graphWidget.plot(time_keys2, data_values2, pen=pg.mkPen(self.graphLine, width=8))
            self.eventCounter += 1
        else:
            self.eventTimer.stop()  # Stop the timer after all points are plotted

