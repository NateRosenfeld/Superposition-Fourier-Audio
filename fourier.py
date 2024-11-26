import numpy as np  # Import numpy for mathematical operations like Fourier transforms
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import to embed Matplotlib plots into tkinter


# Function to compute the Fast Fourier Transform (FFT) of a signal
def computeFFT(signal, sampleRate):
    """
   Compute the Fourier Transform of the signal.
   This transforms the time-domain signal into the frequency domain.
   :param signal: The input signal (e.g., sum of waves).
   :param sampleRate: Sampling rate of the signal in Hz.
   :return: frequencies (Hz) and their corresponding FFT magnitudes.
   """
    # np.fft.rfftfreq generates an array of frequency bins based on the signal length and sample rate
    freqs = np.fft.rfftfreq(len(signal), 1 / sampleRate)  # Frequency array (positive frequencies only for real signals)

    # np.fft.rfft computes the one-dimensional n-point FFT for real input, returning only positive frequencies
    fftMagnitudes = np.abs(np.fft.rfft(signal))  # Compute the magnitude of the FFT (absolute value)

    # Return the frequency bins and the corresponding FFT magnitudes
    return freqs, fftMagnitudes


# Function to plot the Fourier Transform in a tkinter window
def plotFFTInTkinter(signal, sampleRate, root):
    """
   Plot the Fourier Transform in a tkinter window.
   :param signal: The input signal (e.g., sum of waves).
   :param sampleRate: Sampling rate of the signal in Hz.
   :param root: The tkinter root window or a frame to embed the plot.
   """
    # Compute the Fourier Transform using the computeFFT function
    freqs, fftMagnitudes = computeFFT(signal, sampleRate)

    # Create a new Matplotlib figure with a specified size
    fig, ax = plt.subplots(figsize=(8, 4))  # Create a subplot (figure and axes)

    # Plot the Fourier Transform (frequency vs. magnitude) on the axes
    ax.plot(freqs, fftMagnitudes, color='blue')  # Plot the frequencies against their magnitudes

    # Set the title and labels for the axes
    ax.set_title("Fourier Transform")  # Title of the plot
    ax.set_xlabel("Frequency (Hz)")  # X-axis label: frequency in Hz
    ax.set_ylabel("Amplitude")  # Y-axis label: FFT magnitude (amplitude)

    # Enable grid lines for better readability of the plot
    ax.grid(True)

    # Embed the Matplotlib figure into the tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=root)  # Create a Tkinter canvas widget for the figure
    canvas_widget = canvas.get_tk_widget()  # Get the Tkinter widget for the canvas
    canvas_widget.pack()  # Pack the canvas widget into the tkinter window (add it to the window layout)
    canvas.draw()  # Draw the plot to update the canvas


# Function to plot the Fourier Transform in a standalone Matplotlib window
def plotFFTStandalone(signal, sampleRate):
    """
   Plot the Fourier Transform in a standalone Matplotlib window.
   :param signal: The input signal (e.g., sum of waves).
   :param sampleRate: Sampling rate of the signal in Hz.
   """
    # Compute the Fourier Transform using the computeFFT function
    freqs, fftMagnitudes = computeFFT(signal, sampleRate)

    # Create a new Matplotlib figure for standalone plotting
    plt.figure(figsize=(8, 4))  # Create a figure with the specified size

    # Plot the Fourier Transform (frequency vs. magnitude)
    plt.plot(freqs, fftMagnitudes, color='blue')  # Plot the frequencies against their magnitudes

    # Set the title and labels for the plot
    plt.title("Fourier Transform")  # Title of the plot
    plt.xlabel("Frequency (Hz)")  # X-axis label: frequency in Hz
    plt.ylabel("Amplitude")  # Y-axis label: FFT magnitude (amplitude)

    # Enable grid lines for better readability of the plot
    plt.grid(True)

    # Display the plot in a new window
    plt.show()  # Show the plot in a standalone window
