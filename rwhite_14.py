from collections import defaultdict
from typing import Dict, Tuple, List
import math

Element = Tuple[int, str]

data = open('day_14.input').read().split('\n')

ORE = 'ORE'
FUEL = 'FUEL'
reactions: Dict[str, Tuple[List[Element], Element]] = {}
for line in data:
    ing, out = line.split(" => ")
    ings = ing.split(", ")
    ingrediants = [(int(a), b) for ing in ings for a, b in [ing.split()]]
    q, out = out.split()
    reactions[out] = (ingrediants, (int(q), out))


def get_ore_count(fuel_amount):
    required: Dict[str, int] = defaultdict(int)
    required[FUEL] += fuel_amount
    # Keep rolling until only ORE has positive values.
    while any(v > 0 and k != ORE for k, v in required.items()):
        # Get the next non-ORE positive element, and how much we need of it.
        ing, ing_quant = next((k, v) for k, v in required.items() if v > 0 and k != ORE)
        out_quant = reactions[ing][-1][0]
        quant = math.ceil(ing_quant / out_quant)
        required[ing] -= quant * out_quant
        for new_quant, new_ing in reactions[ing][0]:
            required[new_ing] += (new_quant * quant) # This is where I was messing up last time, need to keep a running tally of each required element.
    return required[ORE]

print(get_ore_count(1))
lower = 3000000
upper = 4000000
# These numbers will probably be different depending on your input, I just wanted to narrow the search for myself
assert get_ore_count(lower) // 1_000_000_000_000 == 0 # Bunch of manual searches to find a lower bound
assert get_ore_count(upper) // 1_000_000_000_000 == 1 # Bunch of manual searches to find an upper bound

# Binary search
while lower < upper:
    count = get_ore_count((mid := (lower + upper) // 2))
    if count > 1_000_000_000_000:
        upper = mid -1
    else:
        lower = mid
print(lower)
