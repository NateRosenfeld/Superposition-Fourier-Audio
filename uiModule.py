# Import necessary libraries for the UI and program functionality
import tkinter as tk  # Tkinter is used to create the GUI
from tkinter import ttk  # ttk provides themed widgets (like buttons, entry fields)
import mainProgram  # Import the main program where the superposition calculations are done
import spectrogram  # Import the spectrogram module to create visualizations of sound data

# Define a function to start the UI
def startUI():
   # Create the root window for the tkinter UI
   root = tk.Tk()
   root.title("Quantum Superposition Project")  # Set the title of the window

   # Add a label to ask for the number of outcomes for the quantum state
   label = tk.Label(root, text="How many outcomes of this theoretical quantum state would you like?")
   label.pack(pady=10)  # Pack the label with some padding for better layout

   # Create a StringVar to hold the user input for the number of outcomes
   numOutcomesVar = tk.StringVar()
   entry = ttk.Entry(root, textvariable=numOutcomesVar)  # Create an entry widget to get user input
   entry.pack(pady=5)  # Pack the entry widget with some padding

   # Define the function to start the main program when the user clicks "Start"
   def startMainProgram():
       try:
           # Attempt to get the user input as an integer
           numOutcomes = int(numOutcomesVar.get())
           root.destroy()  # Close the tkinter window
           mainProgram.main(numOutcomes)  # Call the main program with the user input as argument
       except ValueError:
           # If the user input is not a valid number, show an error message
           tk.messagebox.showerror("Invalid Input", "Please enter a valid number.")

   # Add a button to start the main program
   button = ttk.Button(root, text="Start", command=startMainProgram)  # Button will call startMainProgram when clicked
   button.pack(pady=10)  # Pack the button with some padding

   # Start the tkinter main loop to display the UI and wait for user interaction
   root.mainloop()


# Define a function to analyze the spectrogram, which is triggered from elsewhere in the program
def analyzeSpectrogramCallback(frequencies):
   import spectrogram  # Import the spectrogram module only when this function is called
   spectrogram.create_spectrogram(frequencies)  # Call the create_spectrogram function from the spectrogram module


# If this module is run directly, start the UI
if __name__ == "__main__":
   startUI()  # Call the function to start the user interface
