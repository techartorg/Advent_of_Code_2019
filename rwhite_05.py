from typing import List
from functools import wraps
from operator import add, mul, lt, eq
from rwhite_intcode import Intcode

data = [int(v) for v in open('day_05.input').read().split(',')]

part_01 = Intcode(data[:])
part_01.run_until_input()
print(part_01.run_until_input(1)[-1])
part_02 = Intcode(data[:])
part_02.run_until_input()
print(part_02.run_until_input(5)[-1])
