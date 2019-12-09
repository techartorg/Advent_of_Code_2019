from itertools import permutations, repeat, chain
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



data = [int(v) for v in open('day_07.input').read().split(',')]
thrust = []
for phases in permutations(range(5), 5):
    amplifiers = [run_program(data[:]) for i in range(5)]
    input_instruction = 0
    for idx, p in enumerate(phases):
        amplifiers[idx].send(p) # input the phase_instruction, loops to next input
        input_instruction = amplifiers[idx].send(input_instruction) # input the input_instruction, and get the output for the next stage
    thrust.append(input_instruction)
print(max(thrust))

amplified_thrust = []
for phases in permutations(range(5, 10), 5):
    amplifier_loop = deque(run_program(data[:]) for i in range(5))
    for amp, p in zip(amplifier_loop, phases): # Prime and start each amplifier with their phase input
        amp.send(p)

    # From here on out, we're rotating through the amplifiers, sending in the new input instruction, and then having it calculate until it hits the end.
    input_instruction = 0
    while amplifier_loop:
        amp = amplifier_loop.popleft()
        try:
            while (v := amp.send(input_instruction)) is None:
                pass
            else:
                input_instruction = v
        except StopIteration:
            pass
        else:
            amplifier_loop.append(amp)
    amplified_thrust.append(input_instruction)
print(max(amplified_thrust))
