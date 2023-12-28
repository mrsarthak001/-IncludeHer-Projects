# This code is for v1 of the openai package: pypi.org/project/openai
from openai import OpenAI
import os
client=OpenAI(
    #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
    api_key="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"
)
#if user sent such a message which is not relevant as per our customised instructions
#then limit the fnc call and restrict it from sending irrelevant input

#Testing Inputs
# message="tell me command to create a directory named demo"
# message="hello pie"
message="I am just feeling so good about the weather today"
def verifyTheAsk(message):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role":"system",
            "content":"your job is to just give 1 if user is asking for a bash command but if user is asking for anything else just give 0"
        },
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
    output=response.choices[0].message.content
    print(output)
    output=int(output)
    return output
def openAiCall(message):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role":"system",
            "content":"your job is to just give me bash commands nothing else"
        },
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
    output=response.choices[0].message.content
    print(output)
    os.system(output)
if(verifyTheAsk(message)):
    openAiCall(message)
else:
    print("Invalid Input...My job is to just give bash commands nothing else")