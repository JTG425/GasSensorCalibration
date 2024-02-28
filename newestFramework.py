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
graphBackground = "#f9fafc"
graphLine = "#063e78"
borders = "#3b4045"
eventLogBackground = "#063e78"
standbyColor = "#067806"
inProgressColor = "#787806"
warningColor = "#780606"
        



class HMIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.eventID = None
        self.initializeUI()


    def initializeUI(self):
        self.isEventSelected = False

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, 1024,600)
        self.showFullScreen()
        gridLayout = QGridLayout(self)  # Initialize a QGridLayout
        self.sidebar = EventLog(self)
        self.sidebar.move(0, 0)
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
    
        

        # Event Log button at row 0, column 0
        self.eventButton = QPushButton("Menu")
        self.eventButton.clicked.connect(self.toggleEventLog)
        gridLayout.addWidget(self.eventButton, 0, 0, 1, 2)
        
        # Abort at row 0, column 1
        self.abortButton = QPushButton("Abort")
        self.abortButton.clicked.connect(self.toggleAbort)

        gridLayout.addWidget(self.abortButton, 0, 2, 1, 2)
        
        # Dispose at row 0, column 2 and 3
        self.disposeButton = QPushButton("Dispose")
        self.disposeButton.clicked.connect(self.toggleDisposal)     
        gridLayout.addWidget(self.disposeButton, 0, 4, 1, 2)
        

        # Start button at row 0, column 4 and 5
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.onStartButtonClick)
        gridLayout.addWidget(self.startButton, 0, 6, 1, 2)
        
        # Status Label at row 1, column 0 to 5
        self.statusLabel = QLabel("Status: Standby")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gridLayout.addWidget(self.statusLabel, 1, 1, 1, 6)
        
        
        # Graph at row 1 and column 0 to 5
        # Graph Defined in graph.py
        gridLayout.addWidget(self.graph, 2, 1, 6, 6)
        
    

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#efeff1'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # styles
        self.eventButton.setStyleSheet(f"height: 100px; width: 100px; color: {m_s_buttonText}; font-size: 40px; background-color: {buttonColor}; color: {m_s_buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.abortButton.setStyleSheet(f"height: 100px; width: 100px; color: {m_s_buttonText}; font-size: 40px; background-color: {abortButtonColor}; color: {m_s_buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.startButton.setStyleSheet(f"height: 100px; width: 200px; color: {m_s_buttonText}; font-size: 40px; background-color: {buttonColor}; color: {m_s_buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.disposeButton.setStyleSheet(f"height: 100px; width: 200px; color: {m_s_buttonText}; font-size: 40px; background-color: {buttonColor}; color: {m_s_buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.statusLabel.setStyleSheet(f"height: 100px; font-size: 40px; border: 1px solid {borders}; border-radius: 5px; background-color: {standbyColor}; color: {standbyText};")
        # self.graph.setStyleSheet(f"background-color: {graphBackground}; border: 1px solid {borders}; border-radius: 5px;")
        self.setLayout(gridLayout)
        
    def handleStatusChange(self, status):
        self.statusLabel.setText(f"Status: {status}")
        if status == "Standby":
            self.statusLabel.setStyleSheet(f"height: 100px; width: 100px; font-size: 40px; background-color: {standbyColor}; color: {standbyText};")
        elif status == "In Progress":
            self.statusLabel.setStyleSheet(f"height: 100px; width: 100px; font-size: 40px; background-color: {inProgressColor}; color: {warningText};")
        elif status == "Disposal In Progress":
            self.statusLabel.setStyleSheet(f"height: 100px; width: 100px; font-size: 40px; background-color: {inProgressColor}; color: {warningText};")
        elif status == "Aborting Calibration":
            self.statusLabel.setStyleSheet(f"height: 100px; width: 100px; font-size: 40px; background-color: {abortButtonColor}; color: {warningText};")
        elif status == "Showing Previous Event":
            self.statusLabel.setStyleSheet(f"height: 100px; width: 100px; font-size: 40px; background-color: {standbyColor}; color: {m_s_buttonText};")
        else:
            self.statusLabel.setStyleSheet(f"height: 100px; width: 100px; font-size: 40px; background-color: {standbyColor}; color: {m_s_buttonText};")
        
    def toggleAbort(self):
        # Abort button click handler
        print("Abort Clicked")
        self.handleStatusChange("Aborting Calibration")
        # Click Animation for Abort Button
        scale_down = QPropertyAnimation(self.abortButton, b'size')
        scale_down.setDuration(100)  # Duration in milliseconds
        scale_down.setEndValue(self.abortButton.size() * 0.95)  # Scale down to 95%
        scale_down.setEasingCurve(QEasingCurve.Type.InOutQuad)

        scale_up = QPropertyAnimation(self.abortButton, b'size')
        scale_up.setDuration(100)  # Duration in milliseconds
        scale_up.setEndValue(self.abortButton.size())  # Scale back to original size
        scale_up.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.abort_click_animation = QSequentialAnimationGroup()
        self.abort_click_animation.addAnimation(scale_down)
        self.abort_click_animation.addAnimation(scale_up)

        self.abort_click_animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        
        
          
    def toggleDisposal(self):
        # Disposal button click handler
        print("Disposal Clicked")
        self.handleStatusChange("Disposal In Progress")
        # Click Animation for Dispose Button
        scale_down = QPropertyAnimation(self.disposeButton, b'size')
        scale_down.setDuration(100)  # Duration in milliseconds
        scale_down.setEndValue(self.disposeButton.size() * 0.95)  # Scale down to 95%
        scale_down.setEasingCurve(QEasingCurve.Type.InOutQuad)

        scale_up = QPropertyAnimation(self.disposeButton, b'size')
        scale_up.setDuration(100)  # Duration in milliseconds
        scale_up.setEndValue(self.disposeButton.size())  # Scale back to original size
        scale_up.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.dispose_click_animation = QSequentialAnimationGroup()
        self.dispose_click_animation.addAnimation(scale_down)
        self.dispose_click_animation.addAnimation(scale_up)

        self.dispose_click_animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def toggleEventLog(self):
        # Event button click handler
        
        # Toggle The Button Text
        if self.eventButton.text() == "Close Menu":
            self.eventButton.setText("Menu")
        else:
            self.eventButton.setText("Close Menu")
        
        # Click Animation for Event Log Button
        scale_down = QPropertyAnimation(self.eventButton, b'size')
        scale_down.setDuration(100)  # Duration in milliseconds
        scale_down.setEndValue(self.eventButton.size() * 0.95)  # Scale down to 95%
        scale_down.setEasingCurve(QEasingCurve.Type.InOutQuad)

        scale_up = QPropertyAnimation(self.eventButton, b'size')
        scale_up.setDuration(100)  # Duration in milliseconds
        scale_up.setEndValue(self.eventButton.size())  # Scale back to original size
        scale_up.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.click_animation = QSequentialAnimationGroup()
        self.click_animation.addAnimation(scale_down)
        self.click_animation.addAnimation(scale_up)

        self.click_animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
            
        
        # Animation for sidebar
        self.animation = QPropertyAnimation(self.sidebar, b"pos")
        self.animation.setDuration(500)  # Animation duration in milliseconds

        if self.sidebar.x() < 0:  # If sidebar is off-screen, slide it into view
            self.animation.setEndValue(QPoint(0, 0))
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
        
        # Click Animation for Start Button
        scale_down = QPropertyAnimation(self.startButton, b'size')
        scale_down.setDuration(100)  # Duration in milliseconds
        scale_down.setEndValue(self.startButton.size() * 0.95)  # Scale down to 95%
        scale_down.setEasingCurve(QEasingCurve.Type.InOutQuad)

        scale_up = QPropertyAnimation(self.startButton, b'size')
        scale_up.setDuration(100)  # Duration in milliseconds
        scale_up.setEndValue(self.startButton.size())  # Scale back to original size
        scale_up.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.start_click_animation = QSequentialAnimationGroup()
        self.start_click_animation.addAnimation(scale_down)
        self.start_click_animation.addAnimation(scale_up)

        self.start_click_animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        
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
