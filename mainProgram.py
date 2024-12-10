import matplotlib.pyplot as plt  # Importing matplotlib for plotting graphs
from matplotlib.animation import FuncAnimation  # Importing FuncAnimation for animating plots
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To embed matplotlib figures into tkinter
import tkinter as tk  # Import tkinter for creating the GUI
import threading  # Import threading to play sound asynchronously without blocking the GUI
import soundModule  # Importing custom soundModule for sound-related operations
import numpy as np  # Import numpy for mathematical operations
import spectrogram  # Importing custom spectrogram module for spectrogram visualization
import fourier  # Importing custom fourier module for Fourier transforms


# Function to update the equation label on the tkinter canvas
def updateEquationLabel(equation, equationCanvas):
   # Clear previous equation from the canvas
   equationCanvas.delete("all")
   # Create a new text element on the canvas to show the current equation
   equationCanvas.create_text(400, 25, text=equation, font=("Helvetica", 16), fill="blue")


# Function to visualize the individual waves, their sum, and the collapsed state (if applicable)
def visualizeWaves(root, frequencies, collapsedFrequency, isCollapsed, equationCanvas, duration=2, sampleRate=44100):
   # Calculate how many points to show (use more points for better visualization)
   display_points = 2000  # Increased from 1000 for better resolution
   
   t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)
   t_display = t[:display_points]  # Time array for display
   numWaves = len(frequencies)

   fig, ax = plt.subplots(numWaves + 1, 1, figsize=(10, 2 * (numWaves + 1)))
   lines = []
   labels = []

   # Create subplots for each individual wave
   for i in range(numWaves):
       line, = ax[i].plot(t_display, np.zeros(display_points))
       ax[i].set_title(f"Wave for Frequency: {frequencies[i]} Hz")
       ax[i].set_xlabel("Time [s]")
       ax[i].set_ylabel("Amplitude")
       ax[i].set_ylim(-1, 1)
       lines.append(line)
       label = ax[i].text(0.5, 0, "Collapsed", color="red", fontsize=14,
                         ha="center", va="center", visible=False)
       labels.append(label)

   sumLine, = ax[numWaves].plot(t_display, np.zeros(display_points), color='k')
   ax[numWaves].set_title("Sum of Waves")
   ax[numWaves].set_xlabel("Time [s]")
   ax[numWaves].set_ylabel("Amplitude")
   ax[numWaves].set_ylim(-numWaves * 0.5, numWaves * 0.5)

   equation = ax[numWaves].text(
       0.5, 0.9 * numWaves * 0.5,
       "", fontsize=14, ha='center', va='center', color='blue',
       transform=ax[numWaves].transData
   )

   def update(frame):
       if isCollapsed[0] and collapsedFrequency[0] is not None:
           wave = 0.5 * np.sin(2 * np.pi * collapsedFrequency[0] * t_display + frame / 10)
           sumLine.set_ydata(wave)
           for label in labels:
               label.set_visible(True)
           equation.set_text(f"Collapsed: ψ(t) = 0.5 sin(2π {collapsedFrequency[0]:.1f} t)")
           updateEquationLabel(f"Collapsed: ψ(t) = 0.5 sin(2π {collapsedFrequency[0]:.1f} t)", equationCanvas)
           return [sumLine] + labels + [equation]
       else:
           # Calculate complete waves with proper phase relationships
           waves = [0.5 * np.sin(2 * np.pi * freq * t_display + frame / 10) for freq in frequencies]
           
           # Update individual wave plots
           for i, wave in enumerate(waves):
               lines[i].set_ydata(wave)
           
           # Calculate true superposition
           sumWave = np.sum(waves, axis=0)
           sumLine.set_ydata(sumWave)

           terms = " + ".join([f"0.5 sin(2π {f} t)" for f in frequencies])
           equation.set_text(f"ψ(t) = {terms}")
           updateEquationLabel(f"Superposition: ψ(t) = {terms}", equationCanvas)
           
           return lines + [sumLine, equation]

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

        # Create main frames for different sections
        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Create equation canvas in left frame
        equationCanvas = tk.Canvas(left_frame, width=800, height=50)
        equationCanvas.pack(pady=5)

        # Store the superposition wave
        duration = 2
        sampleRate = 44100
        t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)
        sumWave = np.zeros_like(t)

        # Create wave visualization in left frame
        def visualizeWavesCallback():
            nonlocal sumWave
            visualizeWaves(left_frame, frequencies, collapsedFrequency, isCollapsed, equationCanvas, duration, sampleRate)
            for freq in frequencies:
                sumWave += 0.5 * np.sin(2 * np.pi * freq * t)

        visualizeWavesCallback()

        # Create Fourier analysis frame
        fourier_frame = tk.Frame(right_frame)
        fourier_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        fourier.plotFFTInTkinter(sumWave, sampleRate, fourier_frame)

        # Create spectrogram frame
        spectrogram_frame = tk.Frame(right_frame)
        spectrogram_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        spectrogram.create_spectrogram(frequencies, sample_rate=sampleRate, duration=duration, parent_window=spectrogram_frame)

        # Create a label for displaying equations
        equation_label = tk.Label(right_frame, text="", font=("Helvetica", 12))
        equation_label.pack(pady=5)

        def updateEquations():
            if isCollapsed[0] and collapsedFrequency[0] is not None:
                equation_label.config(text=f"Collapsed: ψ(t) = 0.5 sin(2π {collapsedFrequency[0]:.1f} t)")
            else:
                terms = " + ".join([f"0.5 sin(2π {f} t)" for f in frequencies])
                equation_label.config(text=f"Superposition: ψ(t) = {terms}")

        # Update equations in real-time
        def update():
            updateEquations()
            root.after(100, update)  # Update every 100 ms

        update()  # Start the update loop

        # Function to handle the collapse state when the Enter key is pressed
        def collapseState(event):
            if not isCollapsed[0]:  # Only collapse if it's not already collapsed
                collapsedFrequency[0] = soundModule.shiftPitch(frequencies[0])  # Collapse to a new frequency
                isCollapsed[0] = True  # Mark the state as collapsed
                soundModule.stopSound()  # Stop any currently playing sound
                soundModule.playSound(collapsedFrequency[0])  # Play the new collapsed frequency sound
                print(f"Collapsed to frequency: {collapsedFrequency[0]} Hz")

        root.bind("<Return>", collapseState)  # Bind the Enter key to the collapseState function

        # Add stop button at the bottom
        stop_button = tk.Button(
            root,
            text="Stop",
            command=lambda: (soundModule.stopSound(), root.quit(), root.destroy()),
            bg='red',
            fg='white'
        )
        stop_button.grid(row=1, column=0, columnspan=2, pady=5)

        def save_plot():
            fig = plt.gcf()  # Get the current figure
            fig.savefig("visualization.png")  # Save as PNG
            print("Plot saved as visualization.png")

        save_button = tk.Button(right_frame, text="Save Plot", command=save_plot)
        save_button.pack(pady=5)

        root.mainloop()

    except ValueError:
        print("Please enter a valid number.")