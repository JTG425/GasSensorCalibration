import os, sys
import psutil
import logging
import time
import random
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea, QFrame, QScroller, QGridLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QColor, QPalette, QScreen
from datetime import datetime
from eventLog import EventLog
from graph import MakeGraph

# Color Palette
# --primary: #063e78; GraphLine, EventLogBackgroud
# --primary-content: #84bdf9; Text Color
# --primary-dark: #042547; For Gradients
# --primary-light: #0857a9; For Gradients

# --background: #18191b; Window Background
# --foreground: #232629; Graph Background
# --border: #3b4045; Borders

# --copy: #fbfbfb; Text Color (Main Window Above Background, EX: Clock)
# --copy-light: #d6d9dc; Text Color (Light)
# --copy-lighter: #9fa6ac;  Text Color (Lighter)

# --standby: #067806;
# --inProgress: #787806;
# --abort: #780606;
# --standby-text: #84f984;
# --warning-text: #f9f984;
# --error-text: #f98484;

windowBackground = "#18191b"
screensaver1 = 'rgba(28,30,35,0.9)'
screensaver2 = 'rgba(57,75,116,0.9)'
screensaver3 = 'rgba(58,102,201,0.9)'


buttonColor = "#0857a9"
m_s_buttonText = "#ffffff"
warningText = "#ffffff"
standbyText = "#ffffff"
errorText = "#ffffff"
abortButtonColor = "#a30309"
graphBackground = "#232629"
graphLine = "#063e78"
borders = "#3b4045"
eventLogBackground = "#063e78"
standbyColor = "#067806"
inProgressColor = "#787806"
warningColor = "#780606"
        



class HMIWindow(QWidget):
    sideBarShown = False;
    

    
    
    def __init__(self):
        super().__init__()
        self.eventID = None
        self.toggleSaver = QTimer(self)
        self.toggleSaver.timeout.connect(self.toggleScreenSaver)
        self.toggleSaver.start(1000)  # Start the timer with 1-second intervals
        self.saverCounter = 0
        self.graph = MakeGraph(self)
        self.sidebar = EventLog(self)
        self.sidebar.eventData.connect(self.graph.handleEventData)
        self.sidebar.eventData.connect(self.onEventSelected)
        self.initializeUI()


    def initializeUI(self):
        self.isEventSelected = False
        self.operation = "standby"

        # Sets the Window dimensions and Styling
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.showFullScreen()
        self.setStyleSheet(
            f"background-color: {windowBackground};"
            "padding: 10px;"
        )
        gridLayout = QGridLayout(self)  # Initialize a QGridLayout
        gridLayout.setContentsMargins(10, 10, 10, 10)


        # Creates a Screesaver like effect THat will snow the Time and when
        # anywhere on screen is clicked, the main screen shows.
        time = datetime.now()
        self.timer = QTimer(self)  # QTimer to update the time
        self.timer.timeout.connect(self.updateScreenSaverTime)
        self.timer.start(1000)
          
        regular_time = ""
        if time.hour % 12 > 10:
            regular_time = time.strftime("%I:%M %p")
        else:
            regular_time = time.strftime("%-I:%M %p")
            
        self.screensaver = QPushButton(regular_time, self)
        self.screensaver.setFixedSize(self.screen.width(), self.screen.height())
        self.screensaver.setStyleSheet(f"""
            background: qlineargradient(
                x1: 0, y1: 9,
                x2: 0.5, y2: 0.5,
                x3: 1,  y3: 0.1,
                stop: 0 {screensaver1}, 
                stop: 1 {screensaver2}, 
                stop: 2 {screensaver3}); 
            border: none;
            color: white;
            font-size: 200px;
        """)
        self.screensaver.move(QPoint(0,0))
        self.screensaver.show()
        self.screensaver.clicked.connect(self.handleScreensaver)
        
        self.sidebar.move(QPoint(-10,-10))
        self.sidebar.hide()

        
        # Call CreateElements Function
        self.createElements(gridLayout)

        self.setStyles()
        self.setLayout(gridLayout)
        self.screensaver.raise_()
        
    def createElements(self, gridLayout):
        # Create A Power Button that can be used to turn off the device (Kill The Python Script)
        self.powerButton = QPushButton("⏻", self)
        self.powerButton.setFixedSize(75, 75)
        self.powerButton.clicked.connect(self.onPowerButtonClick)
        self.powerButton.setStyleSheet(
            f"background: {abortButtonColor};"
            "color: white;"
            "font-size: 20px;"
            "border: 1px solid #3b4045;"
            "border-radius: 5px;"
        )
        self.powerButton.move(QPoint(-self.sidebar.width(),10))
        
        self.powerOptions = QFrame(self)
        self.powerOptions.setFixedSize(600, 500)
        width = int(self.screen.width() / 2)
        height = int(self.screen.height() / 2)
        self.powerOptions.move(QPoint(width-300, height - 250))
        self.powerOptions.setStyleSheet(
            f"background-color: white;"
            "border: 1px solid #3b4045;"
            "border-radius: 5px;"
        )
        self.powerOptions.hide()
        
        self.powerBackground = QFrame(self)
        self.powerBackground.setFixedSize(self.screen.width(), self.screen.height())
        self.powerBackground.move(QPoint(0,0))
        self.powerBackground.setStyleSheet(
            "background: rgba(0,0,0,0.75);"
        )
        self.powerBackground.hide()
        
        
        self.powerOptions.setLayout(QVBoxLayout())
        self.powerOptions.layout().setContentsMargins(10, 10, 10, 10)
        
        self.cancelButton = QPushButton("Close Power Menu", self.powerOptions)
        self.cancelButton.setFixedSize(550, 100)
        self.cancelButton.clicked.connect(self.handlePowerCancel)
        
        self.sleepButton = QPushButton("Sleep", self.powerOptions)
        self.sleepButton.setFixedSize(550, 100)
        self.sleepButton.clicked.connect(self.handlePowerSleep)
        
        self.shutDownButton = QPushButton("Shut Down", self.powerOptions)
        self.shutDownButton.setFixedSize(550, 100)
        self.shutDownButton.clicked.connect(self.handleShutDown)
        

        
        self.powerOptions.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.powerOptions.layout().addWidget(self.cancelButton)
        self.powerOptions.layout().addWidget(self.sleepButton)        
        self.powerOptions.layout().addWidget(self.shutDownButton)

        

        # Event Log button at row 0, column 0, spanning 2x2
        self.eventButton = QPushButton("☰")
        self.eventButton.setFixedSize(75, 100)
        self.eventButton.clicked.connect(self.toggleEventLog)
        gridLayout.addWidget(self.eventButton, 0, 0, 1, 1)
        
        # Abort at row 0, column 1, spanning 2x4
        self.abortButton = QPushButton("Abort")
        self.abortButton.setFixedSize(125, 100)
        self.abortButton.clicked.connect(self.toggleAbort)
        self.abortButton.setDisabled(True)
        gridLayout.addWidget(self.abortButton, 0, 1, 1, 1)
        
        # Dispose at row 0, column 6
        self.disposeButton = QPushButton("Dispose")
        self.disposeButton.setFixedSize(500, 100)
        self.disposeButton.clicked.connect(self.toggleDisposal)     
        gridLayout.addWidget(self.disposeButton, 0, 6, 1, 1)
        

        # Start button at row 0, column 7
        self.startButton = QPushButton("Start")
        self.startButton.setFixedSize(500, 100)
        self.startButton.clicked.connect(self.onStartButtonClick)
        gridLayout.addWidget(self.startButton, 0, 7, 1, 1)
        
        # Status Label at row 1, column 0 to 5
        self.statusLabel = QLabel("Status: Standby")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gridLayout.addWidget(self.statusLabel, 1, 0, 1, 8)

        
        # Graph at row 2 and column 0 to 5
        # Graph Defined in graph.py
        gridLayout.addWidget(self.graph, 2, 0, 6, 8)      
        
    def setStyles(self):
        # styles
        self.eventButton.setStyleSheet(
            f"color: {m_s_buttonText};" 
            f"background-color: {buttonColor};" 
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"  
            f"border-radius: 5px;"
        )
        self.abortButton.setStyleSheet(
            f"color: white;"
            f"background-color: {abortButtonColor};" 
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"  
            "border-radius: 5px;"
        )
        self.startButton.setStyleSheet(
            f"color: {m_s_buttonText};" 
            f"background-color: {buttonColor};" 
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"  
            "border-radius: 5px;"
        )
        self.disposeButton.setStyleSheet(
            f"color: {m_s_buttonText};" 
            f"background-color: {buttonColor};" 
            f"border: 1px solid {borders};" 
            "font-size: 24px;"
            "padding: 10px;" 
            "border-radius: 5px;"
        )
        self.statusLabel.setStyleSheet(
            f"font-size: 40px;" 
            f"border: 1px solid {borders};" 
            f"border-radius: 5px;" 
            f"background-color: {standbyColor};"
            "padding: 10px;" 
            "color: {standbyText};"
        )
        self.cancelButton.setStyleSheet(
            f"color: {m_s_buttonText};"
            f"background-color: {buttonColor};"
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"
            "border-radius: 5px;"
        )
        
        self.sleepButton.setStyleSheet(
            f"color: {m_s_buttonText};"
            f"background-color: {buttonColor};"
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"
            "border-radius: 5px;"
        )
        self.shutDownButton.setStyleSheet(
            f"color: white;"
            f"background-color: {abortButtonColor};"
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"
            "border-radius: 5px;"
        )
        
        self.powerOptions.setStyleSheet(
            f"background-color: {windowBackground};"
            f"border: 1px solid {borders};"
            "border-radius: 5px;"
        )
        
    # After 300 seconds of inactivity (5 Minutes), the screen saver will show
    def toggleScreenSaver(self):
        self.saverCounter = self.saverCounter + 1;
        if(self.saverCounter >= 300):
            self.screensaver.show()
            self.toggleSaver.stop()
        
    def handleScreensaver(self):
        # When Screen is clicked, the main screen shows
        self.screensaver.hide()
        self.eventButton.setDisabled(False)
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
            
        
        
    

    def updateScreenSaverTime(self):
        # Update the time on the screen saver
        time = datetime.now()
        regular_time = ""
        if time.hour % 12 > 10:
            regular_time = time.strftime("%I:%M %p")
        else:
            regular_time = time.strftime("%-I:%M %p")
        self.screensaver.setText(regular_time)
     
        
    def handleStatusChange(self, status):
        self.statusLabel.setText(f"Status: {status}")
        if status == "Standby":
            self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {standbyColor};"
                "padding: 10px;" 
                "color: {standbyText};"
            )
        elif status == "In Progress":
            self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {inProgressColor};"
                "padding: 10px;" 
                "color: white;"
            )
        elif status == "Calibration Complete, Open Disposal Valve":
             self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {inProgressColor};"
                "padding: 10px;" 
                "color: white;"
            )           
        elif status == "Aborting Calibration":
            self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {warningColor};"
                "padding: 10px;" 
                f"color: {warningText};"
            )           
        elif status == "Showing Previous Event":
             self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {standbyColor};"
                "padding: 10px;" 
                "color: {standbyText};"
            )
        elif status == "Disposal Complete":
            self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {standbyColor};"
                "padding: 10px;" 
                "color: {standbyText};"
            )
            self.statusLabel.setText(f"Status: Standby")
            
        elif status == "Disposal In Progress":
            self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {inProgressColor};"
                "padding: 10px;" 
                "color: white;"
            )
            self.statusLabel.setText(f"Status: Disposal In Progress")
                       
        else:
            self.statusLabel.setStyleSheet(
                f"font-size: 40px;" 
                f"border: 1px solid {borders};" 
                f"border-radius: 5px;" 
                f"background-color: {standbyColor};"
                "padding: 10px;" 
                "color: {standbyText};"
            )
        
    def toggleAbort(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        # Abort button click handler
        print("Abort Clicked")
        self.handleStatusChange("Aborting Calibration")
        self.graph.handleAbort()
        
        QTimer.singleShot(5000, self.postAbortActions)  # 5000 ms = 5 seconds

    def postAbortActions(self):
        # Actions to be taken after the delay
        self.handleStatusChange("Standby")
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
        
          
    def toggleDisposal(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        # Disposal button click handler
        self.handleStatusChange("Disposal In Progress")
        
        # Call Disposal Handler In Graph
        self.graph.handleDisposalClick()
        
        self.disposalDoneCounter = 0
        
        self.simulateDisposalDone = QTimer(self)
        self.simulateDisposalDone.timeout.connect(self.handleDisposalDone)
        self.simulateDisposalDone.start(1000)
        
        # After Disposal is done
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
    def handleDisposalDone(self):
        if self.disposalDoneCounter == 20:
            self.handleStatusChange("Standby")
            self.simulateDisposalDone.stop()
        self.disposalDoneCounter = self.disposalDoneCounter + 1


    def toggleEventLog(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        # Event button click handler
        self.sideBarShown = not self.sideBarShown
        
        # Toggle The Button Text
        if self.sideBarShown:
            self.eventButton.setText("X")
            self.sidebar.show()
            self.powerButton.show()
            self.sidebar.raise_()
            self.powerButton.move(QPoint(self.sidebar.width()-120,10))
            self.powerButton.raise_()
            self.eventButton.raise_()  # Ensure the event button is always on top
        else:
            self.eventButton.setText("☰")
            self.sidebar.hide()
            self.powerButton.hide()
        self.powerButton.raise_()
        self.eventButton.raise_()

  


    def onStartButtonClick(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        
        # Start button click handler
        print("Start button clicked!")
        self.handleStatusChange("In Progress")
        self.abortButton.setDisabled(False)
        self.graph.handleStart()
        
        self.simulationCounter = 0
        self.simulationTimer = QTimer(self)
        self.simulationTimer.timeout.connect(self.simulateDisposalTrigger)
        self.simulationTimer.start(1000)
        
        # After Graphing is done
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
    def simulateDisposalTrigger(self):
        if self.simulationCounter == 50:
            self.handleStatusChange("Calibration Complete, Open Disposal Valve")
            self.disposeButton.setDisabled(False)
            self.simulationCounter = 0
            self.simulationTimer.stop()     
        self.simulationCounter = self.simulationCounter + 1
        
     
    # Handler for when a previous Event is Clicked   
    def onEventSelected(self, eventId):
        self.saverCounter = 0
        self.toggleSaver.stop()
        
        # Call the method on MakeGraph to show the event log graph
        self.toggleEventLog()                                           # Close the event log sidebar
        self.handleStatusChange("Showing Previous Event")               # Change the status label                              # Show the event log graph
        
        # Make The Abort Button UnClickable
        self.abortButton.setDisabled(True)
        
        # After Graphing is done
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
    
      
    # Working :)  
    def onPowerButtonClick(self):
        # Power button click handler
        print("Power button clicked!")
        # sys.exit()
        self.toggleEventLog()
        self.powerBackground.show()
        self.powerOptions.show()
        self.powerBackground.raise_()
        self.powerOptions.raise_()
        
        
    # Working :)
    def handlePowerCancel(self):
        print("Power Options Hidden")
        self.powerBackground.hide()
        self.powerOptions.hide()
        
    # Working :)
    def handlePowerSleep(self):
        print("Sleeping")
        self.powerBackground.hide()
        self.powerOptions.hide()
        self.eventButton.setDisabled(True)
        self.screensaver.show()
    
    # Working :)
    def handleShutDown(self):
        print("Shutting Down")
        self.powerBackground.hide()
        self.powerOptions.hide()
        sys.exit()
        
        

def main():
    app = QApplication(sys.argv)
    window = HMIWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
