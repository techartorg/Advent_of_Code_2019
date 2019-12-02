from __future__ import annotations
import itertools
from typing import List
data = [int(v) for v in open('day_02.input').read().split(',')]

def run_program(memory: List[int], noun: int, verb: int) -> int:
    addr = 0
    memory[1] = noun
    memory[2] = verb
    while memory[addr] != 99:
        op, idx, jdx, res = memory[addr:addr+4]
        if op == 1:
            memory[res] = memory[idx] + memory[jdx]
        elif op == 2:
            memory[res] = memory[idx] * memory[jdx]
        addr += 4
    return memory[0]

print('Part 01:', run_program(data[:], 12, 2))

for n, v in itertools.product(range(100), range(100)):
    if run_program(data[:], n, v) == 19690720:
        print(f'Part 02: {100*n + v}')
        break
