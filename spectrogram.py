import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import spectrogram
import tkinter as tk


# Function to compute and display the spectrogram
def create_spectrogram(frequencies, sample_rate=44100, duration=2, num_points=2048, parent_window=None):
    # Remove Toplevel creation and use parent_window directly
    t = np.linspace(0, duration, num_points, endpoint=False)
    signal = np.zeros_like(t)

    for frequency in frequencies:
        signal += 0.5 * np.sin(2 * np.pi * frequency * t)

    nperseg = min(1024, len(signal))
    f, t_spec, Sxx = spectrogram(signal, fs=sample_rate, nperseg=nperseg)

    fig, ax = plt.subplots(figsize=(8, 4))
    im = ax.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='auto')
    plt.colorbar(im, ax=ax, label='Intensity [dB]')
    ax.set_title('Spectrogram')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [s]')
    ax.set_ylim(0, 2000)

    canvas = FigureCanvasTkAgg(fig, master=parent_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)