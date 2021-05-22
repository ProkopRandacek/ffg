from recipe import recipes, rTimes, needFluid, fluids
from math import ceil
from place import *
from settings import *

x = 0
foundFluid = False
found6Ingr = ""
lastNumberOfSubstations = 0


def ratioCalc(da, r):
    return ceil(rTimes[r] * da / craftSpeed)


def buildBP(r, y=0, n=0, px=0, space=""):
    global found6Ingr, foundFluid, lastNumberOfSubstations, x  # x is global, no matter how deep down
    myx = x
    if r[0] in recipes.keys():  # only if there is a recipe for this item
        x += 9 + gap  # move to the left

        placeBusLink(-x, y, n)  # Connect to the bus
        placeBusLine(-x, y, n, myx - px)  # Extend the bus line
        assemblerNum = ratioCalc(r[1], r[0])  # calculate how many assemblers we need
        for i in range(assemblerNum):
            placeAssemblerUnit(-x, y + i * 3, r[0])  # place assemblers
        placeBeaconEnd(-x, y + (assemblerNum - 1) * 3)  # place beacons
        numberOfSubstations = int(ceil(assemblerNum * 3 / 18))
        for i in range(numberOfSubstations):
            placeSubstation(-x - 6, y + i * 18)  # place substations
            if useBeacon and i >= lastNumberOfSubstations:
                placeSubstation(-x + 8, y + i * 18)  # place substations

        lastNumberOfSubstations = numberOfSubstations

        nn = 0
        if len(recipes[r[0]]) > 6:
            found6Ingr = r[0]  # 6 ingredients are not supported yet
            return
        manual = []
        for i in recipes[r[0]]:  # loop over all ingredients for this recipe
            if i[0] in ignore:
                manual.append(i[0])  # dont create assemblers for ignored recipes
            elif i[0] in fluids:  # it needs fluid -> manual and create warning
                manual.append(i[0])
                foundFluid = True
            else:  # it is normal recipe that we can create -> recursive call itself on that recipe
                buildBP([i[0], r[1] * i[1]], y + 3, n=nn, px=myx, space="  " + space)
                nn += 1

        wasLastManual = False
        for m in manual:  # manual inputs are connected last
            placeManualInput(-myx - 11, y, nn, m, wasLastManual)
            nn += 1
            wasLastManual = True


def GenBP(item, ips):  # ips = items per second
    global bp, x, foundFluid, found6Ingr
    # reset stuff
    x = 0
    lastNumberOfSubstations = 0
    foundFluid = False
    found6Ingr = ""
    bp.reset()

    buildBP([item, ips])
    errorMsg = ""
    if item not in recipes.keys():
        errorMsg += "I couldn't find this recipe, Is it vanilla?\n"
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
