import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame, QLabel
from PyQt6.QtCore import Qt,QAbstractAnimation, QPropertyAnimation, QPoint, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PyQt6.QtGui import QColor, QPalette
from eventLog import EventLog
from graph import MakeGraph

# Color Palette
# --GraphBackground: #f9fafc;
# --GraphLine And Button Color: #526da4;
# --EventLog: #7182a6; 
# --GraphAxes: #d7deeb;

# --background: #efeff1;
# --foreground: #fbfbfb;
# --border: #dddee2;

# --text: #232529;
# --text-light: #5e636e;
# --text-lighter: #848995;

# --standby: #52a452;
# --inprogress: #a4a452;
# --warning: #a45252;

buttonColor = "#526da4"
buttonText = "#232529"
abortButtonColor = "#a61217"
graphBackground = "#f9fafc"
graphLine = "#526da4"
borders = "#dddee2"
eventLogBackground = "#7182a6"
        



class HMIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.eventID = None
        self.initializeUI()


    def initializeUI(self):

        self.setWindowTitle("Sensor Calibration")
        self.setGeometry(100, 100, 1024, 600)
        gridLayout = QGridLayout(self)  # Initialize a QGridLayout
        self.sidebar = EventLog(self)
        self.sidebar.move(-self.sidebar.width(), 0)
        self.graph = MakeGraph(self)
        
        # Signal Connections
        self.sidebar.eventTime.connect(self.graph.setEventTime)
        self.sidebar.eventData.connect(self.graph.setEventData)
        self.sidebar.eventDate.connect(self.graph.setEventDate)
        self.sidebar.eventSelected.connect(self.onEventSelected)



        # Event Log button at row 0, column 0
        self.eventButton = QPushButton("=")
        self.eventButton.clicked.connect(self.toggleEventLog)
        gridLayout.addWidget(self.eventButton, 0, 0, Qt.AlignmentFlag.AlignTop)
        
        # Abort at row 0, column 1
        self.abortButton = QPushButton("Abort")
        self.abortButton.clicked.connect(self.toggleAbort)

        gridLayout.addWidget(self.abortButton, 0, 1, Qt.AlignmentFlag.AlignTop)
        
        # Dispose at row 0, column 2 and 3
        self.disposeButton = QPushButton("Dispose")
        self.disposeButton.clicked.connect(self.toggleDisposal)     
        gridLayout.addWidget(self.disposeButton, 0, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
        

        # Start button at row 0, column 4 and 5
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.onStartButtonClick)
        gridLayout.addWidget(self.startButton, 0, 3, 1, 2, Qt.AlignmentFlag.AlignRight)
        
        # Graph at row 1 and column 0 to 5
        # Graph Defined in graph.py
        gridLayout.addWidget(self.graph, 1, 1, 6, 4)
        
        # Clock at bottom left corner
        self.clock = QFrame()
        self.clock.setFrameShape(QFrame.Shape.StyledPanel)
        self.clock.setFrameShadow(QFrame.Shadow.Raised)
        gridLayout.addWidget(self.clock, 6, 0, 1, 1)
        

        # Add spacer items to create the 5x7 grid structure
        for row in range(1, 7):  # Add spacers for rows 1 to 6
            for col in range(6):  # Each row will have 4 columns
                gridLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), row, col)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#efeff1'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # styles
        self.eventButton.setStyleSheet(f"width: 100px; color: {buttonText}; font-size: 20px; background-color: {buttonColor}; color: {buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.abortButton.setStyleSheet(f"width: 100px; color: {buttonText}; font-size: 20px; background-color: {abortButtonColor}; color: {buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.startButton.setStyleSheet(f"width: 200px; color: {buttonText}; font-size: 20px; background-color: {buttonColor}; color: {buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        self.disposeButton.setStyleSheet(f"width: 200px; color: {buttonText}; font-size: 20px; background-color: {buttonColor}; color: {buttonText}; border: 1px solid {borders}; padding: 10px; border-radius: 5px;")
        # self.graph.setStyleSheet(f"background-color: {graphBackground}; border: 1px solid {borders}; border-radius: 5px;")
        self.setLayout(gridLayout)
        
    def toggleAbort(self):
        # Abort button click handler
        print("Abort Clicked")
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
        if self.eventButton.text() == "x":
            self.eventButton.setText("=")
        else:
            self.eventButton.setText("x")
        
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
        self.graph.showLiveGraph()
        
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
        self.eventID = eventId
        self.graph.showEventLog()

def main():
    app = QApplication(sys.argv)
    window = HMIWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
