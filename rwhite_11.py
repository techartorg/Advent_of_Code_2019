
from operator import add, mul, lt, eq
from collections import defaultdict
from functools import wraps
from typing import List, Dict
from rwhite_intcode import Intcode

data = [int(v) for v in open('day_11.input').read().split(',')]

def run_robot(data: List[int], start_val=0) -> Dict[complex, int]:
    bot = Intcode(data[:])
    bot.run_until_input()
    grid: Dict[complex, int] = defaultdict(int)
    pos = 0j
    facing = 1j
    grid[pos] = start_val
    while True:
        try:
            i = grid[pos]
            grid[pos] = bot.send(i)
            facing *= -1j if bot.send(i) else 1j
            pos += facing
            next(bot)
        except StopIteration:
            break
    return grid
print(len(run_robot(data[:])))

grid = run_robot(data[:], 1)
xmin, *_, xmax = sorted(int(v.real) for v in grid)
ymin, *_, ymax = sorted(int(abs(v.imag)) for v in grid)
# Need to padd out the grid, otherwise you chop off the bottom part and get confused
print('\n'.join(''.join('#' if grid[x - 1j *y] else ' ' for x in range(xmin-1, xmax+2)) for y in range(ymin-1, ymax+2)))