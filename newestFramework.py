import sys
import time
import random
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
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
m_s_buttonText = "#84bdf9"
warningText = "#f9f984"
standbyText = "#84f984"
errorText = "#f98484"
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
        self.saverCounter = 0;
        self.initializeUI()


    def initializeUI(self):
        self.isEventSelected = False
        self.operation = "standby"

        # Sets the Window dimensions and Styling
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        #self.showFullScreen()
        self.setStyleSheet(
            f"background-color: {windowBackground};"
            "padding: 10px;"
        )
        gridLayout = QGridLayout(self)  # Initialize a QGridLayout
        gridLayout.setContentsMargins(10, 50, 10, 10)
        self.sidebar = EventLog(self)

        # Creates a Screesaver like effect THat will snow the Time and when
        # anywhere on screen is clicked, the main screen shows.
        time = datetime.now()
        self.timer = QTimer(self)  # QTimer to update the time
        self.timer.timeout.connect(self.updateScreenSaverTime)
        self.timer.start(1000)  # Start the timer with 1-second intervals
          
        regular_time = ""
        if time.hour % 12 > 10:
            regular_time = time.strftime("%I:%M %p")
        else:
            regular_time = time.strftime("%-I:%M %p")
            
        self.screensaver = QPushButton(regular_time, self)
        self.screensaver.setFixedSize(screen.width(), screen.height())
        self.screensaver.setStyleSheet(f"""
            background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0.5, y2: 0.5,
                x3: 1,  y3: 0.1,
                stop: 0 {screensaver1}, 
                stop: 1 {screensaver2}, 
                stop: 2 {screensaver3}); 
            border: none;
            color: white;
            font-size: 200px;
        """)
        
        self.screensaver.clicked.connect(self.handleScreensaver)
        
        self.sidebar.move(QPoint(-self.sidebar.width(), 0))
        self.graph = MakeGraph(self)
        
        # Signal Connections
        self.sidebar.eventTime.connect(self.graph.setEventTime)
        self.sidebar.eventData.connect(self.graph.setEventData)
        self.sidebar.eventDate.connect(self.graph.setEventDate)
        self.sidebar.eventSelected.connect(self.onEventSelected)
        
        # Call CreateElements Function
        self.createElements(gridLayout)

        self.setStyles()
        self.screensaver.raise_()
        self.setLayout(gridLayout)
        
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
        self.powerButton.move(QPoint(-self.sidebar.width(),46))
    
        

        # Event Log button at row 0, column 0, spanning 2x2
        self.eventButton = QPushButton("☰")
        self.eventButton.setFixedSize(75, 100)
        self.eventButton.clicked.connect(self.toggleEventLog)
        gridLayout.addWidget(self.eventButton, 0, 0, 1, 1)
        
        # Abort at row 0, column 1, spanning 2x4
        self.abortButton = QPushButton("Abort")
        self.abortButton.setFixedSize(125, 100)
        self.abortButton.clicked.connect(self.toggleAbort)
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
            f"color: {m_s_buttonText};" 
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"  
            f"border-radius: 5px;"
        )
        self.abortButton.setStyleSheet(
            f"color: {m_s_buttonText};" 
            f"background-color: {abortButtonColor};" 
            f"color: {m_s_buttonText};" 
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"  
            "border-radius: 5px;"
        )
        self.startButton.setStyleSheet(
            f"color: {m_s_buttonText};" 
            f"background-color: {buttonColor};" 
            f"color: {m_s_buttonText};" 
            f"border: 1px solid {borders};"
            "font-size: 24px;"
            "padding: 10px;"  
            "border-radius: 5px;"
        )
        self.disposeButton.setStyleSheet(
            f"color: {m_s_buttonText};" 
            f"background-color: {buttonColor};" 
            f"color: {m_s_buttonText};" 
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
        
    # After 300 seconds of inactivity (5 Minutes), the screen saver will show
    def toggleScreenSaver(self):
        self.saverCounter = self.saverCounter + 1;
        print(self.saverCounter)
        if(self.saverCounter >= 300):
            self.screensaver.show()
            self.toggleSaver.stop()
        
    def handleScreensaver(self):
        # When Screen is clicked, the main screen shows
        self.screensaver.hide()
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
        elif status == "Disposal In Progress":
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
        
        # After Aborting Is Done
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
        
          
    def toggleDisposal(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        # Disposal button click handler
        print("Disposal Clicked")
        self.handleStatusChange("Disposal In Progress")
        
        # After Disposal is done
        self.saverCounter = 0
        self.toggleSaver.start(1000)


    def toggleEventLog(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        # Event button click handler
        self.sideBarShown = not self.sideBarShown
        
        # Toggle The Button Text
        if self.sideBarShown:
            self.eventButton.setText("X")
        else:
            self.eventButton.setText("☰")
            
        # Animation for Power Button
        self.powerAnimation = QPropertyAnimation(self.powerButton, b"pos")
        self.powerAnimation.setDuration(500)  # Animation duration in milliseconds
        
        if self.sideBarShown:  # If sidebar is off-screen, slide it into view
            self.powerAnimation.setEndValue(QPoint(self.sidebar.width()-120,46))
        else:  # If sidebar is in view, slide it out of view
            self.powerAnimation.setEndValue(QPoint(-self.sidebar.width(), 46))
            
        self.powerAnimation.start()
            
        # Animation for sidebar
        self.animation = QPropertyAnimation(self.sidebar, b"pos")
        self.animation.setDuration(500)  # Animation duration in milliseconds

        if self.sideBarShown:  # If sidebar is off-screen, slide it into view
            self.animation.setEndValue(QPoint(-10,0))
        else:  # If sidebar is in view, slide it out of view
            self.animation.setEndValue(QPoint(-self.sidebar.width(), 0))
        
        self.animation.start()
        self.sidebar.raise_()
        self.powerButton.raise_()
        self.eventButton.raise_()  # Ensure the event button is always on top
  
        


    def onStartButtonClick(self):
        self.saverCounter = 0
        self.toggleSaver.stop()
        
        # Start button click handler
        print("Start button clicked!")
        self.handleStatusChange("In Progress")
        self.graph.tempLiveData()
        
        # After Graphing is done
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
        
    def onEventSelected(self, eventId):
        self.saverCounter = 0
        self.toggleSaver.stop()
        # Call the method on MakeGraph to show the event log graph
        self.toggleEventLog()
        self.handleStatusChange("Showing Previous Event")
        self.graph.showEventLog()
        
        # After Graphing is done
        self.saverCounter = 0
        self.toggleSaver.start(1000)
        
    def onPowerButtonClick(self):
        # Power button click handler
        print("Power button clicked!")
        sys.exit()

def main():
    app = QApplication(sys.argv)
    window = HMIWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
