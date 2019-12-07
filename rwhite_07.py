from itertools import permutations, repeat, chain
from collections import deque
from typing import List

def run_program(memory: List[int]):
    pointer_position = 0
    used_phase = False
    while memory[pointer_position] != 99:
        opcode = f'{memory[pointer_position]:05d}'
        op = int(opcode[-2:])
        modes = [int(c) for c in opcode[:-2]]
        if op == 1:
            idx = memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            jdx = memory[pointer_position+2] if modes[-2] else memory[memory[pointer_position+2]]
            memory[memory[pointer_position+3]] = (idx + jdx)
            pointer_position += 4
        elif op == 2:
            idx = memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            jdx = memory[pointer_position+2] if modes[-2] else memory[memory[pointer_position+2]]
            memory[memory[pointer_position+3]] = (idx * jdx)
            pointer_position += 4
        elif op == 3:
            memory[memory[pointer_position+1]] = yield
            pointer_position += 2
        elif op == 4:
            yield memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            pointer_position += 2
        elif op == 5:
            idx = memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            if idx:
                pointer_position = memory[pointer_position+2] if modes[-2] else memory[memory[pointer_position+2]]
            else:
                pointer_position += 3
        elif op == 6:
            idx = memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            if not idx:
                pointer_position = memory[pointer_position+2] if modes[-2] else memory[memory[pointer_position+2]]
            else:
                pointer_position += 3
        elif op == 7:
            idx = memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            jdx = memory[pointer_position+2] if modes[-2] else memory[memory[pointer_position+2]]
            memory[memory[pointer_position+3]] = int(idx < jdx)
            pointer_position += 4
        elif op == 8:
            idx = memory[pointer_position+1] if modes[-1] else memory[memory[pointer_position+1]]
            jdx = memory[pointer_position+2] if modes[-2] else memory[memory[pointer_position+2]]
            memory[memory[pointer_position+3]] = int(idx == jdx)
            pointer_position += 4
        else:
            raise RuntimeError('Something went really wrong.')


data = [int(v) for v in open('day_07.input').read().split(',')]
thrust = []
for phases in permutations(range(5), 5):
    amplifiers = [run_program(data[:]) for i in range(5)]
    input_instruction = 0
    for idx, p in enumerate(phases):
        next(amplifiers[idx]) # Prime the amplifier, this gets us to the first input
        amplifiers[idx].send(p) # input the phase_instruction, loops to next input
        input_instruction = amplifiers[idx].send(input_instruction) # input the input_instruction, and get the output for the next stage

    thrust.append(input_instruction)
print(max(thrust))

amplified_thrust = []
for phases in permutations(range(5, 10), 5):
    amplifier_loop = deque(run_program(data[:]) for i in range(5))
    for amp, p in zip(amplifier_loop, phases): # Prime and start each amplifier with their phase input
        next(amp)
        amp.send(p)

    # From here on out, we're rotating through the amplifiers, sending in the new input instruction, and then having it calculate until it hits the end.
    input_instruction = 0
    while True:
        amp = amplifier_loop[0]
        try:
            input_instruction = amp.send(input_instruction)
            next(amp)
        except StopIteration:
            break
        else:
            amplifier_loop.rotate(-1) # rotation is negative, otherwise we go the wrong way, yes I did that wrong the first time.
    amplified_thrust.append(input_instruction)
print(max(amplified_thrust))