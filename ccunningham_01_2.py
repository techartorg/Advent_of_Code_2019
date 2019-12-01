def fuel_for_module(mass: int) -> int:
    module_fuel = 0

    while (mass := mass // 3 - 2) > 0:
        module_fuel += mass

    return module_fuel


if __name__ == '__main__':
    with open('data/day1.txt', 'r') as f:
        total_fuel = sum(fuel_for_module(int(mass)) for mass in f)

    print(f'The total fuel requirements for all modules is: {total_fuel}')
