from __future__ import annotations
from collections import defaultdict
from typing import Dict
data = open('day_03.input').read().split('\n')


offsets = {
    'R': 1,
    'L': -1,
    'U': 1j,
    'D': -1j,
}

# So the idea is that we store the position, and the number of steps it took for a wire to get to that position
# Each wire's steps get stored in the sub dictionary, and we can identify intersections based on having multiple
# values in that dictionary.
grid: Dict[complex, Dict[int, int]] = defaultdict(dict)
for idx, wire in enumerate(data):
    steps = 0
    position = 0j
    for move in wire.split(','):
        offset = offsets[move[0]]
        distance = int(move[1:])
        for _ in range(distance):
            steps += 1
            position += offset
            # Using setdefault because we don't want to overright a spot with a higher step count, as we care
            # only about the first time we hit a location.
            grid[position].setdefault(idx, steps)

print(min(abs(p.real) + abs(p.imag) for p, v in grid.items() if len(v) == 2))
print(min(sum(v.values()) for v in grid.values() if len(v) == 2))