from functools import wraps
from typing import Tuple, List, Dict, Callable
from inspect import signature

ops: Dict[int, Tuple[int, bool, bool, Callable]] = {}


def coroutine(gen):
    @wraps(gen)
    def start(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g
    return start


def register_op(op_code: int, takes_input: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        sig = signature(func)
        #  yes kinda dirty hard coding of the last arg, but i need it to behaving a little different then the others
        ops[op_code] = (len(sig.parameters), takes_input, 'addr' in sig.parameters, wrapper)
        return wrapper
    return decorator


@coroutine
def run(memory: List[int]):
    @register_op(op_code=1)
    def add(a, b, addr):
        memory[addr] = a + b

    @register_op(op_code=2)
    def multiply(a, b, addr):
        memory[addr] = a * b

    @register_op(op_code=3, takes_input=True)
    def save(addr):
        memory[addr] = input_data

    @register_op(op_code=4)
    def output(addr):
        return addr if modes[0] else memory[addr]

    @register_op(op_code=5)
    def jump_true(a, b):
        nonlocal pointer
        if a:
            pointer = b - arg_count

    @register_op(op_code=6)
    def jump_false(a, b):
        nonlocal pointer
        if a == 0:
            pointer = b - arg_count

    @register_op(op_code=7)
    def less_then(a, b, addr):
        memory[addr] = int(a < b)

    @register_op(op_code=8)
    def equal(a, b, addr):
        memory[addr] = int(a == b)

    pointer = 0
    while memory[pointer] != 99:
        op_str = f'{memory[pointer]:05d}'
        arg_count, takes_input, has_addr, op = ops[int(op_str[-2:])]
        modes = [int(c) for c in op_str[:-2]][::-1]
        pointer += 1

        args = memory[pointer:pointer + arg_count]
        for i, arg in enumerate(args if not has_addr else args[:-1]):
            args[i] = arg if modes[i] else memory[arg]

        if takes_input:
            input_data = yield

        if (result := op(*args)) is not None:
            yield result

        pointer += arg_count
    return memory[0]


if __name__ == '__main__':
    with open('data/day5.txt', 'r') as f:
        data = [int(x) for x in f.read().split(',')]

        part_01 = run(data[:])
        while (v := part_01.send(1)) == 0:
            pass
        print(f'Part 01: {v}')

        part_02 = run(data[:])
        while (v := part_02.send(5)) == 0:
            pass
        print(f'Part 02: {v}')
