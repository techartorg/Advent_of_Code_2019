from operator import lt, eq, gt
from collections import defaultdict
from pprint import pprint
import math
data = open('day_12.input').read().split('\n')
# data="""<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>""".split('\n')
# data="""<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>""".split('\n')
pos = [tuple(int(p.split('=')[-1]) for p in line[1:-1].split(',')) for line in data]
vel = [(0, 0, 0) for i in range(4)]
states = [tuple(zip(pos, vel))]
for i in range(1000):
    npos = []
    nvel = []
    energy = []
    for p, v in states[-1]:
        np = list(p)
        nv = list(v)
        for op, ov in states[-1]:
            for idx, (x, y) in enumerate(zip(p, op)):
                if x == y:
                    continue
                elif x < y:
                    nv[idx] += 1
                elif x > y:
                    nv[idx] += -1
        np = [a+b for a, b in zip(p, nv)]
        npos.append(tuple(np))
        nvel.append(tuple(nv))
        energy.append((sum(map(abs, np)) * sum(map(abs, nv))))
    states.append(tuple(zip(npos, nvel)))
print('energy', sum(energy))

intervals = {}
for axis in range(3):
    seen = set()
    interval = 0
    positions = [p[axis] for p in pos]
    velocities = [s[axis] for s in vel]
    while True:
        axis_vals = tuple(positions) + tuple(velocities)
        if axis_vals in seen:
            intervals[axis] = interval
            break
        seen.add(axis_vals)
        new_velocities = []
        for p, v in zip(positions, velocities):
            for op in positions:
                if p == op:
                    continue
                elif p < op:
                    v += 1
                elif p > op:
                    v += -1
            new_velocities.append(v)
        velocities = new_velocities
        positions = [a+b for a, b in zip(positions, velocities)]
        interval += 1

lcm = (intervals[0] * intervals[1] // math.gcd(intervals[0], intervals[1]))
print(intervals[2] * lcm // math.gcd(intervals[2], lcm))
