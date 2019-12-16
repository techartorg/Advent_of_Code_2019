from itertools import permutations
from operator import add, mul, lt, eq
from collections import deque, defaultdict
from functools import wraps
from typing import List, Dict
from rwhite_intcode import Intcode, WAITING_FOR_INPUT


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
        pointer_position += param_count
    return memory[0]


data = [int(v) for v in open('day_07.input').read().split(',')]
thrust = []
for phases in permutations(range(5), 5):
    amplifiers = [Intcode(data[:]) for i in range(5)]
    input_instruction = 0
    for idx, p in enumerate(phases):
        amplifiers[idx].run_until_input()
        amplifiers[idx].send(p) # input the phase_instruction, loops to next input
        input_instruction = amplifiers[idx].send(input_instruction) # input the input_instruction, and get the output for the next stage
    thrust.append(input_instruction)
print(max(thrust))

amplified_thrust = []
for phases in permutations(range(5, 10), 5):
    amplifier_loop = deque(Intcode(data[:]) for i in range(5))
    for amp, p in zip(amplifier_loop, phases): # Prime and start each amplifier with their phase input
        amp.run_until_input()
        amp.send(p)

    # From here on out, we're rotating through the amplifiers, sending in the new input instruction, and then having it calculate until it hits the end.
    input_instruction = 0
    while amplifier_loop:
        amp = amplifier_loop.popleft()
        try:
            if (v := amp.send(input_instruction)) is WAITING_FOR_INPUT:
                v = amp.send(input_instruction)
            input_instruction = v
        except StopIteration:
            pass
        else:
            amplifier_loop.append(amp)
    amplified_thrust.append(input_instruction)
print(max(amplified_thrust))
