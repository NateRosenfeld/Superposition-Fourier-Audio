import matplotlib.pyplot as plt  # Importing matplotlib for plotting graphs
from matplotlib.animation import FuncAnimation  # Importing FuncAnimation for animating plots
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To embed matplotlib figures into tkinter
import tkinter as tk  # Import tkinter for creating the GUI
import threading  # Import threading to play sound asynchronously without blocking the GUI
import soundModule  # Importing custom soundModule for sound-related operations
import numpy as np  # Import numpy for mathematical operations
import spectrogram  # Importing custom spectrogram module for spectrogram visualization
import fourier  # Importing custom fourier module for Fourier transforms
import mathModule  # Importing custom mathModule for mathematical equations related to Fourier transforms

from PIL import Image, ImageTk  # For converting Matplotlib image to Tkinter format


# Function to update the equation label on the tkinter canvas
def updateEquationLabel(equation, equationCanvas):
   # Clear previous equation from the canvas
   equationCanvas.delete("all")
   # Create a new text element on the canvas to show the current equation
   equationCanvas.create_text(400, 25, text=equation, font=("Helvetica", 16), fill="blue")


# Function to visualize the individual waves, their sum, and the collapsed state (if applicable)
def visualizeWaves(root, frequencies, collapsedFrequency, isCollapsed, equationCanvas, duration=2, sampleRate=44100):
   # Create a time array from 0 to 'duration' with 'sampleRate' samples per second
   t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)
   numWaves = len(frequencies)  # Number of waves based on the number of frequencies provided


   # Create a Matplotlib figure with multiple subplots, one for each frequency wave plus a sum wave
   fig, ax = plt.subplots(numWaves + 1, 1, figsize=(10, 2 * (numWaves + 1)))
   lines = []  # List to store plot line objects for individual waves
   labels = []  # List to store text labels (collapsed state) for each wave


   # Create subplots for each individual wave
   for i in range(numWaves):
       line, = ax[i].plot(t[:1000], np.zeros(1000))  # Initialize each plot with zeros (empty)
       ax[i].set_title(f"Wave for Frequency: {frequencies[i]} Hz")  # Title each plot with the respective frequency
       ax[i].set_xlabel("Time [s]")  # Label the x-axis
       ax[i].set_ylabel("Amplitude")  # Label the y-axis
       ax[i].set_ylim(-1, 1)  # Set y-axis limits for visualization
       lines.append(line)  # Add the line object to the list
       label = ax[i].text(0.5, 0, "Collapsed", color="red", fontsize=14,  # Add text indicating "Collapsed"
                          ha="center", va="center", visible=False)  # Initially hidden
       labels.append(label)  # Add the label object to the list


   # Create a subplot for the sum of the waves (superposition)
   sumLine, = ax[numWaves].plot(t[:1000], np.zeros(1000), color='k')  # Initialize the sum plot with zeros (black)
   ax[numWaves].set_title("Sum of Waves")  # Title for the sum of waves
   ax[numWaves].set_xlabel("Time [s]")  # Label the x-axis
   ax[numWaves].set_ylabel("Amplitude")  # Label the y-axis
   sumWaveAmplitude = numWaves * 0.5  # Estimate the max amplitude for the sum of waves
   ax[numWaves].set_ylim(-sumWaveAmplitude, sumWaveAmplitude)  # Set y-axis limits for sum wave


   # Equation text for displaying the superposition equation
   equation = ax[numWaves].text(
       0.5, 0.9 * sumWaveAmplitude,
       "", fontsize=14, ha='center', va='center', color='blue',
       transform=ax[numWaves].transData
   )


   # Function to update the waves and sum wave for animation
   def update(frame):
       sumWave = np.zeros(len(t))  # Initialize an array to accumulate the sum of waves
       if isCollapsed[0] and collapsedFrequency[0] is not None:  # Check if the state is collapsed
           # If collapsed, display only the collapsed wave
           wave = 0.5 * np.sin(2 * np.pi * collapsedFrequency[0] * t + frame / 10)
           sumLine.set_ydata(wave[:1000])  # Set the y-data of the sum line to the collapsed wave
           for label in labels:
               label.set_visible(True)  # Make the "Collapsed" label visible
           equation.set_text(f"Collapsed: ψ(t) = 0.5 sin(2π {collapsedFrequency[0]:.1f} t)")  # Update the equation
           updateEquationLabel(f"Collapsed: ψ(t) = 0.5 sin(2π {collapsedFrequency[0]:.1f} t)", equationCanvas)
           return [sumLine] + labels + [equation]  # Return updated elements for animation
       else:
           # If not collapsed, update individual waveforms
           for i, frequency in enumerate(frequencies):
               wave = 0.5 * np.sin(2 * np.pi * frequency * t + frame / 10)  # Calculate the wave for each frequency
               lines[i].set_ydata(wave[:1000])  # Update the plot for the individual wave
               sumWave += wave  # Add the current wave to the sum wave


           # Construct the superposition equation string
           terms = " + ".join([f"0.5 sin(2π {f} t)" for f in frequencies])
           equation.set_text(f"ψ(t) = {terms}")  # Update the equation text
           updateEquationLabel(f"Superposition: ψ(t) = {terms}", equationCanvas)  # Update equation on the canvas
           sumLine.set_ydata(sumWave[:1000])  # Update the sum plot with the accumulated wave
           return lines + [sumLine, equation]  # Return all lines and the equation for animation


   # Embed the Matplotlib figure in the tkinter window
   canvas = FigureCanvasTkAgg(fig, master=root)
   canvas_widget = canvas.get_tk_widget()
   canvas_widget.pack()  # Pack the canvas into the tkinter window


   # Function to handle the collapse state when the Enter key is pressed
   def collapseState(event):
       if not isCollapsed[0]:  # Only collapse if it's not already collapsed
           collapsedFrequency[0] = soundModule.shiftPitch(frequencies[0])  # Collapse to a new frequency
           isCollapsed[0] = True  # Mark the state as collapsed
           soundModule.stopSound()  # Stop any currently playing sound
           soundModule.playSound(collapsedFrequency[0])  # Play the new collapsed frequency sound
           print(f"Collapsed to frequency: {collapsedFrequency[0]} Hz")  # Print the collapsed frequency


   root.bind("<Return>", collapseState)  # Bind the Enter key to the collapseState function


   # Increase spacing between subplots for better visibility
   plt.subplots_adjust(hspace=1.5)


   # Create the animation object using FuncAnimation
   global ani  # Declare ani as global to prevent garbage collection
   ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=50, blit=True)  # Create the animation


   # Explicitly retain reference to ani to prevent it from being garbage collected
   canvas.mpl_connect('draw_event', lambda event: ani.event_source.start())


# Main function that runs the program
def main(numOutcomes=None):
    if numOutcomes is None:
        print("This script is intended to be called from the UI.")
        return

    try:
        if numOutcomes > 10:
            print("Limiting outcomes to 10.")
            numOutcomes = 10

        print(f"Alright! The state will have {numOutcomes} possible outcomes.")

        baseFrequency = 600
        frequencies = [baseFrequency + i * 50 for i in range(numOutcomes)]
        collapsedFrequency = [None]
        isCollapsed = [False]

        def playSound():
            soundModule.playSuperpositionSound(frequencies)

        threading.Thread(target=playSound, daemon=True).start()

        # Start tkinter GUI
        root = tk.Tk()
        root.title("Quantum Superposition Visualization")

        # Create a canvas to display the equation as a header
        equationCanvas = tk.Canvas(root, width=800, height=50)
        equationCanvas.pack(pady=10)

        # Store the superposition wave (to pass into Fourier analysis)
        duration = 2  # Duration of the signal in seconds
        sampleRate = 44100  # Sampling rate in Hz
        t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)
        sumWave = np.zeros_like(t)

        def visualizeWavesCallback():
            nonlocal sumWave
            visualizeWaves(root, frequencies, collapsedFrequency, isCollapsed, equationCanvas, duration, sampleRate)
            # Combine individual waves for Fourier analysis
            for freq in frequencies:
                sumWave += 0.5 * np.sin(2 * np.pi * freq * t)

        # Visualize waves initially
        visualizeWavesCallback()

        # Function to open a new window for Fourier analysis
        def openFourierWindow():
            fourierWindow = tk.Toplevel(root)  # Create a new window for Fourier analysis
            fourierWindow.title("Fourier Transform Analysis")
            fourier.plotFFTInTkinter(sumWave, sampleRate, fourierWindow)  # Pass the new window as parent

        # Add Fourier analysis button
        fftButton = tk.Button(
            root,
            text="Analyze Fourier",
            command=openFourierWindow  # Open Fourier analysis in a new window
        )
        fftButton.pack()

        # Function to open a new window for spectrogram analysis
        def openSpectrogramWindow():
            spectrogramWindow = tk.Toplevel(root)  # Create a new window for the spectrogram
            spectrogramWindow.title("Spectrogram Analysis")
            spectrogram.create_spectrogram(frequencies, sample_rate=sampleRate, duration=duration, parent_window=spectrogramWindow)

        # Add Spectrogram analysis button
        spectrogramButton = tk.Button(
            root,
            text="Analyze Spectrogram",
            command=openSpectrogramWindow  # Open spectrogram analysis in a new window
        )
        spectrogramButton.pack()

        # Add button to show Fourier Transform math
        fourierMathButton = tk.Button(
            root,
            text="Show Fourier Transform Math",
            command=lambda: mathModule.showFourierEquations(root)
        )
        fourierMathButton.pack()

        root.mainloop()

    except ValueError:
        print("Please enter a valid number.")