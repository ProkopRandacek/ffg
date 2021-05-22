from blueprint import BP
from settings import *

belt = beltType + "transport-belt"
underBelt = beltType + "underground-belt"
bp = BP()


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