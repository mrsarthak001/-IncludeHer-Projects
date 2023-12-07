import openai
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import tempfile
import pyttsx3
class VoiceAssistant:
    """
    This class represents a voice assistant.
    
    Attributes:
        history (list): A list of dictionaries representing the assistant's history.
        
    Methods:
        listen: Records audio from the user and transcribes it.
        think: Generates a response to the user's input.
        speak: Converts text to speech and plays it.
    """
    def __init__(self):
        # Set your OpenAI API key
        openai.api_key = ""
        # Initialize the assistant's history
        self.history = [
                {"role": "system", "content": "You are a helpful assistant. The user is english. Only speak english."}
            ]
        
    def listen(self):
        """
        Records audio from the user and transcribes it.
        """
        print("Listening...")
        # Record the audio
        duration = 3  # Record for 3 seconds
        fs = 44100  # Sample rate

        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
        sd.wait()

        # Save the NumPy array to a temporary wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
            wavfile.write(temp_wav_file.name, fs, audio)

            # Use the temporary wav file in the OpenAI API
            transcript = openai.Audio.transcribe("whisper-1", temp_wav_file)

        print(f"User: {transcript['text']}")
        return transcript['text']

    def think(self, text):
        """
        Generates a response to the user's input.
        """
        # Add the user's input to the assistant's history
        self.history.append({"role": "user", "content": text})
        # Send the conversation to the GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            temperature=0.5
        )
        # Extract the assistant's response from the API response
        message = dict(response.choices[0])['message']['content']
        self.history.append({"role": "system", "content": message})
        print('Assistant: ', message)
        return message

    def speak(self, text):
        """"
        Converts text to speech and plays it.
        """
        # Initialize the speech engine
        engine = pyttsx3.init()

        # Convert text to speech
        engine.say(text)

        # Block while processing all currently queued commands
        engine.runAndWait()


if __name__ == "__main__":
    assistant = VoiceAssistant()

    while True:
        text = assistant.listen()

        if "goodbye" in text.strip().lower():
            print("Assistant: Goodbye! Have a great day!")
            assistant.speak("Goodbye! Have a great day!")
            break
        
        response = assistant.think(text)
        assistant.speak(response)
