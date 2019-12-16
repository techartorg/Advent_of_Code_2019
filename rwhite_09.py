from operator import add, mul, lt, eq
from collections import defaultdict
from functools import wraps
from typing import List, Dict
from rwhite_intcode import Intcode

data = [int(v) for v in open('day_09.input').read().split(',')]
assert [v for v in Intcode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])] == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
assert [len(str(v)) for v in Intcode([1102,34915192,34915192,7,4,7,99,0])] == [16]
assert [v for v in Intcode([104,1125899906842624,99])] == [1125899906842624]

boost = Intcode(data[:])
boost2 = boost.clone()
boost.run_until_input()
boost2.run_until_input()
print(boost.send(1))
print(boost2.send(2))
