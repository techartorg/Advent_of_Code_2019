def fuel_for_mass(mass: int) -> int:
    return mass // 3 - 2


def fuel_for_module(mass: int) -> int:
    module_fuel = 0
    while (mass := fuel_for_mass(mass)) > 0:
        module_fuel += mass

    return module_fuel


if __name__ == '__main__':
    with open('data/day1.txt', 'r') as f:
        data = [int(value) for value in f]
        print(f'Part 1: {sum(fuel_for_mass(mass) for mass in data)}')
        print(f'Part 2: {sum(fuel_for_module(mass) for mass in data)}')
