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

'''
    This class is responsible for creating the event log that displays the events that have taken place
    The 'events.txt' file is populated with 

'''

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

def read_event_count(filename, line_number):
    with open(filename, 'r') as file:
        for current_line, content in enumerate(file, 1):
            if current_line == line_number:
                return content.strip()  # Strip to remove any leading/trailing whitespace
    return None 

def read_event(filename, line_number):
    lines = [] 
    with open(filename, 'r') as file:
        for current_line, content in enumerate(file, 1): 
            if current_line >= line_number:
                lines.append(content.strip()) 
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
        self.setFixedSize(screen.width()-500, screen.height())
        self.setAutoFillBackground(True)

        
        # Create the scroll area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        
        # Hide Scroll Bars
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollContent = QWidget(self.scrollArea)
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollArea.setWidget(self.scrollContent)
        self.layout.addWidget(self.scrollArea)
    
        self.scrollContent.setContentsMargins(10,100,10,10)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.raise_()
        
        # Enable Touch Scrolling on the Scroll Area
        QScroller.grabGesture(self.scrollArea.viewport(), QScroller.ScrollerGestureType.TouchGesture)
        
        self.title = QLabel("Event Log", self.scrollContent)
        self.title.setStyleSheet(
            "font-size: 48px;"
            "color: white;"
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
            frames[event_key].setStyleSheet(
                f"background: {eventLogBackground};"
                f"color: {m_s_buttonText};"
                "font-size: 24px;"
                "height: 100px;"
                f"border: 1px solid {borders};"
                "margin-bottom: 10px;"
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

