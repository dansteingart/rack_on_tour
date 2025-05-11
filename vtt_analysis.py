##Author: 
##Date Started:
##Notes:

from sqlite_utils import Database
import json
import requests
from pprint import pprint as pp

def chat_with_model(prompt):
    token="OPENWEBUI_token" 
    url="OPENWEBUI_url"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
      "model": "ghack2.gemini-2.0-flash",
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    }
    response = requests.post(url, headers=headers, json=data)
    foo = response.json()['choices'][0]['message']['content']
    txt = ''.join(foo)
    return txt



# Connect to the SQLite database
db = Database("transcriptions.db")
table = db['transcriptions']

debug =False
for row in table.rows: 
    fna = row['filename']
    foo = table.get(fna)
    fmc = foo['five_m_chunks']
    if debug: print(fmc)
    if fmc == None:
        clean = foo['clean_transcript']
        resp = chat_with_model(f"provide a detailed summary in 5 minute increments where the included timestamps at the beginning of the lines are minutes and fractions thereof from the start of the conversaion in x.xx format :\n {clean}")        
        table.update(row['filename'], {"five_m_chunks": resp})

    foo = table.get(fna)
    smy = foo['summary']
    if debug: print(smy)
    if smy == None:
        fivem = foo['five_m_chunks']
        resp = chat_with_model(f"please provide 4 detailed summary parapgraphs of this. Then list any action items:\n {fivem}")        
        table.update(row['filename'], {"summary": resp})

    foo = table.get(fna)
    onl = foo['oneline']
    if debug: print(onl)
    if onl == None:
        summary = foo['summary']
        resp = chat_with_model(f"one line (50 chars is) summary with a fun emoji if possible:\n {summary}")        
        print(resp)
        table.update(row['filename'], {"oneline": resp},alter=True)

    if debug: break