# This Will be the File that contains the Main GUI Components for the Final Project:
#   => Need to use Two threads to prevent the GUI from Freezing as the signal is processed.
#   => The First Thread will be responsible for the GUI.
#   => The First Thread will recieve the results of the second thread and update the GUI accordingly.
#      1. A Graphical (live) Display of the Data, PPM vs Time.
#      2. A Status Indicator showing the following:
#           a. Green: Standby, Ready To Calibrate.
#           b. Yellow: Calibrating
#           c. Orange: : Calibrated, Ready to Release Into Disposal / Disposal In Progress
#           d. Red: Leak Detected, RUN.

#   => The Second Thread will be responsible for processing sensor input.

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget
import numpy as np

import time
import traceback, sys
import random

simulate = True


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exc()
            self.signals.error.emit((type(e), e, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Calibration GUI")
        self.setFixedSize(QSize(1024, 600))

        layout = QGridLayout()

        def create_log(label):
            widget = QLabel(label)
            widget.setFrameShape(QFrame.Shape.Box)
            widget.setFrameShadow(QFrame.Shadow.Plain)
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return widget

        def create_status(label):
            widget = QLabel(label)
            widget.setFrameShape(QFrame.Shape.Box)
            widget.setFrameShadow(QFrame.Shadow.Plain)
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return widget

        def create_clock(label):
            widget = QLabel(label)
            widget.setFrameShape(QFrame.Shape.Box)
            widget.setFrameShadow(QFrame.Shadow.Plain)
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            widget.setText(time.strftime("%H:%M:%S"))
            return widget

        def create_graph(data):
            widget = PlotWidget()
            widget.setLabel('left', 'PPM', units='PPM')
            widget.setLabel('bottom', 'Time', units='s')
            widget.showGrid(x=True, y=True)
            widget.setBackground('w')
            s = np.linspace(0, 100, len(data))
            widget.plot(s, data)
            return widget

        data = open("data.txt", "r")
        dataARR = [float(line) for line in data.readlines()]

        self.counter = 0
        self.l = QLabel()
        self.threadpool = QThreadPool()

        layout.addWidget(create_log("Event Log"), 0, 0)
        layout.addWidget(create_status("Status"), 0, 3)
        layout.addWidget(create_graph(dataARR), 1, 1, 3, 3)
        layout.addWidget(create_clock("Clock"), 3, 0)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start(1000)  # Timer fires every 1000 milliseconds (1 second)

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        try:
            with open("data.txt", "w") as file:
                for _ in range(100):
                    random_number = random.randint(0, 100)
                    file.write(str(random_number) + "\n")
                    time.sleep(1)
                    progress_callback.emit((_ * 100) / 4)
            return "Done."
        except Exception as e:
            return str(e)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        worker = Worker(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)


app = QApplication([])
window = MainWindow()
app.exec_()
