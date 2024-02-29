import sys
import time
from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
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
        self.initializeUI()


    def initializeUI(self):
        self.isEventSelected = False

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        # self.showFullScreen()
        gridLayout = QGridLayout(self)  # Initialize a QGridLayout
        gridLayout.setContentsMargins(10, 50, 10, 10)
        self.sidebar = EventLog(self)
        self.sidebar.move(QPoint(-self.sidebar.width(), 0))
        self.graph = MakeGraph(self)
        self.setStyleSheet(
            f"background: {windowBackground};"
        )
        
        
        # Linear Gradient Setup
        # self.setStyleSheet(
        #     "background-color: qlineargradient("
        #     "x1: 0, y1:0," 
        #     "x2: 1, y2: 1," 
        #     f"stop: 0 {windowBackground1}," 
        #     f"stop: 1 {windowBackground2});"
        #     )
        
        # Signal Connections
        self.sidebar.eventTime.connect(self.graph.setEventTime)
        self.sidebar.eventData.connect(self.graph.setEventData)
        self.sidebar.eventDate.connect(self.graph.setEventDate)
        self.sidebar.eventSelected.connect(self.onEventSelected)
    
        

        # Event Log button at row 0, column 0, spanning 2x2
        self.eventButton = QPushButton("☰")
        self.eventButton.setFixedSize(75, 75)
        self.eventButton.clicked.connect(self.toggleEventLog)
        gridLayout.addWidget(self.eventButton, 0, 0, 1, 1)
        
        # Abort at row 0, column 1, spanning 2x4
        self.abortButton = QPushButton("Abort")
        self.abortButton.setFixedSize(125, 75)
        self.abortButton.clicked.connect(self.toggleAbort)
        gridLayout.addWidget(self.abortButton, 0, 1, 1, 1)
        
        # Dispose at row 0, column 6
        self.disposeButton = QPushButton("Dispose")
        self.disposeButton.setFixedSize(225, 75)
        self.disposeButton.clicked.connect(self.toggleDisposal)     
        gridLayout.addWidget(self.disposeButton, 0, 6, 1, 1)
        

        # Start button at row 0, column 7
        self.startButton = QPushButton("Start")
        self.startButton.setFixedSize(225, 75)
        self.startButton.clicked.connect(self.onStartButtonClick)
        gridLayout.addWidget(self.startButton, 0, 7, 1, 1)
        
        # Status Label at row 1, column 0 to 5
        self.statusLabel = QLabel("Status: Standby")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gridLayout.addWidget(self.statusLabel, 1, 0, 1, 8)
        
        
        # Graph at row 2 and column 0 to 5
        # Graph Defined in graph.py
        gridLayout.addWidget(self.graph, 2, 0, 6, 8)
        
    

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#efeff1'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

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

        self.setLayout(gridLayout)
        
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
        # Abort button click handler
        print("Abort Clicked")
        self.handleStatusChange("Aborting Calibration")
        
        
          
    def toggleDisposal(self):
        # Disposal button click handler
        print("Disposal Clicked")
        self.handleStatusChange("Disposal In Progress")


    def toggleEventLog(self):
        # Event button click handler
        self.sideBarShown = not self.sideBarShown
        
        # Toggle The Button Text
        if self.sideBarShown:
            self.eventButton.setText("X")
        else:
            self.eventButton.setText("☰")
                 
        # Animation for sidebar
        self.animation = QPropertyAnimation(self.sidebar, b"pos")
        self.animation.setDuration(500)  # Animation duration in milliseconds

        if self.sideBarShown:  # If sidebar is off-screen, slide it into view
            self.animation.setEndValue(QPoint(-10,0))
        else:  # If sidebar is in view, slide it out of view
            self.animation.setEndValue(QPoint(-self.sidebar.width(), 0))
        
        self.animation.start()
        self.sidebar.raise_()
        self.eventButton.raise_()  # Ensure the event button is always on top
        


    def onStartButtonClick(self):
        # Start button click handler
        print("Start button clicked!")
        self.handleStatusChange("In Progress")
        self.graph.tempLiveData()
        
        
    def onEventSelected(self, eventId):
        # Call the method on MakeGraph to show the event log graph
        self.toggleEventLog()
        self.handleStatusChange("Showing Previous Event")
        self.graph.showEventLog()

def main():
    app = QApplication(sys.argv)
    window = HMIWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
