#!/usr/bin/env python3
import sys
import openai

openai.api_key = "ENTER_YOUR_API"

try:
    prompt = sys.argv[1]
except IndexError:
    print('Usage: ais "Your Search Query"') 
    quit()   

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    temperature=0.2
)

print(response["choices"][0]["text"])
