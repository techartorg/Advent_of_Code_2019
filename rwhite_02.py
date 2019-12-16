import itertools
from functools import wraps
from typing import List
from operator import add, mul, lt, eq
from rwhite_intcode import Intcode

data = [int(v) for v in open('day_02.input').read().split(',')]


def run_with_noun_verb(memory: List[int], noun: int, verb: int):
    memory[1] = noun
    memory[2] = verb
    try:
        return Intcode(memory[:]).run_until_input()[0]
    except StopIteration as e:
        return e.value

print('Part 01:', run_with_noun_verb(data[:], 12, 2))

for n, v in itertools.product(range(100), range(100)):
    if run_with_noun_verb(data[:], n, v) == 19690720:
        print(f'Part 02: {100*n + v}')
        break
