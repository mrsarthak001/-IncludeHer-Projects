#For Speech To Text Conversion model here used is wishper-1
#path is required to send to fnc to transcript speech to text 
from openai import OpenAI
path="Day2\TestSpeech.mp3"
def SpeechtoText(path):
  client = OpenAI(
      api_key="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"
  )

  audio_file= open(path, "rb")
  transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )
  print(transcript)
SpeechtoText(path)