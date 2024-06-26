import sys
import ast
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


windowBackground = "#18191b"
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
    eventData = pyqtSignal(str, int, float, str, list)
    
    
    
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
        
        # Align Scroll Area Items to The Vertical Top
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
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
            
            # Send Signal To Main Window When Event is Clicked, Which Will Send the "event" Signal with all corresponding data
            frames[event_key].clicked.connect(lambda checked, i=i: self.eventData.emit(events[f"event_{i}"][0], int(events[f"event_{i}"][1]), float(events[f"event_{i}"][2]), events[f"event_{i}"][3], ast.literal_eval(events[f"event_{i}"][4])))
            

