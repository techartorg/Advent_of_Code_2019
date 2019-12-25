from collections import defaultdict
import math
from typing import Dict, Tuple, Set, List

AsteroidMap = Dict[Tuple[int, int], Set[Tuple[int, int]]]
data = open('day_10.input').read().split()
asteroids = [(j, i) for i in range(len(data)) for j in range(len(data[0])) if data[i][j] == '#']
seen: AsteroidMap = defaultdict(set)
for x, y in asteroids:
    for a, b in asteroids:
        if (x, y) == (a, b):
            continue
        j, k = x-a, y-b
        gcd = abs(math.gcd(j, k)) # get the greatest common demoninator
        for m in range(1, gcd):
            # Check for other asteroids along that vector
            if any((a + j // gcd * m, b + k // gcd * m) in asteroids for m in range(1, gcd)):
                break
        else:
            seen[x, y].add((a, b))

best = max(seen, key=lambda x: len(seen[x]))
print(best, len(seen[best]))

lines: Dict[float, List[Tuple[int, int]]] = defaultdict(list)
for x, y in [a for a in asteroids if a != best]:
    angle = math.atan2((x-best[0]), (y-best[1])) - math.pi / 2 # Getting the angle offset from straight up
    lines[angle].append((x,y))

for v in lines.values():
    v.sort(key=lambda x: abs(x[0]-best[0]) + abs(x[1]-best[1])) # Sorting based on distance from the start point

ordered = sorted(lines.items(), key=lambda x: x[0], reverse=True) # Ordering based on the rotation angle
assert len(ordered) >= 200 # If its less than 200, I probably have to do more work rotating through all of these instead of just looping until this works.
for idx, (angle, point) in enumerate(ordered, 1):
    if idx == 200:
        x, y = point[0]
        print(x*100 + y)
        break
