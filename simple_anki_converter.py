import csv
import json

with open("atticgreek.json", "r") as f:
    words = json.load(f)

def format_meaning(meaning):
    return ";  ".join([", ".join(mean) for mean in meaning])

cards = []
for word in words:
    cards.append((word["lemma"], format_meaning(word["meaning"])))

with open('anki_atticgreek.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Front', 'Back'])  # Header
    writer.writerows(cards)

