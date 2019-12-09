from collections import defaultdict
from typing import Dict, Tuple
from operator import add

Vec2Int = Tuple[int, int]

directions = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def add_vec(a: Vec2Int, b: Vec2Int) -> Vec2Int:
    return tuple(map(add, a, b))


if __name__ == '__main__':
    grid: Dict[Vec2Int, Dict[int, int]] = defaultdict(dict)

    with open('data/day3.txt', 'r') as f:
        for idx, wire in enumerate(f):
            steps = 0
            position = (0, 0)

            for move in wire.split(','):
                direction = directions[move[0]]
                distance = int(move[1:])

                for _ in range(distance):
                    steps += 1
                    position = add_vec(position, direction)
                    grid[position].setdefault(idx, steps)

    part1 = min(abs(p[0]) + abs(p[1]) for p, v in grid.items() if len(v) == 2)
    print(f'Part 01: {part1}')

    part2 = min(sum(v.values()) for v in grid.values() if len(v) == 2)
    print(f'Part 02: {part2}')
