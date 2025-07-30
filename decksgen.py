import requests
import json
import sys

# Constants
ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "NOPEAtticGreekTAU_principle_parts"
MODEL_NAME = "Basic"
FRONT_FIELD = "Front"
BACK_FIELD = "Back"

# Load words data
with open("atticgreek.json", "r") as f:
    words = json.load(f)

# Formatting functions
def format_front(word):
    added = f" ({word['added']})" if word["added"] else ""
    if word["rest"] and word["rest"][0]:
        return f"{word['lemma']};  {', '.join(word['rest'])}{added}"
    return word["lemma"] + added

def format_back(word):
    return ";  ".join([", ".join(mean) for mean in word["meaning"]])

def format_verbs_front(word):
    return word["lemma"]

def format_verbs_back(word, num_princ_parts=3):
    assert word["part"] == "v"
    meaning = ";  ".join([", ".join(mean) for mean in word["meaning"]])
    princ_parts = [word["lemma"]] + word["rest"]
    if num_princ_parts and len(princ_parts) > num_princ_parts:
        princ_parts = princ_parts[:num_princ_parts]
    return ", ".join(princ_parts) + "<br>" + meaning

# Prepare cards
verb_cards = []
for word in words:
    if word["part"] == "v":
        verb_cards.append({
            "front": format_verbs_front(word),
            "back": format_verbs_back(word),
            "tags": [f"unit_{word['unit']}"]
        })

# Build notes
notes = []
for card in verb_cards:
    notes.append({
        "deckName": DECK_NAME,
        "modelName": MODEL_NAME,
        "fields": {
            FRONT_FIELD: card["front"],
            BACK_FIELD: card["back"]
        },
        "tags": card["tags"],
        "options": {
            "allowDuplicate": True
        }
    })

# API helper functions
def invoke(action, params=None):
    payload = {"action": action, "version": 6}
    if params:
        payload["params"] = params
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    if response["error"]:
        print(f"Error in action '{action}': {response['error']}")
        sys.exit(-1)
    return response["result"]

# Create deck
print("Creating deck...")
invoke("createDeck", {"deck": DECK_NAME})

# Add notes
print("Adding notes...")
invoke("addNotes", {"notes": notes})
print("All cards added successfully!")

# --- Commented Out: Flagging Cards by Part ---
# The following code is left for future flagging implementation.
# ids = response["result"]
# word_by_id = {word["lemma"]: id for id, word in zip(ids, words)}
# parts = set([word["part"] for word in words])
#
# for i, part in enumerate(parts):
#     words_by_part = [w["lemma"] for w in words if w["part"] == part]
#     for word in words_by_part:
#         req = {
#             "action": "setSpecificValueOfCard",
#             "version": 6,
#             "params": {
#                 "card": word_by_id[word],
#                 "keys": ["flags"],
#                 "newValues": [i+1]
#             }
#         }
#         response = requests.post(ANKI_CONNECT_URL, json=req).json()
#         print(response)
#         if response["error"]:
#             print(f"Failed to set flag {i} for word {word}")
#             sys.exit(-1)
