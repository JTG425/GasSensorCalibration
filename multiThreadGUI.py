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