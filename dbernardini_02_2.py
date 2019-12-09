"""
Find the input noun and verb that cause the program to produce the output 19690720.
What is 100 * noun + verb?
"""

intcode = [int(d) for d in open('input_02.txt', 'r').read().split(',')]


def execute_opcode(intcode, position):
    if intcode[position] == 99:
        return intcode
    elif intcode[position] == 1:
        intcode[intcode[position+3]] = intcode[intcode[position+1]]+intcode[intcode[position+2]]
    elif intcode[position] == 2:
        intcode[intcode[position + 3]] = intcode[intcode[position + 1]] * intcode[intcode[position + 2]]
    execute_opcode(intcode, position+4)
    return intcode


output = 19690720
for noun in range(100):
    for verb in range(100):
        temp_code = intcode.copy()
        temp_code[1] = noun
        temp_code[2] = verb
        if execute_opcode(temp_code, 0)[0] == output:
            print("Result: %d " % (100*noun+verb))
            break
