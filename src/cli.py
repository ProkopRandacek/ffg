#!/usr/bin/python
import sys
from main import GenBP


def printHelp():
    print("Usage:")
    print("./cli.py internal-item-name amountOfItemsPerSecond")
    print("Example:")
    print("./cli.py military-science-pack 1")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] == "help":
        printHelp()
    else:
        recipe = sys.argv[1]
        amount = 0.0
        try:
            amount = float(sys.argv[2])
        except ValueError:
            print(f'Could not convert "{sys.argv[2]}" to float.')
            exit(1)
        print(GenBP(recipe, amount))
