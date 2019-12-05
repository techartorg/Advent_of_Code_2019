from string import digits


if __name__ == '__main__':
    possible = (str(v) for v in range(130254, 678275))

    possible_count = 0
    filtered_count = 0

    for v in possible:
        if ''.join(sorted(v)) != v or not any(v.count(d) > 1 for d in digits):
            continue

        possible_count += 1
        if any(v.count(d) == 2 for d in digits):
            filtered_count += 1

    print(f'Part 01: {possible_count}')
    print(f'Part 02: {filtered_count}')
