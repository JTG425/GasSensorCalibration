import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea, QFrame, QScroller
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QScreen
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
mainBackground = "#efeff1"

def read_event_count(filename, line_number):
    with open(filename, 'r') as file:
        for current_line, content in enumerate(file, 1):  # Start counting from 1
            if current_line == line_number:
                return content.strip()  # Strip to remove any leading/trailing whitespace and newline characters
    return None  # Return None if the specified line_number does not exist

def read_event(filename, line_number):
    lines = []  # List to store the lines
    with open(filename, 'r') as file:
        for current_line, content in enumerate(file, 1): 
            if current_line >= line_number:
                lines.append(content.strip())  # Append the line to the list
                if len(lines) == 5:  # Stop after reading 5 lines
                    break
    return lines if lines else None  # Return the list of lines if not empty, else return None

class EventLog(QWidget):
    # Signals
    eventSelected = pyqtSignal(int)
    eventTime = pyqtSignal(int)
    eventData = pyqtSignal(object)
    eventDate = pyqtSignal(str)
    
    
    def __init__(self, parent=None):
        super(EventLog, self).__init__(parent)
        self.initEventLog()

    def initEventLog(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        screen = QApplication.primaryScreen().geometry()
        self.setFixedSize(screen.width() - 200, screen.height() - 100)
        self.layout.setContentsMargins(20, 125, 10, 10)
        self.setAutoFillBackground(True)
        
        # Create the scroll area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollContent = QWidget(self.scrollArea)
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollArea.setWidget(self.scrollContent)
        self.layout.addWidget(self.scrollArea)
    
        # Enable Touch Scrolling on the Scroll Area
        QScroller.grabGesture(self.scrollArea.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        
        # Example content in the sidebar
        self.title = QLabel("Event Log", self.scrollContent)
        self.title.setStyleSheet(
            "font-size: 30px;"
        )
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.scrollLayout.addWidget(self.title)

        num_events = int(read_event_count('./logs/eventCount.txt', 1))
        offset = 1
        events = {}
        frames = {}
        for i in range(num_events):
            event_key = f"event_{i}"
            events[event_key] = read_event('./logs/events.txt', i * 5 + offset)
            offset = offset + 1
            frames[event_key] = QPushButton(self.scrollContent)
            frames[event_key].setFixedSize(350, 75)
            frames[event_key].setStyleSheet(
                f"background: {eventLogBackground};"
                "font-size: 40px;"
                "width: 100%;"
                f"border: 1px solid {borders};"
            )
            self.scrollLayout.addWidget(frames[event_key])
            frames[event_key].setText(events[event_key][0])

            # Sends Signal To Main Window When Event is Clicked To Display Calibration Data
            frames[event_key].clicked.connect(lambda checked, eventId=i: self.eventSelected.emit(eventId))
            
            # Sends Time Calibration Took To Graph.py For use as the x axis
            frames[event_key].clicked.connect(lambda checked, eventId=i: self.eventTime.emit(int(events[f"event_{eventId}"][1])))
            
            # Sends Date Calibration Took Place To Graph.py
            frames[event_key].clicked.connect(lambda checked, eventId=i: self.eventDate.emit(events[f"event_{eventId}"][0]))
            
            # Sends List of Calibration Data to Graph.py For use as the y axis
            frames[event_key].clicked.connect(lambda checked, eventId=i: self.eventData.emit(list(map(float, events[f"event_{eventId}"][4].split()))))
