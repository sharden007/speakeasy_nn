# mic_check.py
import speech_recognition as sr

def list_microphones():
    mic_list = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mic_list):
        print(f"Microphone '{name}' found for `Microphone(device_index={index})`")
    return mic_list

if __name__ == '__main__':
    list_microphones()