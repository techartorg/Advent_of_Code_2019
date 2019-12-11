def run_intcode(input_data, start_panel):
    op_counts = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]
    program = [int(x) for x in input_data] + [0] * 10000
    i, relative_base = 0, 0

    panels = {(0, 0): start_panel}
    pos = (0, 0)
    outputs = []

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_idx = 0

    while program[i] != 99:
        modes = [int(x) for x in f"{program[i]:0>5}"[:3]][::-1]
        instruction = int(f"{program[i]:0>5}"[3:])
        op_count = op_counts[instruction]
        base = [relative_base if modes[x] == 2 else 0 for x in range(op_count)]
        operands = [program[i+x+1] if modes[x] == 1 else program[base[x] + program[i+x+1]] for x in range(op_count)]

        if instruction == 1:
            program[base[2] + program[i + 3]] = operands[0] + operands[1]
        elif instruction == 2:
            program[base[2] + program[i + 3]] = operands[0] * operands[1]
        elif instruction == 3:
            program[base[0] + program[i + 1]] = panels[pos] if pos in panels else 0
        elif instruction == 4:
            outputs.append(operands[0])
            if len(outputs) == 2:
                panels[pos] = outputs[0]
                dir_idx = (dir_idx + (1 if outputs[1] else -1)) % len(directions)
                pos = (pos[0] + directions[dir_idx][0], pos[1] + directions[dir_idx][1])
                outputs = []
        elif instruction == 5:
            i = (operands[1] - 3) if operands[0] != 0 else i
        elif instruction == 6:
            i = (operands[1] - 3) if operands[0] == 0 else i
        elif instruction == 7:
            program[base[2] + program[i + 3]] = int(operands[0] < operands[1])
        elif instruction == 8:
            program[base[2] + program[i + 3]] = int(operands[0] == operands[1])
        elif instruction == 9:
            relative_base += operands[0]
        i += op_count + 1

    return panels


def generate_registration(intcode_result):
    """
    Generates the ascii array
    :param intcode_result: result of the intcode operation
    :return: array of ascii characters
    """
    grid = [[" "] * 50 for _ in range(7)]

    for panel in zip(intcode_result.keys(), intcode_result.values()):
        grid[panel[0][0]][panel[0][1]] = "#" if panel[1] else " "

    return grid


if __name__ == "__main__":
    data = open("input11.txt", 'r').readline().split(',')
    print("Part One:", "Panel Count =", len(run_intcode(data, 0)))

    registration = generate_registration(run_intcode(data, 1))
    [print(" ".join(panel)) for panel in registration]
