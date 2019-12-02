data = [int(v) for v in open('day_01.input', 'r').read().split()]

def calc_mass(v: int) -> int:
    total = 0
    while (v := v // 3 - 2) > 0:
        total += v
    return total

print(sum(d // 3 - 2 for d in data))
print(sum(calc_mass(d) for d in data))
