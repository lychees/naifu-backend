import json
import requests
import sys
from os import system, name, path
import time
from flask import Flask
from flask import request

created = False

if not path.isfile('stats'):
    f = open('stats', 'w+')
    created = True

if not path.isfile('users'):
    f = open('users', 'w+')

if not path.isfile('apikey'):
    f = open('apikey', 'w+')

if created:
    sys.exit(0)

f = open('apikey', 'r')
key = f.read()
f.close()

API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
headers = {"Authorization": key.strip()}

def query(input, temp, max_tokens, use_cache, top_k=None, top_p=1, use_gpu=False, returnseq=1, rep=None):
    payload = {'inputs': input, "parameters": {"temperature": temp, "eos_token_id": 50256,
     "max_new_tokens": max_tokens, "return_full_text": False, "use_cache": use_cache}}
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

app = Flask(__name__)

f= open('users', 'r')
users = f.read().split('\n')
f.close()

@app.route('/novelai/auth', methods=['POST'])
def auth():
    json = request.json
    if json is None:
        return "EmptyBody"

    try:
        if json['user'] in users:
            return json['user']

        else:
            return "AuthFail"
    except:
        return "MissingParameters"

@app.route('/novelai', methods=['POST'])
def generate():
    
    json = request.json
    if json is None:
        return "EmptyBody"

    if json['key'] == 'TVqbkahiIo':
        user = json['user']
        generated_txt = query(json['input'], float(json['temperature']), json['max_gen_tokens'], json['use_cache'])
        generated_txt = generated_txt[0]['generated_text']
        curr_time = time.time()
        f = open('stats', 'r')
        lines = f.readlines()
        f.close()
        inline = False
        for line in lines:
            print(line.split(':')[0])
            if line.split(':')[0] == user:
                inline = True

        if not inline:
            f = open('stats', 'a')
            print('test')
            f.write(user + ":" + str(len(generated_txt)) + "\n")
            f.close()

        else:
            print('test2')
            f = open('stats', "w")
            linenum = 0
            for x in range(0, len(lines)): 
                if user == lines[x].split(':')[0]:
                    lines[x] = user + ":" + str(len(generated_txt) + int(lines[x].split(':')[1])) + "\n"
                    f.writelines(lines)
                    f.close()

        print(time.time() - curr_time)
        return generated_txt
    else:
        return "InvalidKey"

if __name__ == "__main__":
    app.run(debug=False, host="localhost", port=5733)
