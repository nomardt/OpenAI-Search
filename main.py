#!/usr/bin/env python3
import sys
import openai

openai.api_key = "ENTER_YOUR_API"

# Getting prompt
try:
    prompt = sys.argv[1]
except IndexError:
    print('Usage: ais "Your Search Query" [temperature]') 
    quit()   

# Getting the amount of randomness
if len(sys.argv) != 3:
    temp = 0.2
elif sys.argv[2] <= 1 and sys.argv[2] >= 0:
    temp = sys.argv[2]
else:
    print("The amount of randomness can only be between values 0 and 1!")
    temp = 0.2
    
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    temperature=temp
)

print(response["choices"][0]["text"])
