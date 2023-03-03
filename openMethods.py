import os
import openai
import json
from myconfig import *
import sqlite3
from datetime import date


def getResponse(prompt, user):
    openai.api_key = OPENAI_KEY[0]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=10,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response)
    response_data = extractResponse(json.dumps(response))
    saveResponse(CLIENT_USERNAME[0], prompt, response_data[0], response_data[2], response_data[1])
    return response_data


def extractResponse(json_data):
    data = json.loads(json_data)
    model = data['model']
    response_text = data['choices'][0]['text']
    total_tokens = data['usage']['total_tokens']
    return response_text, model, total_tokens

def saveResponse(user, prompt, response, tokens, model):
    path = 'db/db.sqlite3'
    scriptdir = os.path.dirname(__file__)
    db_path = os.path.join(scriptdir, path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    con = sqlite3.connect(db_path+"responses.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS REQUESTS(DATE, USER, PROMPT, RESPONSE, TOKENS, MODEL)")
    cur.execute(" INSERT INTO REQUESTS VALUES(?, ?, ?,?, ?, ?)",
                (date.today(), user, prompt, response.strip(), tokens, model))
    con.commit()
    con.close()