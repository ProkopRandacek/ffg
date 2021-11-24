import json

recipes = {}
craft_times = {}
need_fluid = set()  # all items that need a fluid to be crafted
item_names = set()  # all item names
fluids = set(["water", "crude-oil", "petroleum-gas", "light-oil", "heavy-oil", "lubricant", "sulfuric-acid", "steam"])

# parse recipes
for d in json.loads(open("recipe.json", "r").read()):
    # expensive vs normal recipe handling
    # just takes the `normal` variant if it finds one
    if "normal" in d.keys():
        d["ingredients"] = d["normal"]["ingredients"]
        if "energy_required" in d["normal"]:
            d["energy_required"] = d["normal"]["energy_required"]

    item_names.add(d["name"])

    recipes[d["name"]] = []
    for i in d["ingredients"]:
        if isinstance(i, dict):
            need_fluid.add(d["name"])
            recipes[d["name"]] += [[i["name"], i["amount"]]]
        else:
            recipes[d["name"]] += [i]

    if "energy_required" in d.keys():
        craft_times[d["name"]] = d["energy_required"]
    else:                           
        craft_times[d["name"]] = 0.5

