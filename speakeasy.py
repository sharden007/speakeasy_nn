import subprocess
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
import wave
import pyaudio
import threading

# Function to list available microphones
microphones = subprocess.check_output(['python', 'mic_check.py']).decode().split('\n')
microphone_options = [line for line in microphones if 'found for' in line]

# Function to record audio
def record_audio(device_index=1):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    seconds = 5
    filename = "output.wav"

    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True,
                        input_device_index=device_index)
    except OSError as e:
        transcription.set(f"Error opening stream: {e}")
        return

    frames = []

    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to recognize speech and update the transcription
def recognize_speech(language):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile('output.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)
            transcription.set(text)
    except sr.UnknownValueError:
        transcription.set("Could not understand the audio")
    except sr.RequestError as e:
        transcription.set(f"API request error: {e}")
    except Exception as e:
        transcription.set(f"Recognition error: {e}")

# Function to start recording and transcribing in a separate thread
def start_transcription():
    transcription.set("Recording...")
    threading.Thread(target=record_and_transcribe).start()

def record_and_transcribe():
    try:
        device_index = int(device_index_var.get().split('=')[-1].strip(')')) if device_index_var.get() else 1
        record_audio(device_index)
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

# Microphone index selection
device_index_var = tk.StringVar()
device_index_label = tk.Label(root, text="Microphone Index:")
device_index_label.pack()
device_index_dropdown = ttk.Combobox(root, textvariable=device_index_var, values=microphone_options)
device_index_dropdown.pack()

# Buttons
start_button = tk.Button(root, text="Start Transcription", command=start_transcription)
start_button.pack(pady=5)

play_button = tk.Button(root, text="Play Audio", command=play_audio)
play_button.pack(pady=5)

# Run the GUI loop
root.mainloop()