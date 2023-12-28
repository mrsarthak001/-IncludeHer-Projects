#Dalle-3 and Dalle-2 used for image generation 
#Dalle-2 is used to generate variation of pre-existing images
#Dalle-3 is used to generate image from prompt
from openai import OpenAI
message="shoes in umbrella"
def GenerateImage(message):
  client = OpenAI(
      api_key="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"
  )

  response = client.images.generate(
    model="dall-e-3",
    prompt="{}".format(message),
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url
  print(image_url)#this url land to that image when you open it in your browser
GenerateImage(message)