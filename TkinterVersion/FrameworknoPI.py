from tkinter import *
from datetime import datetime

def start_calibration():
    # Add logic for starting calibration
    print("Starting Calibration...")

def start_disposal():
    # Add logic for starting disposal
    print("Starting Disposal...")
    
def toggle_event_log():
    # Add logic for toggling event log
    print("Toggling Event Log...")



GUI = Tk()
# Dimensions for ELCROW 7 inch Display.
GUI_Width = 1024
GUI_Height = 600

GUI.geometry(f"{GUI_Width}x{GUI_Height}")
GUI.title("Calibration App")


# Variables for PPM levels - Will be defined by RP4 GPIO input signals
ExpectedPPM = IntVar()
CurrentPPM = IntVar()

# Time Widget
now = datetime.now()
current_time = now.strftime("%H:%M")
timeLabel = Label(GUI, text=current_time, width=10, height=3, font=("Arial", 16), border=1, relief="solid")
timeLabel.place(x=465, y=15)


# Button Widgets
eventLogButton = Button(GUI, text='Event Log', font=("Ariel", 16), command=toggle_event_log, width=10, height=3)
eventLogButton.place(x=10, y=10)

startButton = Button(GUI, text='Start Calibration', font=("Ariel", 16), command=start_disposal, width=10, height=3)
startButton.place(x=880, y=10)



GUI.mainloop()