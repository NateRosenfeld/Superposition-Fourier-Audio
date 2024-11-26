import pygame  # Import pygame for sound functionality and playing sound
import numpy as np  # Import numpy for numerical operations like sine wave generation
import threading  # Import threading to allow playing sound in the background


# Initialize pygame mixer to handle audio playback
pygame.mixer.pre_init(allowedchanges=0, channels=1)  # Set pre-initialization parameters for pygame mixer
pygame.mixer.init()  # Initialize the pygame mixer to start audio playback


# Function to create a sound wave given frequencies, duration, and sample rate
def createSoundWave(frequencies, duration, sampleRate=44100):
   # Create a time array 't' from 0 to duration, with the specified sample rate (number of samples per second)
   t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)  # Time array for the sound wave

   # Initialize the sound wave as a zero array of the same length as the time array
   wave = np.zeros(len(t))  # Start with an empty wave (all zeros)

   # If the input frequencies is a single value (int or float), convert it to a list for consistency
   if isinstance(frequencies, (int, float)):  # Check if frequencies is not a list
       frequencies = [frequencies]  # Convert to list for consistency

   # Sum sine waves for each frequency in the frequencies list
   for frequency in frequencies:  # Loop through all frequencies
       wave += 0.5 * np.sin(2 * np.pi * frequency * t)  # Create a sine wave for each frequency and add it to the wave

   # Convert the wave to 16-bit PCM format (appropriate for sound playback)
   return (wave * 32767).astype(np.int16)  # Scale the wave to 16-bit PCM format (range -32768 to 32767)


# Function to play sound for multiple frequencies (creating a superposition of waves)
def playSuperpositionSound(frequencies):
   duration = 2  # Duration of the sound in seconds
   soundWave = createSoundWave(frequencies, duration)  # Generate the sound wave by summing multiple frequencies

   # Create a pygame Sound object from the numpy array (the sound wave)
   sound = pygame.sndarray.make_sound(soundWave)  # Convert the numpy array to a pygame sound object

   # Play sound in a new thread to allow it to play in the background (non-blocking)
   sound_thread = threading.Thread(target=lambda: sound.play(-1))  # Create a thread to play the sound in a loop
   sound_thread.start()  # Start the sound-playing thread


# Function to play sound for a single frequency
def playSound(frequency):
   duration = 2  # Duration of the sound in seconds
   soundWave = createSoundWave(frequency, duration)  # Generate the sound wave for a single frequency

   # Create a pygame Sound object from the numpy array (the sound wave)
   sound = pygame.sndarray.make_sound(soundWave)  # Convert the numpy array to a pygame sound object
   sound.play(-1)  # Play the sound in a loop (-1 means infinite loop)


# Function to stop the current sound being played
def stopSound():
   pygame.mixer.stop()  # Stop all sounds currently playing through the pygame mixer


# Function to shift the pitch of a given frequency randomly within a range
def shiftPitch(frequency):
   shift = np.random.uniform(-50, 50)  # Generate a random pitch shift between -50 Hz and +50 Hz
   newFrequency = frequency + shift  # Apply the shift to the original frequency
   return newFrequency  # Return the new frequency with the pitch shift applied
