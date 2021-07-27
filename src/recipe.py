import json

recipes = {}  # recipes
rTimes = {}  # craft times
needFluid = []
fluids = [
    "water",
    "steam",
    "sulfuric-acid",
    "crude-oil",
    "heavy-oil",
    "light-oil",
    "petroleum-gas",
    "lubricant",
]

# parse recipes
# this is bad code TODO
for d in json.loads(open("recipe.json", "r").read()):
    if "normal" in d.keys():
        if "energy_required" in d["normal"]:
            d["energy_required"] = d["normal"]["energy_required"]
    if "ingredients" not in d.keys():
        d["ingredients"] = d["normal"]["ingredients"]
    recipes[d["name"]] = []
    for i in d["ingredients"]:
        if isinstance(i, dict):
            needFluid.append(d["name"])
            recipes[d["name"]] += [[i["name"], i["amount"]]]
        else:
            recipes[d["name"]] += [i]
    if "energy_required" in d.keys(): rTimes[d["name"]] = d["energy_required"]
    else:                             rTimes[d["name"]] = 0.5
