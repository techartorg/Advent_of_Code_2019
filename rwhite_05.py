from typing import List

data = [int(v) for v in open('day_05.input').read().split(',')]

def coroutine(gen):
    def start(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return start

two_param_operations = {
    1: lambda a, b : a + b,
    2: lambda a, b : a * b,
    7: lambda a, b : int(a < b),
    8: lambda a, b : int(a == b),
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


part_01 = run_program(data[:])
while (v := part_01.send(1)) == 0:
    pass
print(v)
part_02 = run_program(data[:])
while (v := part_02.send(5)) == 0:
    pass
print(v)