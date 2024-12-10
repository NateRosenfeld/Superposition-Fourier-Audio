import numpy as np  # Import numpy for mathematical operations like Fourier transforms
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import to embed Matplotlib plots into tkinter


# Function to compute the Fast Fourier Transform (FFT) of a signal
def computeFFT(signal, sampleRate):
    """
    Compute the Fourier Transform of the signal.
    """
    # Use a window function to reduce spectral leakage
    window = np.hanning(len(signal))
    windowed_signal = signal * window

    # Compute FFT with zero-padding for better frequency resolution
    n_points = len(signal)
    padded_length = 2 ** int(np.ceil(np.log2(n_points)))  # Next power of 2

    freqs = np.fft.rfftfreq(padded_length, 1 / sampleRate)
    fft = np.fft.rfft(windowed_signal, n=padded_length)
    fftMagnitudes = 2 * np.abs(fft) / n_points  # Normalize the magnitudes

    return freqs, fftMagnitudes


# Function to plot the Fourier Transform in a tkinter window
def plotFFTInTkinter(signal, sampleRate, root):
    """
    Plot the Fourier Transform in a tkinter window.
    """
    freqs, fftMagnitudes = computeFFT(signal, sampleRate)

    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot with higher resolution and better visibility
    ax.plot(freqs, fftMagnitudes, color='blue', linewidth=1)

    # Add grid and set better axis limits
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1000)  # Limit x-axis to relevant frequency range
    ax.set_ylim(0, np.max(fftMagnitudes) * 1.1)  # Add 10% padding to y-axis

    # Improve labels and title
    ax.set_title("Frequency Spectrum (FFT)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")

    # Find and annotate peaks
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(fftMagnitudes, height=np.max(fftMagnitudes) / 10)
    for peak in peaks:
        freq = freqs[peak]
        magnitude = fftMagnitudes[peak]
        if magnitude > np.max(fftMagnitudes) / 5:  # Only label significant peaks
            ax.annotate(f'{freq:.1f} Hz',
                        xy=(freq, magnitude),
                        xytext=(0, 10),
                        textcoords='offset points',
                        ha='center')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()


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
    plt.figure(figsize=(10, 8))  # Create a figure with the specified size

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
