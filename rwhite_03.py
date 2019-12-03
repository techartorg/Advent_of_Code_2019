from collections import defaultdict
data = open('day_03.input').read().split('\n')


offsets = {
    'R': 1,
    'L': -1,
    'U': 1j,
    'D': -1j,
}

grid = {}
wire_01 = {}
start = 0j
steps = 0
grid[start] = '0'
wire_01[start] = steps
for move in data[0].split(','):
    d = move[0]
    dist = int(move[1:])
    for _ in range(dist):
        steps += 1
        start += offsets[d]
        grid[start] = '#'
        wire_01[start] = steps

start = 0j
steps = 0
wire_02 = {}
wire_02[start] = steps
for move in data[1].split(','):
    d = move[0]
    dist = int(move[1:])
    for _ in range(dist):
        start += offsets[d]
        steps += 1
        wire_02[start] = steps
        if grid.get(start) == '#':
            grid[start] = 'X'
        else:
            grid[start] = '+'

print(min(abs(p.real) + abs(p.imag) for p, v in grid.items() if v == 'X'))
print(min(wire_01[p] + wire_02[p] for p, v in grid.items() if v == 'X'))