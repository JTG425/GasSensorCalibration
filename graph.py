import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QShowEvent

class MakeGraph(QWidget):
    def __init__(self, parent=None):
        super(MakeGraph, self).__init__(parent)
        self.eventTimeValue = None
        self.eventDataValues = []
        self.eventDateValue = None
        self.gridLayout = QGridLayout
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.showLiveGraph()

    def showLiveGraph(self):
        time = [1, 2, 3, 4, 5]
        data = [0.53, 0.60, 0.61, 0.62, 0.7]
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', 'PPM', color='black')
        self.graphWidget.setTitle('Concentration In PPM', color='black')
        self.graphWidget.plot(time, data)
        
        print("Live graph shown")

    def setEventTime(self, time):
        self.eventTimeValue = time

    def setEventData(self, data):
        self.eventDataValues = data
    
    def setEventDate(self, date):
        self.eventDateValue = date

    def showEventLog(self):
        if self.eventTimeValue is None or self.eventDataValues == [] or self.eventDateValue is None:
            print("No data to show")
        else:
            print(f"{self.eventDateValue} Data Plotted")
