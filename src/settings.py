def die(reason):
    print("ERROR: " + reason)
    exit(1)

ignore = ["stone-brick", "steel-plate", "iron-plate", "copper-plate", "coal"]
ignore += ["plastic-bar"]

gap = 0
beltLevel = 2  # 0, 1 or 2
assemblerLevel = 2  # 0, 1 or 2
useBeacon = False # TODO calculate craft time

inserter = "fast-inserter"
longInserter = "long-handed-inserter"

assemblerMod = "" # TODO productivity support
assemblerModNum = 4
module = "speed-module"  # module for beacons


if   assemblerLevel == 0: assembler, craftSpeed = "assembling-machine-1", 0.50
elif assemblerLevel == 1: assembler, craftSpeed = "assembling-machine-2", 0.75
elif assemblerLevel == 2: assembler, craftSpeed = "assembling-machine-3", 1.25
else: die(f"'{assemblerLevel}' is not a valid value for assemblerLevel")

if   assemblerMod == "speed-module":          craftSpeed *= (1.0 + ( 0.2 * assemblerModNum))
elif assemblerMod == "speed-module-2":        craftSpeed *= (1.0 + ( 0.3 * assemblerModNum))
elif assemblerMod == "speed-module-3":        craftSpeed *= (1.0 + ( 0.5 * assemblerModNum))
#elif assemblerMod == "productivity-module":   craftSpeed *= (1.0 + (-0.05 * assemblerModNum))
#elif assemblerMod == "productivity-module-2": craftSpeed *= (1.0 + (-0.10 * assemblerModNum))
#elif assemblerMod == "productivity-module-3": craftSpeed *= (1.0 + (-0.15 * assemblerModNum))
elif assemblerMod == "effectivity-module":   pass
elif assemblerMod == "effectivity-module-2": pass
elif assemblerMod == "effectivity-module-3": pass
elif assemblerMod == "": pass
else: die(f"'{assemblerMod}' is not a valid value for assemblerMod")

if   beltLevel == 0: beltType, singleLineIPS = ""        ,  7.5
elif beltLevel == 1: beltType, singleLineIPS = "fast-"   , 15.0
elif beltLevel == 2: beltType, singleLineIPS = "express-", 22.5
else: die(f"'{beltLevel}' is not a valid value for beltLevel")

gap += 2
if useBeacon: gap += 3 # beacons are 3 wide
