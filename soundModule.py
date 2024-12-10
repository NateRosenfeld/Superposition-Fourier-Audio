import pygame  # Import pygame for sound functionality and playing sound
import numpy as np  # Import numpy for numerical operations like sine wave generation
import threading  # Import threading to allow playing sound in the background

# Initialize pygame mixer to handle audio playback
pygame.mixer.pre_init(allowedchanges=0, channels=1)  # Set pre-initialization parameters for pygame mixer
pygame.mixer.init()  # Initialize the pygame mixer to start audio playback


# Function to create a sound wave given frequencies, duration, and sample rate
def createSoundWave(frequencies, duration, sampleRate=44100):
    t = np.linspace(0, duration, int(sampleRate * duration), endpoint=False)

    # Normalize the amplitude based on number of frequencies
    amplitude = 0.5 / len(np.atleast_1d(frequencies))  # Adjust amplitude to prevent clipping

    # Create the combined wave
    wave = np.sum([amplitude * np.sin(2 * np.pi * f * t) for f in np.atleast_1d(frequencies)], axis=0)

    # Ensure the wave stays within [-1, 1] range before converting to 16-bit
    wave = np.clip(wave, -1, 1)
    return (wave * 32767).astype(np.int16)


# Function to play sound for multiple frequencies (creating a superposition of waves)
def playSuperpositionSound(frequencies):
    duration = 2
    # Ensure frequencies is always a list
    if isinstance(frequencies, (int, float)):
        frequencies = [frequencies]
    soundWave = createSoundWave(frequencies, duration)
    sound = pygame.sndarray.make_sound(soundWave)
    sound_thread = threading.Thread(target=lambda: sound.play(-1))
    sound_thread.start()


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
