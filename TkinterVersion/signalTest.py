import time
import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

class signalPlot():
    size = 100

    # Set up interactive mode for live updating
    plt.ion()

    count = 0

    # Generate a time vector with evenly spaced samples
    t = np.linspace(0, size, num=size)
    waveform = np.zeros(size)  # Initialize the waveform array with zeros
    peak = 0
    s = 10


    avg_s = int(size/s)

    # For Verifying Results of Continuous Average
    avg_a = np.empty(avg_s)

    # For Calculating Continuous Average
    avg_c = 0

    # For Calculating Continuous Average
    avg_sum = 0
    avg = 0



    while count < size:
        # Update the waveform array with a step-like function
        step = random.uniform(0.01, 0.02)
        noise = random.uniform(-0.001,0.001)

        if count % s == 0 and count != 0 and count <= 60:
            waveform[count] = waveform[count-1] + step
            avg_a[avg_c] = step
            avg_sum += step
            avg_c+=1
            if count == 60:
                peak = waveform[count]
        elif count > s and count < 60:
            diff = count % s
            waveform[count] = waveform[count-diff]+noise
        elif count > 60:
            waveform[count] = peak+noise

        if count >= s:
            avg = avg_sum/avg_c
        

        current = waveform[:count + 1]
    
    
    
        # Clear the previous plot
        plt.clf()

        complete_text = "Calibrating"
        complete = False
        # Plot the updated waveform
        plt.plot(t[:count + 1], current)
        plt.title('Gas Concentration (PPM) vs Time (s)')
        plt.xlabel('Time (s)')
        plt.ylabel('Concentration (PPM)')
    
        if count >= 75:
            complete = True
            plt.axvline(x=75, linestyle='dotted', color='red', label='Vertical Line')
            plt.axvline(x=70, linestyle='dotted', color='grey', label='Vertical Line')
        if complete == True:
            complete_text = "Done"
            plt.text(0.02, 0.79,f'Status: {complete_text}, Open Release Valve', ha='left', va='center', transform=plt.gca().transAxes,
                bbox=dict(facecolor='red', alpha=0.5))
            plt.text(0.02, 0.95, f'Final Average Step: {avg:.6f} PPM', ha='left', va='center', transform=plt.gca().transAxes,
                bbox=dict(facecolor='grey', alpha=0.5))
            plt.text(0.02, 0.87, f'Final Average Interval: {s:.2f} Seconds', ha='left', va='center', transform=plt.gca().transAxes,
                bbox=dict(facecolor='grey', alpha=0.5))
        else:            
            plt.text(0.02, 0.79,f'Status: {complete_text}', ha='left', va='center', transform=plt.gca().transAxes,
                bbox=dict(facecolor='yellow', alpha=0.5))
            plt.text(0.02, 0.95, f'Average Step: {avg:.6f} PPM', ha='left', va='center', transform=plt.gca().transAxes,
                bbox=dict(facecolor='grey', alpha=0.5))
            plt.text(0.02, 0.87, f'Average Interval: {s:.2f} Seconds', ha='left', va='center', transform=plt.gca().transAxes,
                bbox=dict(facecolor='grey', alpha=0.5))

        # Display the updated plot
        plt.draw()
        plt.pause(0.1)  # Adjust the pause duration as needed

        count += 1
    
    expected = np.sum(avg_a)/avg_c
    print("Calculated Average: ", avg)
    print("Expected Average: " , expected)


    # Turn off interactive mode
    plt.ioff()
    plt.show()