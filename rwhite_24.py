from collections import deque, defaultdict
from itertools import chain

data = open('day_24.input').read().split('\n')

states = {''.join(data)}
grid = {}
for y in range(len(data)):
    for x in range(len(data[0])):
        grid[(x, y)] = data[y][x]

while True:
    new_grid = grid.copy()
    for (x, y), v in grid.items():
        adjacent = []
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx = dx + x
            ny = dy + y
            adjacent.append(grid.get((nx, ny), ''))
        if v == '#' and adjacent.count('#') != 1:
            new_grid[(x, y)] = '.'
        elif v == '.' and adjacent.count('#') in (1, 2):
            new_grid[(x, y)] = '#'
    grid = new_grid.copy()
    state = ''.join(new_grid[(x, y)] for y in range(len(data)) for x in range(len(data[0])))
    if state in states:
        break
    states.add(state)
bio = 0
for idx, v in enumerate(state):
    if v == '#':
        bio += 2 ** idx
print(bio)

# We know we need to go 200 steps, which means we'll be peaking into 200 layers on each side, so we'll start by building a stack 401 layers deep.
# where layer 200 will be our initial start.
RUN_TIME = 200
infinite_grid = []
for idx in range(RUN_TIME * 2 + 1):
    if idx == RUN_TIME:
        infinite_grid.append([list(d) for d in data])
    else:
        infinite_grid.append([['.']*5 for _ in range(5)])


for idx in range(200):
    # Make a new empty stack, we'll be mutating this one, and then replacing the previous with updated values
    ig = [[['.']*5 for _ in range(5)] for _ in range(2*RUN_TIME + 1)]
    for depth in range(2*RUN_TIME + 1):
        for y in range(5):
            for x in range(5):
                if x == y == 2:
                    continue
                bugs = 0
                # No bugs on the outer most, this one is empty and just exists so we can properly check info in +/- 199
                if depth not in (0, RUN_TIME*2):
                    # I tried being cleve at first with checking adjacent values, but kept coming up with the wrong answer
                    # so I just kept getting more explicit
                    if y == 0:
                        bugs += infinite_grid[depth-1][1][2] == '#'
                    elif (x, y) == (2, 3):
                        bugs += sum(infinite_grid[depth+1][4][k] == '#' for k in range(5))
                    else:
                        bugs += infinite_grid[depth][y-1][x] == '#'

                    if y == 4:
                        bugs += infinite_grid[depth-1][3][2] == '#'
                    elif (x, y) == (2, 1):
                        bugs += sum(infinite_grid[depth+1][0][k] == '#' for k in range(5))
                    else:
                        bugs += infinite_grid[depth][y+1][x] == '#'

                    if x == 0:
                        bugs += infinite_grid[depth-1][2][1] == '#'
                    elif (x, y) == (3, 2):
                        bugs += sum(infinite_grid[depth+1][k][4] == '#' for k in range(5))
                    else:
                        bugs += infinite_grid[depth][y][x-1] == '#'

                    if x == 4:
                        bugs += infinite_grid[depth-1][2][3] == '#'
                    elif (x, y) == (1, 2):
                        bugs += sum(infinite_grid[depth+1][k][0] == '#' for k in range(5))
                    else:
                        bugs += infinite_grid[depth][y][x+1] == '#'

                # Grid's already empty to start, so we only need to insert locations where a bug should now exist.
                if (infinite_grid[depth][y][x] == '#' and bugs == 1) or (infinite_grid[depth][y][x] == '.' and bugs in (1, 2)):
                    ig[depth][y][x] = '#'
    # Make sue to check the new grid on the next loop through
    infinite_grid = ig
# List of lists of strings, double chain.from_iterable!
print(''.join(chain.from_iterable(chain.from_iterable(infinite_grid))).count('#'))
