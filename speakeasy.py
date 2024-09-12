import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
import wave
import pyaudio

# Function to recognize speech and update the transcription
def recognize_speech(language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            transcription.set(text)
        except sr.UnknownValueError:
            transcription.set("Could not understand the audio")
        except sr.RequestError:
            transcription.set("API request error")

# Function to start recording and transcribing
def start_transcription():
    language = language_var.get()
    recognize_speech(language)

# Function to play back the recorded audio
def play_audio():
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