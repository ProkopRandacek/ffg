from recipe import recipes, craft_times, need_fluid, fluids
from math import ceil
from blueprint import BP
from settings import *

belt = beltType + "transport-belt"
underBelt = beltType + "underground-belt"
bp = BP()

x = 0 # x needs to be global since it changes with each call
lastNumberOfSubstations = 0

def die(reason):
    print("ERROR: " + reason)
    exit(1)


def ratioCalc(da, r):
    return ceil(craft_times[r] * da / craftSpeed)


def placeAssemblerUnit(x, y, r):
    bp.addEntity(
        assembler,
        x, y,
        recipe=r,
        mod=assemblerMod,
        mnum=assemblerModNum,
    )
    bp.addEntity(inserter,     x - 2, y - 1, direction=6)
    bp.addEntity(inserter,     x + 2, y - 0, direction=6)
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
    bp.addEntity("beacon", x + 5, y - 1, mod=module, mnum=2)
    bp.addEntity("beacon", x + 5, y + 2, mod=module, mnum=2)
    bp.addEntity("beacon", x + 5, y + 5, mod=module, mnum=2)


def placeBusLink(x, y, n):
    bp.addEntity(belt, x - 5, y - 6, direction=3)
    bp.addEntity(belt, x - 4, y - 6, direction=3)
    bp.addEntity(belt, x - 3, y - 6, direction=4)
    bp.addEntity(belt, x - 5, y - 5, direction=3)
    bp.addEntity(belt, x - 4, y - 5, direction=4)
    bp.addEntity(belt, x - 3, y - 5, direction=4)
    bp.addEntity(belt, x - 5, y - 4, direction=4)
    bp.addEntity(belt, x - 4, y - 4, direction=4)
    bp.addEntity(belt, x - 3, y - 4, direction=4)
    bp.addEntity(belt, x - 5, y - 3, direction=4)
    bp.addEntity(belt, x - 4, y - 3, direction=4)
    bp.addEntity(belt, x - 3, y - 3, direction=4)
    bp.addEntity(belt, x - 5, y - 2, direction=4)
    bp.addEntity(belt, x - 4, y - 2, direction=4)
    bp.addEntity(underBelt, x - 3, y - 2, direction=4, type="input")

    # the output line link
    if n in [0, 2, 4]: # to the lower line
        n = int(n / 2)
        for i in range(2, n + 7):
            bp.addEntity(belt, x + 3, y - i, direction=0)
        bp.addEntity(belt, x + 3, y - n - 7, direction=3)
        bp.addEntity(belt, x + 2, y - n - 7, direction=3)
    else: # to the upper line
        n = int(n / 2) + 1
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
    bp.addEntity("substation", x, y)

# recipe
# ips = items per second that this recipe needs to have
# y = y offset to build with
# n = what belt to connect to on the local bus
# px = upper recursion level x (we need to know how long the bus line needs to be)
def build(recipe, ips, y=0, n=0, px=0) -> None: 
    global lastNumberOfSubstations, x
    myx = x # my x is given to the lower recursion level
    if recipe in recipes.keys():  # only if there is a recipe for this item
        x += 9 + gap  # move to the left


        # === BUS ===
        placeBusLink(-x, y, n)  # Connect to the bus
        placeBusLine(-x, y, n, myx - px)  # Extend the bus line


        # === ASSEMBLER ===
        assemblerNum = ratioCalc(ips, recipe)
        for i in range(assemblerNum):
            placeAssemblerUnit(-x, y + i * 3, recipe) # beacons are placed from this function (if enabled)


        # === BEACON ===
        if useBeacon:
            placeBeaconEnd(-x, y + (assemblerNum - 1) * 3) # place those 3 beacons at the end


        # === SUBSTATIONS ===
        numberOfSubstations = int(ceil(assemblerNum * 3 / 18)) + 1
        for i in range(numberOfSubstations):
            placeSubstation(-x - 6, y + i * 18)
            if useBeacon and i >= lastNumberOfSubstations:
                placeSubstation(-x + 8, y + i * 18 - 3)
        lastNumberOfSubstations = numberOfSubstations


        # === CREATE INPUTS ===
        if len(recipes[recipe]) > 6: die("I found a recipe with more than 6 ingredients.")

        inputs = []
        manual = []  # the manual input belts

        for i in recipes[recipe]:  # loop over all ingredients for this recipe
            if   i[0] in ignore: manual.append(i[0])
            elif i[0] in fluids: manual.append(i[0])
            else:  # it is normal recipe that we can create -> recursive call itself on that recipe
                requiredIPS = ips * i[1]
                while requiredIPS > 0:
                    thisBeltIPS = min(singleLineIPS, requiredIPS)
                    requiredIPS -= thisBeltIPS

                    inputs.append((i[0], thisBeltIPS))

        # === RECURSIVE CALL ===
        if (len(manual) + len(inputs)) > 6: die(f"{recipe} requires more ingredients that I can fit on 3 belts.")
        belt = 0  # what bus line the lower recursion is supposed to connect to
        for i in sorted(inputs, key=lambda x: x[1]):
            build(i[0], i[1], y + 3, n=belt, px=myx)
            belt += 1

        # === CREATE MANUAL INPUT INDICATORS ===
        wasLastManual = False
        for m in manual:
            placeManualInput(-myx - 11, y, belt, m, wasLastManual)
            belt += 1
            wasLastManual = True


def GenBP(item, ips):  # ips = items per second
    global bp, x, lastNumberOfSubstations
    # reset global variables
    x = 0
    lastNumberOfSubstations = 0
    bp = BP()

    build(item, ips)

    return bp.export()


if __name__ == "__main__":
    print("Run the cli.py script for cli interface")

