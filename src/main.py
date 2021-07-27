from recipe import recipes, rTimes, needFluid, fluids
from math import ceil
from place import *
from settings import *

x = 0 # x needs to be global since it changes with each call
lastNumberOfSubstations = 0

def die(reason):
    print("ERROR: " + reason)
    exit(1)

def ratioCalc(da, r):
    return ceil(rTimes[r] * da / craftSpeed)


# recipe
# ips = items per second that this recipe needs to have
# y = y offset to build with
# n = what belt to connect to on the local bus
# px = upper recursion level x (we need to know how long the bus line needs to be)
def build(recipe, ips, y=0, n=0, px=0): 
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
    bp.reset()

    build(item, ips)
    errorMsg = ""
    if item not in recipes.keys():
        errorMsg += "I couldn't find this recipe, Is it vanilla?\n"

    return bp.export()


if __name__ == "__main__":
    print("Run the cli.py script for cli interface")
