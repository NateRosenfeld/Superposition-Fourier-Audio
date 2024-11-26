import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import spectrogram

# Function to compute and display the spectrogram
def create_spectrogram(frequencies, sample_rate=44100, duration=2, num_points=2048, parent_window=None):
    # Create time array and signal
    t = np.linspace(0, duration, num_points, endpoint=False)
    signal = np.zeros_like(t)

    # Add the frequencies to the signal (sum of sinusoids)
    for frequency in frequencies:
        signal += 0.5 * np.sin(2 * np.pi * frequency * t)

    # Adjust nperseg to ensure it doesn't exceed the signal length
    nperseg = min(1024, len(signal))

    # Compute the spectrogram using scipy
    f, t_spec, Sxx = spectrogram(signal, fs=sample_rate, nperseg=nperseg)

    fig, ax = plt.subplots()

    # Your spectrogram creation code here...


    # ... existing code up to spectrogram computation ...

    # Create single figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the spectrogram using the ax object

    im = ax.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='auto')
    plt.colorbar(im, ax=ax, label='Intensity [dB]')
    ax.set_title('Spectrogram')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [s]')
    ax.set_ylim(0, 2000)  # Limit y-axis for better visibility of lower frequencies

    # Create canvas
    canvas = FigureCanvasTkAgg(fig, master=parent_window)
    canvas_widget = canvas.get_tk_widget()

    canvas_widget.pack()