import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import pyqtgraph as pg
# import smbus
import time
from datetime import datetime


class MakeGraph(QWidget):
    graphBackground = "#232629"
    graphLine = "#063e78"
    borders = "#3b4045"
   
    eventTime = []  # Event Time Points
    eventData = []  # Event Data Points
    timeNow = datetime.now()
    counter = 0
   
    dateForLog = timeNow.strftime("%m-%d-%Y")
    timeForLog = 0
    maxPPMForLog = 0
    warningsForLog = 'No Warnings'
    ppmValuesForLog = []
    leakTimeStamp = 0
   

   
    def __init__(self, parent=None):
        super(MakeGraph, self).__init__(parent)
        self.eventTimeValue = None
        self.showLive = True
        self.finished = False
        self.disposal = False
        self.leak = False
        self.abort = False
        self.eventDataValues = {}
        self.eventDateValue = None
       
        # False: Running On PI With Sensor
        # True: Running On Computer Without Sensor
        self.simulation = True
       
       
        self.data = []
        self.simulatedData = [1.27, 1.278, 1.363, 1.363, 1.449, 1.518, 1.627, 1.694, 1.731, 1.864, 2.053, 2.053, 2.21, 2.292, 2.292, 2.434, 2.629, 2.802, 2.802, 2.932, 3.054, 3.054, 3.215, 3.347, 3.347, 3.582, 3.702, 3.915, 3.915, 4.343, 4.692, 4.692, 5.435, 6.163, 6.163, 6.61, 6.89, 7.049, 7.049, 7.414, 7.874, 7.874, 8.65, 4.877, 4.877, 2.508, 1.795, 1.482, 1.482, 1.412, 1.244, 1.244, 1.202, 1.038, 1.173, 1.173, 1.096, 1.096, 1.109]
        self.time = []
        self.counter = 0
       
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
        self.graphWidget.getPlotItem().layout.setContentsMargins(0, 0, 0, 25)  # Left, Top, Right, Bottom margins

        self.graphWidget.setBackground(self.graphBackground)
        self.graphWidget.setFixedWidth(1024)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle('<span style="font-size: 32pt">Concentration In PPM</span>', color='w')
        self.data_line = self.graphWidget.plot(self.data, self.time, pen=pg.mkPen(self.graphLine, width=8))
       
        # Increase the font size for axis labels
        axisFont = QFont()
        axisFont.setPixelSize(24)  # Set the desired font size
        self.graphWidget.getPlotItem().getAxis('left').setTickFont(axisFont)
        self.graphWidget.getPlotItem().getAxis('bottom').setTickFont(axisFont)
       
        self.graphWidget.setLabel('left', 'PPM', **{'font-size': '32pt'} , **{'color': '#ffffff'})
        self.graphWidget.setLabel('bottom', 'Time (s)', **{'font-size': '32pt'},  **{'color': '#ffffff'})
        layout.addWidget(self.graphFrame)  # Add the graphFrame to the main layout
           
    def showStandByGraph(self):
        print("Standby mode activated")
       
       
    def validate_checksum(self, data_bytes, received_checksum):
        # Calculate the 256-modulo (8-bit) sum of the data bytes
        data_sum = sum(data_bytes) % 256
        # Calculate the checksum: 0x01 + ~(sum)
        calculated_checksum = (0x01 + (~data_sum & 0xFF)) & 0xFF
        # Check if the checksum + sum equals 0x00
        return (calculated_checksum + data_sum) & 0xFF == 0x00
       
    def read_sensor_data(self, bus, sensor_address):

        data_bytes = bus.read_block_data(sensor_address, 3)
   
        # Used For Checksum
        crc = data_bytes[0]
   
        # Extract calibrated sensor data (Big-Endian format)
        calibrated_data_msb = data_bytes[1]
        calibrated_data_lsb = data_bytes[2]
        calibrated_sensor_value = (calibrated_data_msb << 8) | calibrated_data_lsb


        # Validate the data using the checksum
        if self.validate_checksum(data_bytes[1:], crc):
            return calibrated_sensor_value
        else:
            print("Checksum mismatch")
            return None
           
    # def handleSensorRead(self, bus, sensor_address):  
    #     sensor_value = self.read_sensor_data(bus, sensor_address) # Real
    #     if sensor_value is not None:
    #         self.data.append(sensor_value)
    #         self.time.append(self.counter)
    #         self.counter += 1
    #         self.plotSensorData()
           
    def simulateSensorData(self):
        simulated_value = self.simulatedData[self.counter]
        self.data.append(simulated_value)
        self.time.append(self.counter)
        self.counter += 1
        self.plotSensorData()
           
   
    def handleStart(self):
        self.sensorTimer = QTimer(self)
        if not self.simulation:
            self.sensorTimer = QTimer(self)
            # Initialize I2C (SMbus)
            #bus = smbus.SMBus(1)
   
            # Sensor I2C Address
            sensor_address = 0x50
            #self.sensorTimer.timeout.connect(lambda: self.handleSensorRead(bus, sensor_address))
        else:
            self.sensorTimer.timeout.connect(self.simulateSensorData)

        self.sensorTimer.start(1000)
       
    def handleAbort(self):
        print("Abort button pressed")
        self.abort = True
        self.showLive = False
        self.sensorTimer.stop()
        self.graphWidget.clear()
        self.counter = 0
         

           
    def handleDisposalClick(self):
        print("Disposal button pressed")
        self.disposal = True
        self.showLiveGraph()    
       
   
    def tempDisposal(self):
        print("creating disposal graph")
           
        if self.disposal:
            print("Disposal mode activated")
            lastPPM = self.data[self.counter - 1]
            for i in range(self.counter+1, self.counter + 20):
                self.time[i] = i
                self.data[i] = lastPPM - (i - self.counter)
                if self.data[i] < 0:
                    self.data[i] = 0
                    self.timer.stop()
                   
            self.timer.start(1000)
           
           
    def plotSensorData(self):
        self.data_line.setData(self.time, self.data)
       
       
    def handleEventClicked(self):
        print("Event button pressed")
        self.showLive = False
        self.sensorTimer.stop()
           
        self.graphWidget.clear()
        self.counter = 0
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
            print(f"{self.eventDateValue} Data Plotting...")
            self.data_line.setData(self.eventTime, self.eventData)

           


    def writeToLog(self, date, time, maxPPM, warnings, warningStamp, ppmValues):
        with open(f'logs/eventCount.txt', 'r') as file:
            count = int(file.read())
            count += 1
            with open(f'logs/eventCount.txt', 'w') as file:
                file.write(str(count))
       
        with open(f'logs/events.txt', 'a') as file:
            file.write(f"\n{date}\n{time}\n{maxPPM}\n{warnings}\n{ppmValues}\n")