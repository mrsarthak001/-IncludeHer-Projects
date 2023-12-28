#Basic API Usecase
from openai import OpenAI
client=OpenAI(
    api_key="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"
)
message="Hello how are you"
def openAiCall(message):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": "{}".format(message)
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print(response.choices[0].message.content)
openAiCall(message)