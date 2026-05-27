import json
import time
import requests
import os

import pyttsx3
import pyaudio
import vosk

class Speech:
    def __init__(self):
        self.tts = pyttsx3.init('sapi5')
        # Slow down speech slightly for better clarity
        self.tts.setProperty('rate', 150)

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        # Use first available voice (usually English)
        if len(self.voices) > 0:
            return self.voices[0].id
        return None

    def text2voice(self, speaker=0, text='Ready'):
        voice_id = self.set_voice(speaker)
        if voice_id:
            self.tts.setProperty('voice', voice_id)
        self.tts.say(text)
        self.tts.runAndWait()

class Recognize:
    def __init__(self):
        # Download English model from: https://alphacephei.com/vosk/models
        # Use "vosk-model-small-en-us-0.15" for English
        model = vosk.Model('model_small_en')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']

class JokeAssistant:
    def __init__(self):
        self.url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
        self.current_joke = None
        self.file_name = "jokes.txt"

    def fetch_joke(self):
        response = requests.get(self.url)
        data = response.json()
        self.current_joke = data
        return data

    def get_joke_text(self):
        if not self.current_joke:
            self.fetch_joke()
        
        if self.current_joke['type'] == 'single':
            return self.current_joke['joke']
        else:
            return f"{self.current_joke['setup']} ... {self.current_joke['delivery']}"

    def get_joke_type(self):
        if not self.current_joke:
            self.fetch_joke()
        
        if self.current_joke['type'] == 'single':
            return "single line joke"
        else:
            return "two part joke with setup and delivery"

    def get_category(self):
        if not self.current_joke:
            self.fetch_joke()
        
        category = self.current_joke.get('category', 'Unknown')
        return category

    def read_joke(self):
        joke_text = self.get_joke_text()
        return joke_text

    def save_to_file(self):
        if not self.current_joke:
            self.fetch_joke()
        
        joke_text = self.get_joke_text()
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{joke_text}\n")
            f.write("-" * 40 + "\n")
        
        return f"Joke saved to {self.file_name}"

def speak(text):
    speech = Speech()
    speech.text2voice(speaker=0, text=text)

def main():
    rec = Recognize()
    text_gen = rec.listen()
    assistant = JokeAssistant()
    
    rec.stream.stop_stream()
    speak("Voice assistant started. Say a command")
    time.sleep(0.5)
    rec.stream.start_stream()
    
    print("Assistant started. Say a command...")
    print("Available commands: create, type, category, read, save, help, exit")
    
    for text in text_gen:
        print(f"Recognized: {text}")
        text_lower = text.lower()
        
        if text_lower == 'exit' or text_lower == 'quit' or text_lower == 'goodbye':
            speak("Goodbye!")
            print("Goodbye!")
            quit()
        
        elif 'create' in text_lower or 'new' in text_lower or 'next' in text_lower:
            speak("Creating a new joke")
            assistant.fetch_joke()
            joke_text = assistant.get_joke_text()
            speak(joke_text)
        
        elif 'type' in text_lower:
            joke_type = assistant.get_joke_type()
            speak(f"Joke type: {joke_type}")
        
        elif 'category' in text_lower:
            category = assistant.get_category()
            speak(f"Joke category: {category}")
        
        elif 'read' in text_lower or 'tell' in text_lower:
            joke_text = assistant.read_joke()
            speak(joke_text)
        
        elif 'save' in text_lower or 'write' in text_lower:
            result = assistant.save_to_file()
            speak(result)
        
        elif 'help' in text_lower:
            help_text = "Available commands: create new joke, type, category, read joke, save to file, exit"
            speak(help_text)
        
        else:
            speak("Command not recognized. Say help for list of commands")

if __name__ == '__main__':
    main()