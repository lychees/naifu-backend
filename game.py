import json
import requests
import sys
from os import system, name 
import time

text = ""
system('cls')
while 1:
    ink = input()
    if input is not None:
        text = text + ink

    user = "kurumuz"
    json = {"input": text, "temperature": 1, "max_gen_tokens": 100, "use_cache": False, "user": user, "key": "TVqbkahiIo"}
    text = text + requests.post('http://127.0.0.1:5000/apicall', json=json).text
    system('cls')
    print(text)