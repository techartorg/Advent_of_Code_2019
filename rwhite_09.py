from itertools import permutations
from operator import add, mul, lt, eq
from collections import deque
from functools import wraps
from typing import List

def coroutine(gen):
    @wraps(gen)
    def start(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return start

two_param_operations = {
    1: add,
    2: mul,
    7: lt,
    8: eq,
}

def get_value(memory, pntr, mode, relative_base):
    if mode == 0:
        return memory[pntr]
    if mode == 1:
        return pntr
    if mode == 2:
        return memory[pntr+relative_base]

# @coroutine
def run_program(memory: List[int]):
    memory.extend(0 for _ in range(10000))
    pointer_position = 0
    relative_base = 0
    while memory[pointer_position] != 99:
        opcode = f'{memory[pointer_position]:05d}'
        op = int(opcode[-2:])
        modes = [int(c) for c in opcode[:-2]][::-1]
        pointer_position += 1
        if op in (1, 2, 7, 8): # 2 parameters, stored in a register
            idx, jdx, register = memory[pointer_position:pointer_position+3]
            idx = get_value(memory, idx, modes[0], relative_base)
            jdx = get_value(memory, jdx, modes[1], relative_base)
            if modes[2] == 2:
                memory[register + relative_base] = two_param_operations[op](idx, jdx)
            else:
                memory[register] = two_param_operations[op](idx, jdx)
            pointer_position += 3
        elif op in (3, 4, 9):
            register = memory[pointer_position]
            if op == 3:
                if modes[0] == 0:
                    memory[register] = yield
                elif modes[0] == 1:
                    memory[pointer_position] = yield
                elif modes[0] == 2:
                    memory[register + relative_base] = yield
            elif op == 4:
                yield get_value(memory, register, modes[0], relative_base)
            elif op == 9:
                relative_base += get_value(memory, register, modes[0], relative_base)
            pointer_position += 1
        elif op in (5, 6): # Jumps
            idx, jdx = memory[pointer_position:pointer_position+2]
            idx = get_value(memory, idx, modes[0], relative_base)
            jdx = get_value(memory, jdx, modes[1], relative_base)
            if (op == 5 and idx) or (op == 6 and not idx):
                pointer_position = jdx
            else:
                pointer_position += 2
        else:
            raise RuntimeError('Something went really wrong.')
    return memory[0]

data = [int(v) for v in open('day_09.input').read().split(',')]
assert [v for v in run_program([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99][:])] == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
assert [len(str(v)) for v in run_program([1102,34915192,34915192,7,4,7,99,0][:])] == [16]
assert [v for v in run_program([104,1125899906842624,99][:])] == [1125899906842624]

boost = coroutine(run_program)(data[:])
print(boost.send(1))
boost = coroutine(run_program)(data[:])
print(boost.send(2))
