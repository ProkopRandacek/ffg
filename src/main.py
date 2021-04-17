from blueprint import BP
from recipe import recipes, rTimes, needFluid, fluids
from math import ceil

# settings
ignore = ["stone-brick", "steel-plate", "iron-plate", "copper-plate", "coal"]
gap = 5  # min 2
beltType = "express-"  # "" or "fast-" or "express-"
assembler = "assembling-machine-3"
inserter = "stack-inserter"
longInserter = "long-handed-inserter"
useBeacon = True  # gap min 3
assemblerMod = "speed-module-3"
assemblerModNum = 4
module = "speed-module"
craftSpeed = 1.25  # The craft speed of the assembler including the modules and beacons
# end of settings

belt = beltType + "transport-belt"
underBelt = beltType + "underground-belt"
bp = BP()
x = 0
foundFluid = False
found6Ingr = ""


def placeAssemblerUnit(x, y, r):
    bp.addEntity(
        assembler,
        x,
        y,
        recipe=r,
        mod=assemblerMod,
        mnum=assemblerModNum,
    )
    bp.addEntity(inserter, x - 2, y - 1, direction=6)
    bp.addEntity(inserter, x + 2, y - 0, direction=6)
    bp.addEntity(longInserter, x - 2, y - 0, direction=6)
    bp.addEntity(longInserter, x - 2, y + 1, direction=6)
    bp.addEntity(longInserter, x - 3, y + 1, direction=6)
    for i in range(2):  # outer two input lines
        for j in range(3):
            bp.addEntity(belt, x - 5 + i, y - 1 + j, direction=4)
    for i in range(3):  # output line
        bp.addEntity(belt, x + 3, y - 1 + i, direction=0)
    bp.addEntity(underBelt, x - 3, y - 1, direction=4, type="output")
    bp.addEntity(underBelt, x - 3, y + 0, direction=4, type="input")

    if useBeacon:
        bp.addEntity("beacon", x + 5, y - 4, mod=module, mnum=2)


def placeBeaconEnd(x, y):
    if useBeacon:
        bp.addEntity("beacon", x + 5, y - 1, mod=module, mnum=2)
        bp.addEntity("beacon", x + 5, y + 2, mod=module, mnum=2)
        bp.addEntity("beacon", x + 5, y + 5, mod=module, mnum=2)


def placeBusLink(x, y, n):
    for i in range(3):  # the input lines with the curve
        for j in range(5):
            if i + j < 6:
                bp.addEntity(
                    belt,
                    x - 5 + i,
                    y - 6 + j,
                    direction=4 if i + j > 1 else 3,
                    # this curves the belts from the bus
                )
            else:  # there is that one underground input at the start
                bp.addEntity(
                    underBelt,
                    x - 5 + i,
                    y - 6 + j,
                    direction=4,
                    type="input",
                )
    if n in [0, 2, 4]:  # the output line link
        n = int(n / 2)
        for i in range(2, n + 7):
            bp.addEntity(belt, x + 3, y - i, direction=0)
        bp.addEntity(belt, x + 3, y - n - 7, direction=3)
        bp.addEntity(belt, x + 2, y - n - 7, direction=3)
    else:
        for i in range(2, n + 3):
            bp.addEntity(belt, x + 3, y - i, direction=0)
        bp.addEntity(belt, x + 2, y - n - 3, direction=1)
        bp.addEntity(belt, x + 2, y - n - 4, direction=1)
        bp.addEntity(belt, x + 2, y - n - 5, direction=2)

        bp.addEntity(belt, x + 3, y - n - 4, direction=1)
        bp.addEntity(belt, x + 3, y - n - 5, direction=1)
        bp.addEntity(belt, x + 3, y - n - 6, direction=2)

        bp.addEntity(belt, x + 3, y - n - 3, direction=6)


def placeBusLine(x, y, n, l):
    if n in [1, 3, 5]:
        l -= gap + 2
    n = int(n / 2)

    for i in range(0, l - 9):
        bp.addEntity(belt, x + 4 + i, y - n - 7, direction=3)


def placeManualInput(x, y, n, r, wasLastManual):
    bp.addEntity(
        "constant-combinator",
        x - (4 if n in [0, 2, 4] else (5 if wasLastManual else 6 + gap)) - gap,
        y - 4 - int(n / 2),
        direction=2,
        ccitem=r,
    )


def placeSubstation(x, y):
    global lastSub
    bp.addEntity("substation", x, y)


def ratioCalc(da, r):
    return ceil(rTimes[r] * da / craftSpeed)


def buildBP(r, y=0, n=0, px=0, space=""):
    global found6Ingr, foundFluid, x  # x is global, no matter how deep down
    myx = x
    if r[0] in recipes.keys():  # only if there is a recipe for this item
        x += 9 + gap  # move to the left
        placeBusLink(-x, y, n)  # place entities into the blueprint
        placeBusLine(-x, y, n, myx - px)
        assemblerNum = ratioCalc(r[1], r[0])
        for i in range(assemblerNum):
            placeAssemblerUnit(-x, y + i * 3, r[0])
        placeBeaconEnd(-x, y + (assemblerNum - 1) * 3)
        for i in range(int(ceil(assemblerNum * 3 / 18))):
            placeSubstation(-x - 6, y + i * 18)
        # print(space + r[0], "\t -", ratioCalc(r[1], r[0]), x, y, n, myx - px)
        nn = 0
        if len(recipes[r[0]]) > 6:
            found6Ingr = r[0]  # 3 ingredients are not supported yet
            return
        manual = []
        for i in recipes[r[0]]:  # loop over all ingredients for this recipe
            if i[0] in ignore:
                manual.append(i[0])
            elif i[0] in fluids:  # needFluid:
                manual.append(i[0])
                foundFluid = True
            else:
                buildBP([i[0], r[1] * i[1]], y + 3, n=nn, px=myx, space="  " + space)
                nn += 1
        wasLastManual = False
        for m in manual:  # manual inputs are connected last
            placeManualInput(-myx - 11, y, nn, m, wasLastManual)
            nn += 1
            wasLastManual = True


def GenBP(item, ips):
    global bp, x, foundFluid, found6Ingr
    # reset stuff
    x = 0
    foundFluid = False
    found6Ingr = ""
    bp.reset()

    buildBP([item, ips])
    errorMsg = ""
    if item not in recipes.keys():
        errorMsg += "I couldn't find this recipe, Is it vanilla?\n"
        errorMsg += "Mod support is planned eventually"
    if foundFluid:
        errorMsg += "I found a recipe with fluid. Those are not yet supported.\n"
        errorMsg += "I created the factory anyway"
    if found6Ingr != "":
        errorMsg += "I found a recipe with more than 6 ingredients.\n"
        errorMsg += "I can't create a factory for those yet :(\n"
        errorMsg += "recipe with more than 6 ingredients: " + found6Ingr

    return [bp.export(), errorMsg]


if __name__ == "__main__":
    print("\n".join(GenBP("military-science-pack", 1)))
