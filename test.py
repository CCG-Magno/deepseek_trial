from dataclasses import dataclass
import enum
from typing import List

from dotenv import load_dotenv, dotenv_values
import os
from openai import OpenAI

load_dotenv()

class Role(enum.StrEnum):
    Assistant = "assistant"
    User = "user"
    System = "system"

@dataclass
class Message:
    role: Role 
    content: str
    
    def as_dict(self):
        return { "user": self.role.value, "content": self.content }

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), 
                base_url="https://api.deepseek.com/v1")

messages= []

system_prompts = [
    {
        "role": "system",#Role.System.value,
        "content": "You are a university professor assistant"
    },
]

#response = client.chat.completions.create(
#    model="deepseek-chat",
#    messages=[
#        {"role": "system", "content": "You are a helpful assistant"},
#        {"role": "user", "content": "Hello"},
#    ],
#    stream=False
#)

while True:
    msg = input(">>>")
    #m = Message(role=Role.User, content=msg)
    messages.append({
        "role": "user",
        "content": msg,
    })
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages= messages,
    )
    print(response.choices[0].message)
    messages.append({
        "role":"system", 
        "content": response.choices[0].message
    })
    print(f"Messages Round 1: {messages}")
    #print(response.choices[0].message.content)
