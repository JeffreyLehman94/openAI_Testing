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
    response_data = extractResponse(json.dumps(response))
    saveResponse(user, prompt, response_data[0], response_data[2], response_data[1])
    return response_data[0]


def extractResponse(json_data):
    data = json.loads(json_data)
    model = data['model']
    response_text = data['choices'][0]['text']
    prompt_tokens = data['usage']['prompt_tokens']
    completion_tokens = data['usage']['completion_tokens']
    total_tokens = data['usage']['total_tokens']
    return response_text, model, total_tokens


def saveResponse(user, prompt, response, tokens, model):
    con = sqlite3.connect("responses.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS REQUESTS(DATE, USER, PROMPT, RESPONSE, TOKENS, MODEL)")
    cur.execute(" INSERT INTO REQUESTS VALUES(?, ?, ?,?, ?, ?)",
                (date.today(), user, prompt, response.strip(), tokens, model))
    con.commit()
    con.close()
