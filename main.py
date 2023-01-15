import sys
import openai

openai.api_key = "ENTER YOUR API KEY HERE"

try:
    prompt = sys.argv[1]
except IndexError:
    print('Usage: opai "Your Search Query"')    

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    temperature=0
)

print(response["choices"][0]["text"])