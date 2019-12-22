
from collections import defaultdict
from itertools import count
from typing import Dict, Tuple

from rwhite_intcode import Intcode

def is_valid(x, y):
    ic = Intcode(data[:])
    ic.run_until_input()
    return  ic.send_multiple(x, y)

data = [int(i) for i in open('day_19.input').read().split(',')]
grid: Dict[Tuple[int, int], int] = defaultdict(int)

cnt = 0
start = 0
for i in count():
    search_range = range(start, 50)
    start = 0
    for j in search_range:
        cnt += 1
        if is_valid(i, j):
            grid[(i, j)] = 1
            if not start:
                start = j
        else:
            if start:
                break
    if i == 49:
        break

print(sum(grid.values()))
cnt = 0
start = 0
for i in count(100):
    for j in count(start):
        cnt += 1
        if is_valid(i, j):
            start = j
            break
    if is_valid(i-99, j+99) and is_valid(i, j):
        break
print((i-99)*10_000 + j)
