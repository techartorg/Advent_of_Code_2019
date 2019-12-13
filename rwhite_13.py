
from operator import add, mul, lt, eq
from collections import defaultdict
from functools import wraps
from typing import List, Dict, Tuple


WAITING_FOR_INPUT = object()
def coroutine(gen):
    @wraps(gen)
    def start(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return start

# @coroutine
def run_program(state: List[int]):
    def get_value(pntr, mode):
        if mode == 0:
            ret = memory[pntr]
        if mode == 1:
            ret = pntr
        if mode == 2:
            ret = memory[pntr+relative_base]
        return ret

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
            # yield WAITING_FOR_INPUT
            memory[storage_position] = yield WAITING_FOR_INPUT

        elif op == 4: # output
            yield parameters[0]
        elif op == 9: # update offset
            relative_base += parameters[0]
        elif (op == 5 and parameters[0]) or (op == 6 and not parameters[0]): # Jumps
            pointer_position = parameters[1]
            continue # We want to avoid incrementing the pointer position because we did a jump
        pointer_position += param_count # Advance pointer to next opcode
    return memory[0]

data = [int(v) for v in open('day_13.input').read().split(',')]

def run_game(data: List[int]):
    grid: Dict[Tuple[int, int], int] = defaultdict(int)
    game = list(run_program(data[:]))
    screen = [game[i:i+3] for i in range(0, len(game), 3)]
    for x, y, typ in screen:
        grid[(x, y)] = typ
    return grid
grid = run_game(data[:])
print(list(grid.values()).count(2))

def free_play(data: List[int]):
    data[0] = 2
    game = run_program(data[:])
    ball_pos = (0, 0)
    padd_pos = (0, 0)
    icons = (' ', '#', '*', '_', '.')
    state = [next(game)]
    grid: Dict[Tuple[int, int], int] = defaultdict(int)
    while True:
        try:
            if ball_pos[0] < padd_pos[0]:
                move = -1
            elif ball_pos[0] > padd_pos[0]:
                move = 1
            else:
                move = 0

            while (v := game.send(move)) != WAITING_FOR_INPUT:
                state.append(v)

            coords = [state[i:i+3] for i in range(0, len(state), 3)]
            for idx in range(0, len(state), 3):
                x, y, typ = state[idx:idx+3]
                if x == -1:
                    continue
                elif typ == 4:
                    ball_pos = (x, y)
                elif typ == 3:
                    padd_pos = (x, y)
                grid[x, y] = typ


            state.clear()
        except StopIteration:
            break
    return state[-1]
print(free_play(data[:]))