from blueprint import BP
from recipe import recipes, rTimes
from math import ceil

ignore = ["stone-brick", "steel-plate", "iron-plate", "copper-plate"]
bp = BP()
x = 0
foundFluid = False
found3Ingr = ""


def placeAssemblerUnit(x, y, recipe):
    global bp
    bp.addEntity("assembling-machine-3", x, y, recipe=recipe)
    bp.addEntity("stack-inserter", x - 2, y - 1, direction=6)
    bp.addEntity("stack-inserter", x + 2, y - 0, direction=6)
    bp.addEntity("long-handed-inserter", x - 2, y - 0, direction=6)
    bp.addEntity("long-handed-inserter", x - 2, y + 1, direction=6)
    bp.addEntity("long-handed-inserter", x - 3, y + 1, direction=6)
    for i in range(2):  # outer two input lines
        for j in range(3):
            bp.addEntity("express-transport-belt", x - 5 + i, y - 1 + j, direction=4)
    for i in range(3):  # output line
        bp.addEntity("express-transport-belt", x + 3, y - 1 + i, direction=0)
    bp.addEntity("express-underground-belt", x - 3, y - 1, direction=4, type="output")
    bp.addEntity("express-underground-belt", x - 3, y + 0, direction=4, type="input")


def placeBusLink(x, y, n):
    global bp
    for i in range(3):  # the input lines with the curve
        for j in range(5):
            if i + j < 6:
                bp.addEntity(
                    "express-transport-belt",
                    x - 5 + i,
                    y - 6 + j,
                    direction=4 if i + j > 1 else 3,
                    # this curves the belts from the bus
                )
            else:  # there is that one underground input at the start
                bp.addEntity(
                    "express-underground-belt",
                    x - 5 + i,
                    y - 6 + j,
                    direction=4,
                    type="input",
                )
    for i in range(2, n + 7):  # the output line link
        bp.addEntity("express-transport-belt", x + 3, y - i, direction=0)
    bp.addEntity("express-transport-belt", x + 3, y - n - 7, direction=3)


def placeBusLine(x, y, n, l):
    global bp
    if l < 11:
        return
    for i in range(1, l - 8):
        bp.addEntity("express-transport-belt", x + 3 + i, y - n - 7, direction=3)


def ratioCalc(da, r):
    return ceil(rTimes[r] * da / 1.25)


def buildBP(r, y=0, n=0, px=0, space=""):
    global found3Ingr, x  # x is global, no matter how deep down
    myx = x
    if r[0] in recipes.keys():  # only if there is a recipe for this item
        x += 11  # move to the left
        placeBusLink(-x, y, n)  # place entities into the blueprint
        placeBusLine(-x, y, n, myx - px)
        for i in range(ratioCalc(r[1], r[0])):
            placeAssemblerUnit(-x, y + i * 3, r[0])
        # print(space + r[0], "\t -", ratioCalc(r[1], r[0]), x, y, n, myx - px)
        nn = 0
        if len(recipes[r[0]]) > 3:
            found3Ingr = r[0]  # 3 ingredients are not supported yet
            return
        for i in recipes[r[0]]:  # loop over all ingredients for this recipe
            if i[0] in ignore:
                continue
            buildBP([i[0], r[1] * i[1]], y + 3, n=nn, px=myx, space="  " + space)
            nn += 1


def GenBP(item, ips):
    global bp, x, foundFluid, found3Ingr
    # reset stuff
    x = 0
    foundFluid = False
    found3Ingr = ""
    bp.reset()

    buildBP([item, ips])
    errorMsg = ""
    if item not in recipes.keys():
        errorMsg += "I couldn't find this recipe, Is it vanilla?\n"
        errorMsg += "Mod support is planned eventually"
    if foundFluid:
        errorMsg += "I found a recipe with fluid. Those are not yet supported.\n"
        errorMsg += (
            "I created the blueprint anyway but you should check it for errors.\n"
        )
    if found3Ingr != "":
        errorMsg += "I found a recipe with more than 3 ingredients.\n"
        errorMsg += "I can't create a Blueprint for those yet :(\n"
        errorMsg += "recipe with more than 3 ingredients: " + found3Ingr

    return [bp.export(), errorMsg]


if __name__ == "__main__":
    print("\n".join(GenBP("military-science-pack"), 1))
