if __name__ == '__main__':
    with open('data/day1.txt', 'r') as f:
        total_fuel = sum(int(mass) // 3 - 2 for mass in f)

    print(f'The total fuel requirements for all modules is: {total_fuel}')
