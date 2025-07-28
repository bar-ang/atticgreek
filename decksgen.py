import requests
import json

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
        "action": "addNote",
        "version": 6,
        "params": {
           "note": {
                "deckName": DECK_NAME,
                "modelName": "בסיסי",
                "fields": {
                    "Front": "SOCRATES",
                    "Back": "He who knows that he knows nothing"
                },
                "tags": [
                    "cool_guy"
                ]
            }
        }
    }
]


for req in requests_to_send:
# Send to AnkiConnect
    response = requests.post('http://localhost:8765', json=req)
    print(response.json())

