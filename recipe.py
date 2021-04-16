import json

recipes = {}
rTimes = {}

# parse recipes
for d in json.loads(open("recipe.json", "r").read()):
    if "ingredients" not in d.keys():
        d["ingredients"] = d["normal"]["ingredients"]
    recipes[d["name"]] = []
    for i in d["ingredients"]:
        if isinstance(i, dict):
            recipes[d["name"]] += [[i["name"], i["amount"]]]
        else:
            recipes[d["name"]] += [i]
    if "energy_required" in d.keys():
        rTimes[d["name"]] = d["energy_required"]
    else:
        rTimes[d["name"]] = 0.5
