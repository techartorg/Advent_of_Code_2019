import string
import heapq
from pprint import pprint
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set
Position = Tuple[int, int]

data = open('day_20.input').read().split('\n')

# data = """*********A*********
# *********A*********
#   #######.#########
#   #######.........#
#   #######.#######.#
#   #######.#######.#
#   #######.#######.#
#   #####  B    ###.#
# BC...##  C    ###.#
#   ##.##       ###.#
#   ##...DE  F  ###.#
#   #####    G  ###.#
#   #########.#####.#
# DE..#######...###.#
#   #.#########.###.#
# FG..#########.....#
#   ###########.#####
#              Z*****
#              Z*****""".split('\n')
grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[0]))}
positions: Dict[str, List[Position]] = defaultdict(list)
portals: Dict[Position, Tuple[str, int]] = {}
for (x, y), v in grid.items():
    if v in string.ascii_uppercase:
        for dx, dy in ((0, 1), (1, 0), ):
            if (v2 := grid.get((x+dx, y+dy), '0')) in string.ascii_uppercase:
                port = v+v2
                pos = (x-dx, y-dy) if grid.get((x-dx, y-dy)) == ' ' else (x+2*dx, y+2*dy)
                positions[port].append(pos)
                portals[pos] = port, -1 if None in (grid.get((x+2*dx, y+2*dy)), grid.get((x-dx, y-dy))) else 1
                break

def get_connected_portals(start: Position) -> Dict[str, Tuple[Position, int]]:
    total_steps = 0
    queue = deque([(start, total_steps)])
    seen = set()
    portal_info = {}
    while queue:
        pos, steps = queue.popleft()
        if pos in portals and pos != start:
            port, _ = portals[pos]
            other_pos = next((p for p in positions[port] if p != pos), pos)
            portal_info[port] = other_pos, steps+1
        seen.add(pos)
        steps += 1
        x, y = pos
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = (x + dx, y + dy)
            if grid.get(new_pos) != ' ' or new_pos in seen:
                continue
            queue.append((new_pos, steps))
    return portal_info

total_steps = 0
queue = [(-1, {'AA'}, positions['AA'][0])]
possible = set()
while queue:
    steps, seen_portals, pos = heapq.heappop(queue)
    for portal, (new_pos, distance) in get_connected_portals(pos).items():
        if portal == 'ZZ':
            possible.add((steps+distance))
        if portal in seen_portals:
            continue
        heapq.heappush(queue, (steps+distance, seen_portals | {portal}, new_pos))
print(min(possible))

# So I couldn't get my portal based graph solution to work for part 2, instead I had to go finer grained and make a graph of all the possitions in the system
graph: Dict[Position, Set[Tuple[Position, int]]] = defaultdict(set)
for (x, y), v in grid.items():
    if v not in string.ascii_uppercase + ' ':
        continue
    for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        p = (x+dx, y+dy)
        if grid.get(p) == ' ':
            graph[(x, y)].add((p, 0))
        elif grid.get(p, '').isalpha() and grid.get((x, y), '') == ' ':
            port, offset = portals[(x, y)]
            pp = next((v for v in positions[port] if v != (x, y)), (-1, -1))
            graph[(x, y)].add((pp, offset))

seen: Set[Tuple[int, int, int]] = set()
queue2 = [(-1, 0, positions['AA'][0])]
try:
    while queue2:
        steps, depth, (x, y) = heapq.heappop(queue2)
        if (x, y, depth) in seen:
            continue
        seen.add((x, y, depth))
        for (dx, dy), dd in graph[(x, y)]:
            if portals.get((x, y), [''])[0] == 'ZZ' and depth == 0:
                raise RuntimeError()
            if (new_depth := dd + depth) >= 0: # have to go deeper before we can use the outside ring again
                heapq.heappush(queue2, (steps+1, new_depth, (dx, dy)))
except RuntimeError:
    print(steps+1)
