import json

with open("atticgreek_raw.json", "r") as f:
    words = json.load(f)


new = []
for word in words:
    word["rest"] = word["rest"].split(",")
    word["rest"] = [t.strip() for t in word["rest"]]

    word["meaning"] = [t.split(",") for t in word["meaning"].split(";")]
    word["meaning"] = [[d.strip() for d in t] for t in word["meaning"]]

    if word["part"] == "n":
       gender = ""

       for g in ["m", "f", "n"]:
           if g in word["added"]:
               gender += g

       word["added"] = gender
       print(word["added"])
    new.append(word)

with open("atticgreek.json", "w") as f:
    json.dump(new, f, ensure_ascii=False, indent=4)
