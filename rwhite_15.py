
from __future__ import annotations
from operator import add, mul, lt, eq
from collections import defaultdict, deque
from typing import List, Dict
from rwhite_intcode import Intcode, WAITING_FOR_INPUT




data = [int(v) for v in open('day_15.input').read().split(',')]
move_codes = {
    1: 1j,
    2: -1j,
    3: -1,
    4: 1,
}
return_codes = {
   -2: 'D',
   -1: 'S',
    0: '#',
    1: ' ',
    2: 'X',
    3: 'O',
}

def build_grid(data):
    # So basic idea, is that instead of trying to trick one robot into mapping the whole maze
    # we create a fleet of robots. So each time mutliple viable paths exist, we clone the bot,
    # and start it going in the extra directions.
    grid = defaultdict(int)
    grid[0j] = -1

    bot = Intcode(data[:])
    fleet = deque([(bot, 0j, 0)])
    counts = {0j: 0}
    oxy_pos = None
    total_steps = set()
    while fleet:
        bot, pos, steps = fleet.popleft()
        steps += 1
        assert next(bot) == WAITING_FOR_INPUT
        for jdx, (code, mov) in enumerate(move_codes.items()):
            npos = mov + pos
            if npos in grid and counts[npos] < steps:
                continue
            nbot = bot.clone()
            assert next(nbot) == WAITING_FOR_INPUT
            ret = nbot.send(code)
            grid[npos] = ret
            counts[npos] = steps
            if ret == 2:
                # We don't return early here, because we want to finish mapping the grid, as we need it for part 2
                # in theory we shouldn't hit this more than once, but just in case we track the steps in a collection
                # and we'll return the minimum value.
                total_steps.add(steps)
                oxy_pos = npos
            if ret:
                fleet.append((nbot, npos, steps))
    return grid, min(total_steps), oxy_pos


def get_oxygen_count(start_pos, grid):
    # Flood fill
    seen = set()
    fill = [(start_pos, 0)]
    total_steps = set()
    count = 0
    while fill:
        new_edges = []
        for pos, step in fill:
            if pos in seen:
                continue
            step += 1
            seen.add(pos)
            for m in move_codes.values():
               npos = m + pos
               if grid.get(npos):
                   grid[npos] = 3
                   new_edges.append((npos, step))
                   if 1 not in grid.values():
                       return step
        fill[:] = new_edges

grid, steps, oxy_pos = build_grid(data[:])
print(steps)
print(get_oxygen_count(oxy_pos, grid.copy()))
