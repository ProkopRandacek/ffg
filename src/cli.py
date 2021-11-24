#!/usr/bin/python
import sys, argparse, difflib
from main import GenBP
from settings import gap, assemblerLevel, useBeacon
from recipe import item_names

def uint(s): # positive number check for the --gap argument
    try:
        v = int(s)
        if v < 0: raise ValueError
        else: return v
    except ValueError:
        raise ValueError

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Factorio factory generator")
    parser.add_argument('item'  , type=str  , help='The item you want a factory for')
    parser.add_argument('amount', type=float, help='How many items per second do you want')
    parser.add_argument('-a', '--asmLevel' , default=3, type=int,  help="What assembler level to use.", choices=range(1, 4))
    parser.add_argument('-b', '--beltLevel', default=3, type=int,  help="What belt level to use."     , choices=range(1, 4))
    parser.add_argument('-g', '--gap'      , default=0, type=uint, help="Width of the gap between assembler lines")
    parser.add_argument('-u', '--useBeacon', action='store_true',  help="Place beacons next to the assemblers")
    args = parser.parse_args()

    recipe = args.item
    amount = args.amount

    if recipe not in item_names:
        print(f"'{recipe}' is not a valid item name")
        close = difflib.get_close_matches(recipe, item_names)
        if len(close) > 0:
            print(f"Did you mean {close[0]}?")
        exit(1)

    if amount <= 0:
        print(f"amount cannot be negative '{amount}'")
        exit(1)

    print(GenBP(recipe, amount))

