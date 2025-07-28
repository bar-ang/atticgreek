import requests
import json
import random

with open("atticgreek.json", "r") as f:
    words = json.load(f)

def format_meaning(meaning):
    return ";  ".join([", ".join(mean) for mean in meaning])

cards = []
for word in words:
    cards.append({
        "front" : word["lemma"],
        "back" : format_meaning(word["meaning"]),
        "tags" : [word["part"], f"unit_{word["unit"]}"]
    })

DECK_NAME = "AtticGreekTAU"
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
    {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": DECK_NAME
        }
    },
    {
        "action": "addNotes",
        "version": 6,
        "params": {
           "notes": random.sample(notes, k=200)
        }
    }
]


for req in requests_to_send:
    response = requests.post('http://localhost:8765', json=req)
    print(response.json())

