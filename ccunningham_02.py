from typing import List

import itertools


operations = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b
}


def run(memory: List[int], noun: int, verb: int) -> int:
    memory[1] = noun
    memory[2] = verb

    for i in range(0, len(memory), 4):
        op, addr_a, addr_b, addr_res = memory[i:i + 4]
        if op == 99:
            break
        memory[addr_res] = operations[op](memory[addr_a], memory[addr_b])

    return memory[0]


if __name__ == '__main__':
    with open('data/day2.txt', 'r') as f:
        data = [int(x) for x in f.read().split(',')]
        print(f'Part 01: {run(data[:], 12, 2)}')

        for n, v in itertools.permutations(range(100), 2):
            if run(data[:], n, v) == 19690720:
                print(f'Part 02: {100 * n + v}')
                break
