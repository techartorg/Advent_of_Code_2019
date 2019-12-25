from collections import defaultdict
import math
from typing import Dict, Tuple, Set, List

AsteroidMap = Dict[Tuple[int, int], Set[Tuple[int, int]]]
data = open('day_10.input').read().split()
asteroids = [(x, y) for y in range(len(data)) for x in range(len(data[0])) if data[y][x] == '#']
seen: AsteroidMap = defaultdict(set)
for x0, y0 in asteroids:
    for x1, x2 in asteroids:
        if (x0, y0) == (x1, x2):
            continue
        dx, dy = x0-x1, y0-x2
        # get the greatest common demoninator
        gcd = abs(math.gcd(dx, dy))
        # Check for other asteroids along that vector
        if not any((x1 + dx // gcd * m, x2 + dy // gcd * m) in asteroids for m in range(1, gcd)):
            seen[x0, y0].add((x1, x2))


best = max(seen, key=lambda x0: len(seen[x0]))
print(len(seen[best]))

lines: Dict[float, List[Tuple[int, int]]] = defaultdict(list)
for x, y in [ast for ast in asteroids if ast != best]:
    angle = math.atan2((x-best[0]), (y-best[1])) - math.pi / 2 # Getting the angle offset from straight up
    lines[angle].append((x, y))

for v in lines.values():
    v.sort(key=lambda x: abs(x[0]-best[0]) + abs(x[1]-best[1])) # Sorting based on distance from the start point

ordered = sorted(lines.items(), key=lambda x: x[0], reverse=True) # Ordering based on the rotation angle
assert len(ordered) >= 200 # If its less than 200, I probably have to do more work rotating through all of these instead of just looping until this works.
for idx, (angle, point) in enumerate(ordered, 1):
    if idx == 200:
        x, y = point[0]
        print(x*100 + y)
        break
