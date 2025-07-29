import requests
import json
import random
import sys

with open("atticgreek.json", "r") as f:
    words = json.load(f)

#words = random.sample(words, k = 80) # FOR DEBUG!

def format_front(word): 
    added = ""
    if word["added"]:
        added = f" ({word['added']})"
    if word["rest"] and word["rest"][0]:
        return f"{word["lemma"]};  {", ".join(word["rest"])}{added}"
    else:
        return word["lemma"] + added

def format_back(word):
    return ";  ".join([", ".join(mean) for mean in word["meaning"]])    

cards = []
for word in words:
    cards.append({
        "front" : format_front(word),
        "back" : format_back(word),
        "tags" : [word["part"], f"unit_{word["unit"]}"]
        
    })

DECK_NAME = "AtticGreekTAU_extended"
MODEL_NAME = "Basic"
FRONT = "Front"
BACK = "Back"

notes = []
for card in cards:
    notes.append({
        "deckName": DECK_NAME,
        "modelName": MODEL_NAME,
        "fields": {
            FRONT: card["front"],
            BACK: card["back"]
        },
        "tags": card["tags"],
        "options": {
             "allowDuplicate": True
        }
    })

requests_to_send = [
    {
        "action": "modelNames",
        "version": 6
    },
]

req = {
    "action": "createDeck",
    "version": 6,
    "params": {
        "deck": DECK_NAME
    }
}

response = requests.post('http://localhost:8765', json=req).json()
print(response)
if response["error"]:
    print(f"FAILED TO MAKE DECK")
    sys.exit(-1)

req = {
    "action": "addNotes",
    "version": 6,
    "params": {
        "notes": notes
    }
}
response = requests.post('http://localhost:8765', json=req).json()
print("ALL CARDS ADDED!")
if response["error"]:
    print(response["error"])
    print(f"FAILED TO ADD CARDS")
    sys.exit(-1)



    
