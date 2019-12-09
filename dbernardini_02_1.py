"""
PART 1
What value is left at position 0 after the program halts?
"""

intcode = [int(d) for d in open('input_02.txt', 'r').read().split(',')]
intcode[1] = 12
intcode[2] = 2


def execute_opcode(intcode, position):
    if intcode[position] == 99:
        return intcode
    elif intcode[position] == 1:
        intcode[intcode[position+3]] = intcode[intcode[position+1]]+intcode[intcode[position+2]]
    elif intcode[position] == 2:
        intcode[intcode[position + 3]] = intcode[intcode[position + 1]] * intcode[intcode[position + 2]]
    execute_opcode(intcode, position+4)
    return intcode


print("Output: %d" % execute_opcode(intcode, 0)[0])
