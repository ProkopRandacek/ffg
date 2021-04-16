import json, zlib, base64
from graphviz import Digraph

# parse recipes
recepty = {}
for d in json.loads(open("recipe.json", "r").read()):
    if "ingredients" not in d.keys():
        d["ingredients"] = d["normal"]["ingredients"]
    recepty[d["name"]] = []
    for i in d["ingredients"]:
        if isinstance(i, dict):
            recepty[d["name"]] += [[i["name"], i["amount"]]]
        else:
            recepty[d["name"]] += [i]

recept = []
receptBackwards = []

ignore = ["steel-plate", "iron-plate", "copper-plate"]


# get target recipe tree
def recipeTree(pos, space=""):
    if pos[0] in ignore:
        return
    if pos[0] in recepty.keys():
        print(space + pos[0])
        for i in recepty[pos[0]]:
            recept.append([pos[0], i[0], i[1] * pos[1]])
            recipeTree([i[0], 1], "  " + space)


recipeTree(["locomotive", 1], "- ")
