import sys
import ast
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import pyqtgraph as pg
from pyqtgraph import TextItem
# import smbus
import time
from datetime import datetime


class MakeGraph(QWidget):
    graphBackground = "#232629"
    graphLine = "#063e78"
    borders = "#3b4045"
   
    eventTime = []  # Event Time Points
    eventData = []  # Event Data Points
    eventDate = ""
    eventMaxPPM = 0
    eventWarnings = ""
    
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
       
        # False: Running On PI With Sensor
        # True: Running On Computer Without Sensor
        self.simulation = True
       
       
        self.data = []
        self.simulatedData = [1.27, 1.278, 1.363, 1.363, 1.449, 1.518, 1.627, 1.694, 1.731, 1.864, 2.053, 2.053, 2.21, 2.292, 2.292, 2.434, 2.629, 2.802, 2.802, 2.932, 3.054, 3.054, 3.215, 3.347, 3.347, 3.582, 3.702, 3.915, 3.915, 4.343, 4.692, 4.692, 5.435, 6.163, 6.163, 6.61, 6.89, 7.049, 7.049, 7.414, 7.874, 7.874, 8.65, 8.71, 8.68, 8.70, 8.71, 8.73, 8.68, 8.69, 8.70, 8.69, 8.68, 8.71, 8.70, 4.877, 4.877, 2.508, 1.795, 1.482, 1.482, 1.412, 1.244, 1.244, 1.202, 1.038, 1.173, 1.173, 1.096, 1.096, 1.109]
        self.time = []
        self.counter = 0
        self.sensorTimer = QTimer(self)
        self.warningText = pg.LabelItem(f"Warnings: {self.eventWarnings}", color='w', size='24pt')
       
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
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle('<span style="font-size: 32pt">Concentration In PPM</span>', color='w')
       
        # Increase the font size for axis labels
        axisFont = QFont()
        axisFont.setPixelSize(24)  # Set the desired font size
        self.graphWidget.getPlotItem().getAxis('left').setTickFont(axisFont)
        self.graphWidget.getPlotItem().getAxis('bottom').setTickFont(axisFont)
       
        self.graphWidget.setLabel('left', 'PPM', **{'font-size': '32pt'} , **{'color': '#ffffff'})
        self.graphWidget.setLabel('bottom', 'Time (s)', **{'font-size': '32pt'},  **{'color': '#ffffff'})
        self.graphWidget.setMouseEnabled(x=False, y=False)
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
        self.ppmValuesForLog.append(simulated_value)
        self.data.append(simulated_value)
        self.time.append(self.counter)
        self.plotSensorData()
           
   
    def handleStart(self):
        self.abort = False
        self.showLive = True
        self.counter = 0
        self.graphWidget.clear()
        self.graphWidget.setTitle(f'<span style="font-size: 24pt">Concentration In PPM</span>', color='w')
        self.data_line = self.graphWidget.plot(self.data, self.time, pen=pg.mkPen(self.graphLine, width=8))
        if self.warningText in self.graphWidget.getPlotItem().listDataItems():
            self.graphWidget.removeItem(self.warningText)
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
        
    
    def plotSensorData(self):
        if self.counter == 50 and not self.disposal:
            self.sensorTimer.stop()
            
        self.data_line.setData(self.time, self.data)
        self.counter += 1
        
        #Add Horzontal Line When counter == 50
        if self.counter == 50:
            self.graphWidget.addLine(x=49, pen=pg.mkPen('g', width=3))
        
        if self.counter == 70:
            self.timeForLog = self.counter
            self.maxPPMForLog = max(self.ppmValuesForLog)
            self.graphWidget.clear()
            self.counter = 0
            self.writeToLog(self.dateForLog, self.timeForLog, self.maxPPMForLog, self.warningsForLog, self.leakTimeStamp, self.ppmValuesForLog)
            
        
    def handleAbort(self):
        self.abort = True
        self.showLive = False
        self.sensorTimer.stop()
        self.graphWidget.clear()
        self.warningsForLog = 'Aborted'
        self.timeForLog = self.counter
        self.maxPPMForLog = max(self.ppmValuesForLog)
        self.counter = 0
        self.writeToLog(self.dateForLog, self.timeForLog, self.maxPPMForLog, self.warningsForLog, self.leakTimeStamp, self.ppmValuesForLog)
        self.resetGraphViewport()
        
    def resetGraphViewport(self):
        self.graphWidget.setXRange(0, 1, padding=0)
        self.graphWidget.setYRange(0, 1, padding=0)
        self.data_line = self.graphWidget.plot(pen=pg.mkPen(self.graphLine, width=8))
         

           
    def handleDisposalClick(self):
        self.disposal = True
        self.sensorTimer.start(1000)      
       
    def handleEventClicked(self):
        print("Event button pressed")

    def handleEventData(self, eventDateValue, eventTimeValue, eventMaxPPMValue, eventWarningsValue, eventDataValue):
        self.eventDate = eventDateValue
        for i in range(eventTimeValue):
            self.eventTime.append(i)
        self.eventData = eventDataValue
        self.eventMaxPPM = eventMaxPPMValue
        self.eventWarnings = eventWarningsValue
        self.sensorTimer.stop()
        self.graphWidget.clear()
        self.showEventLog()
        
    def clearEventData(self):
        self.eventDate = ""
        self.eventTime = []
        self.eventData = []
        self.eventMaxPPM = 0
        self.eventWarnings = ""
        # Delete the previous warning text
        if self.warningText in self.graphWidget.getPlotItem().listDataItems():
            self.graphWidget.removeItem(self.warningText)
        

    def showEventLog(self):
        self.graphWidget.setTitle(f'<span style="font-size: 24pt">Calibration Performed on {self.eventDate}</span>', color='w')
        self.data_line_event = self.graphWidget.plot(self.eventData, self.eventTime, pen=pg.mkPen(self.graphLine, width=8))
        self.data_line_event.setData(self.eventTime, self.eventData)
        self.graphWidget.setLabel('left', 'PPM', **{'font-size': '24pt'}, **{'color': '#ffffff'})
        self.graphWidget.setLabel('bottom', 'Time (s)', **{'font-size': '24pt'},  **{'color': '#ffffff'})
        self.graphWidget.getPlotItem().layout.setContentsMargins(0, 0, 0, 25)
        if self.eventWarnings == 'No Warnings':
            self.graphWidget.addLine(x=49, pen=pg.mkPen('g', width=3))

        self.warningText.setText(f"Warnings: {self.eventWarnings}")
        self.warningText.setParentItem(self.graphWidget.getPlotItem())
        self.warningText.setPos(100, 0)
        

        
            
        
            
            
            
            
        maxPPMText = TextItem(f"Max PPM: {self.eventMaxPPM}", anchor=(0, 1), color='white')


        self.graphWidget.setXRange(min(self.eventTime), max(self.eventTime), padding=0.05)
        self.graphWidget.setYRange(min(self.eventData), max(self.eventData), padding=0.05)
        self.clearEventData()
           


    def writeToLog(self, date, time, maxPPM, warnings, warningStamp, ppmValues):
        with open(f'logs/eventCount.txt', 'r') as file:
            count = int(file.read())
            count += 1
            with open(f'logs/eventCount.txt', 'w') as file:
                file.write(str(count))
       
        with open(f'logs/events.txt', 'a') as file:
            file.write(f"\n{date}\n{time}\n{maxPPM}\n{warnings}\n{ppmValues}\n")