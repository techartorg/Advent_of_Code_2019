
from operator import add, mul, lt, eq
from collections import defaultdict
from functools import wraps
from typing import List, Dict

def coroutine(gen):
    @wraps(gen)
    def start(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return start

@coroutine
def run_program(state: List[int]):
    def get_value(pntr, mode):
        if mode == 0:
            return memory[pntr]
        if mode == 1:
            return pntr
        if mode == 2:
            return memory[pntr+relative_base]

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
            memory[storage_position] = yield
        elif op == 4: # output
            yield parameters[0]
        elif op == 9: # update offset
            relative_base += parameters[0]
        elif (op == 5 and parameters[0]) or (op == 6 and not parameters[0]): # Jumps
            pointer_position = parameters[1]
            continue # We want to avoid incrementing the pointer position because we did a jump
        pointer_position += param_count # Advance pointer to next opcode
    return memory[0]

data = [int(v) for v in open('day_11.input').read().split(',')]

def run_robot(data: List[int], start_val=0) -> Dict[complex, int]:

    bot = run_program(data[:])
    grid: Dict[complex, int] = defaultdict(int)
    pos = 0j
    facing = 1j
    grid[pos] = start_val
    while True:
        try:
            i = grid[pos]
            grid[pos] = bot.send(i)
            facing *= -1j if bot.send(i) else 1j
            pos += facing
            next(bot)
        except StopIteration:
            break
    return grid
print(len(run_robot(data[:])))

grid = run_robot(data[:], 1)
xmin, *_, xmax = sorted(int(v.real) for v in grid)
ymin, *_, ymax = sorted(int(abs(v.imag)) for v in grid)
# Need to padd out the grid, otherwise you chop off the bottom part and get confused
print('\n'.join(''.join('#' if grid[x - 1j *y] else ' ' for x in range(xmin-1, xmax+2)) for y in range(ymin-1, ymax+2)))