#Text To Speech is supported by tts-1 and tts-1-hd model we are using tts-1 here
#6 voice options are there u can explore for {Alloy,Echo,Fable,Onyx,Nova,Shimmer}
# input files supported are of format .mp3 or .mp4
from pathlib import Path
from openai import OpenAI
message="Today is a wonderful day to build something people love!"
def TextToSpeech(message):
  client = OpenAI(
      api_key="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"
  )

  speech_file_path = "/Cohort/Day2/TestSpeech.mp3"
  response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="{}".format(message)
  )
  response.stream_to_file(speech_file_path)