
from operator import add, mul, lt, eq
from collections import defaultdict, deque
from itertools import tee
from functools import wraps
from typing import List, Dict, Tuple


WAITING_FOR_INPUT = object()
BEGIN_LOOP = object()

def coroutine(gen):
    @wraps(gen)
    def start(*args, **kwargs):
        g = gen(*args, **kwargs)
        assert next(g) == BEGIN_LOOP
        return g
    return start

@coroutine
def run_program(state: List[int]):
    def get_value(pntr, mode):
        if mode == 0:
            ret = memory[pntr]
        if mode == 1:
            ret = pntr
        if mode == 2:
            ret = memory[pntr+relative_base]
        return ret

    def dump_state():
        return dict(memory)

    two_param_operations = {
        1: add,
        2: mul,
        7: lt,
        8: eq,
    }
    pointer_position = 0
    relative_base = 0
    op_params = (0, 3, 3, 1, 1, 2, 2, 3, 3, 1)
    memory: Dict[int, int] = defaultdict(int) # Keeps me from guessing as to how much memory expansion I need to do.
    memory.update(enumerate(state)) # Fastest way to convert a list into a dictionary and keep the indicies in order.
    yield BEGIN_LOOP
    while memory[pointer_position] != 99:
        # Get the current opcode, and storage location
        opcode = f'{memory[pointer_position]:05d}'
        op = int(opcode[-2:])
        modes = [int(c) for c in opcode[:-2]][::-1]
        param_count = op_params[op]
        storage_position = memory[pointer_position+param_count] if modes[param_count-1] == 0 else memory[pointer_position+param_count] + relative_base
        # Advance the pointer by 1 so we can start processing parameters.
        pointer_position += 1
        parameters = [get_value(memory[idx], mode) for idx, mode in zip(range(pointer_position, pointer_position+param_count), modes)]
        if op in (1, 2, 7, 8): # 2 parameters
            memory[storage_position] = int(two_param_operations[op](parameters[0], parameters[1]))
        elif op == 3: # input
            # yield WAITING_FOR_INPUT
            memory[storage_position] = yield WAITING_FOR_INPUT, [memory[idx] for idx in range(max(memory)+1)]
        elif op == 4: # output
            yield parameters[0]
        elif op == 9: # update offset
            relative_base += parameters[0]
        elif (op == 5 and parameters[0]) or (op == 6 and not parameters[0]): # Jumps
            pointer_position = parameters[1]
            continue # We want to avoid incrementing the pointer position because we did a jump
        pointer_position += param_count # Advance pointer to next opcode
    return memory[0]

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
    # Basic idea here is that we're going to map out the grid with a fleet of robots.
    # so at each step we build new robots for each direction, unless we hit a wall
    # we're also tracking the total number of steps each of these bots take, so if they
    # loop back onto a spot another bot explored, they avoid it, but only if the other bot
    # got their with a smaller number of steps.
    grid = defaultdict(int)
    grid[0j] = -1

    bot = run_program(data[:])
    fleet = deque([(bot, 0j, 0)]) # Flood filling with robots!
    counts = {0j: 0}
    oxy_pos = None
    total_steps = -1
    while fleet:
        bot, pos, steps = fleet.popleft()
        steps += 1
        v, state = next(bot)
        assert v == WAITING_FOR_INPUT
        for jdx, (code, mov) in enumerate(move_codes.items()):
            npos = mov + pos
            if npos in grid and counts[npos] < steps:
                continue
            nbot = run_program(state[:])
            _v, _state = next(nbot)
            assert _v == v and _state == state
            ret = nbot.send(code)
            grid[npos] = ret
            counts[npos] = steps
            if ret == 2:
                # We don't return early here, because we want to finish mapping the grid, as we need it for part 2
                total_steps = steps
                oxy_pos = npos
            if ret:
                fleet.append((nbot, npos, steps))
    return grid, total_steps, oxy_pos


def get_oxygen_count(start_pos, grid):
    # Flood fill again
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
