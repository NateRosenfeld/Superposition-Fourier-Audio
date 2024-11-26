import tkinter as tk  # Import tkinter for creating the graphical user interface (GUI)
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import to embed Matplotlib figures into tkinter

# Function to show Fourier Transform equations in a new Tkinter window
def showFourierEquations(root):
    # Create a new top-level window for displaying the Fourier equations
    mathWindow = tk.Toplevel(root)  # Create a new top-level window (pop-up)
    mathWindow.title("Fourier Transform Equations")  # Set the title of the window

    # LaTeX representations of the Fourier Transform equations to be displayed
    fourier_eqns = [
        r"$\psi(x) = \sum_{n} \left| \alpha_n \right| \cdot \exp(i 2 \pi f_n t)$",  # Equation for wave function in terms of Fourier coefficients
        r"$\alpha_n = \frac{1}{T} \int_{0}^{T} \psi(t) \cdot e^{-i 2 \pi f_n t} dt$",  # Equation for Fourier coefficient calculation
        r"$F(\omega) = \int_{-\infty}^{\infty} f(t) \cdot e^{-i \omega t} dt$",  # General form of the Fourier transform
        r"$f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} F(\omega) \cdot e^{i \omega t} d\omega$"  # Inverse Fourier transform
    ]

    # Create a matplotlib figure to render LaTeX equations
    fig, ax = plt.subplots(figsize=(8, 4))  # Create a Matplotlib figure and axis, set size of the plot
    ax.axis("off")  # Turn off the axes so they aren't displayed (just equations are shown)

    # Add each Fourier equation to the figure with proper formatting
    y_offset = 1  # Initial offset to place the first equation
    for eq in fourier_eqns:  # Loop through each Fourier equation
        ax.text(0.5, y_offset, eq, ha='center', va='center', fontsize=16)  # Add LaTeX formatted text to the figure
        y_offset -= 0.1  # Decrease the y-offset so the next equation appears lower

    # Create a canvas for Tkinter to embed the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=mathWindow)  # Convert the Matplotlib figure into a Tkinter widget
    canvas.draw()  # Draw the figure onto the canvas
    canvas.get_tk_widget().pack()  # Pack the canvas into the Tkinter window so it gets displayed

    # Optionally, add a "Close" button to close the window when pressed
    closeButton = tk.Button(mathWindow, text="Close", command=mathWindow.destroy)  # Create a close button
    closeButton.pack(pady=10)  # Pack the button into the window with some padding for spacing
