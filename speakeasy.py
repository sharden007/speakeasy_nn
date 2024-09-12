import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
import wave
import pyaudio
import threading

# Function to record audio
def record_audio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 5 seconds
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to recognize speech and update the transcription
def recognize_speech(language):
    recognizer = sr.Recognizer()
    with sr.AudioFile('output.wav') as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            transcription.set(text)
        except sr.UnknownValueError:
            transcription.set("Could not understand the audio")
        except sr.RequestError as e:
            transcription.set(f"API request error: {e}")

# Function to start recording and transcribing in a separate thread
def start_transcription():
    transcription.set("Recording...")
    threading.Thread(target=record_and_transcribe).start()

def record_and_transcribe():
    try:
        record_audio()
        language = language_var.get()
        recognize_speech(language)
    except Exception as e:
        transcription.set(f"Error: {e}")

# Function to play back the recorded audio
def play_audio():
    try:
        chunk = 1024
        wf = wave.open('output.wav', 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
    except FileNotFoundError:
        transcription.set("No audio file found. Please record first.")
    except Exception as e:
        transcription.set(f"Playback error: {e}")

# GUI setup
root = tk.Tk()
root.title("Speech Recognition")

# Transcription label
transcription = tk.StringVar()
transcription_label = tk.Label(root, textvariable=transcription, wraplength=400)
transcription_label.pack(pady=10)

# Language selection
language_var = tk.StringVar(value='en-US')
language_label = tk.Label(root, text="Select Language:")
language_label.pack()
language_dropdown = ttk.Combobox(root, textvariable=language_var, values=['en-US', 'es-ES'])
language_dropdown.pack()

# Buttons
start_button = tk.Button(root, text="Start Transcription", command=start_transcription)
start_button.pack(pady=5)

play_button = tk.Button(root, text="Play Audio", command=play_audio)
play_button.pack(pady=5)

# Run the GUI loop
root.mainloop()