import itertools
from functools import wraps
from typing import List
from operator import add, mul, lt, eq


data = [int(v) for v in open('day_02.input').read().split(',')]

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

@coroutine
def run_program(memory: List[int]):
    pointer_position = 0
    while memory[pointer_position] != 99:
        opcode = f'{memory[pointer_position]:05d}'
        op = int(opcode[-2:])
        modes = [int(c) for c in opcode[:-2]][::-1]
        pointer_position += 1
        if op in (1, 2, 7, 8): # 2 parameters, stored in a register
            idx, jdx, register = memory[pointer_position:pointer_position+3]
            idx = idx if modes[0] else memory[idx]
            jdx = jdx if modes[1] else memory[jdx]
            memory[register] = two_param_operations[op](idx, jdx)
            pointer_position += 3
        elif op in (3, 4):
            register = memory[pointer_position]
            if op == 3:
                memory[register] = yield
            elif op == 4:
                yield register if modes[0] else memory[register]
            pointer_position += 1
        elif op in (5, 6): # Jumps
            idx, register = memory[pointer_position:pointer_position+2]
            idx = idx if modes[0] else memory[idx]
            register = register if modes[1] else memory[register]
            if (op == 5 and idx) or (op == 6 and not idx):
                pointer_position = register
            else:
                pointer_position += 2
        else:
            raise RuntimeError('Something went really wrong.')
    return memory[0]

def run_with_noun_verb(memory: List[int], noun: int, verb: int):
    memory[1] = noun
    memory[2] = verb
    try:
        return run_program(memory[:])
    except StopIteration as e:
        return e.value

print('Part 01:', run_with_noun_verb(data[:], 12, 2))

for n, v in itertools.product(range(100), range(100)):
    if run_with_noun_verb(data[:], n, v) == 19690720:
        print(f'Part 02: {100*n + v}')
        break
