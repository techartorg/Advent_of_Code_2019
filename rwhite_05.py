from typing import List

data = [int(v) for v in open('day_05.input').read().split(',')]

def run_program(memory: List[int], input_instruction=1):
    addr = 0
    while memory[addr] != 99:
        opcode = f'{memory[addr]:05d}'
        op = int(opcode[-2:])
        modes = [int(c) for c in opcode[:-2]]
        if op == 1:
            idx = memory[addr+1] if modes[-1] else memory[memory[addr+1]]
            jdx = memory[addr+2] if modes[-2] else memory[memory[addr+2]]
            memory[memory[addr+3]] = (idx + jdx)
            addr += 4
        elif op == 2:
            idx = memory[addr+1] if modes[-1] else memory[memory[addr+1]]
            jdx = memory[addr+2] if modes[-2] else memory[memory[addr+2]]
            memory[memory[addr+3]] = (idx * jdx)
            addr += 4
        elif op == 3:
            memory[memory[addr+1]] = input_instruction
            addr += 2
        elif op == 4:
            print(memory[addr+1] if modes[-1] else memory[memory[addr+1]])
            addr += 2
        elif op == 5:
            idx = memory[addr+1] if modes[-1] else memory[memory[addr+1]]
            if idx:
                addr = memory[addr+2] if modes[-2] else memory[memory[addr+2]]
            else:
                addr += 3
        elif op == 6:
            idx = memory[addr+1] if modes[-1] else memory[memory[addr+1]]
            if not idx:
                addr = memory[addr+2] if modes[-2] else memory[memory[addr+2]]
            else:
                addr += 3
        elif op == 7:
            idx = memory[addr+1] if modes[-1] else memory[memory[addr+1]]
            jdx = memory[addr+2] if modes[-2] else memory[memory[addr+2]]
            memory[memory[addr+3]] = int(idx < jdx)
            addr += 4
        elif op == 8:
            idx = memory[addr+1] if modes[-1] else memory[memory[addr+1]]
            jdx = memory[addr+2] if modes[-2] else memory[memory[addr+2]]
            memory[memory[addr+3]] = int(idx == jdx)
            addr += 4
        else:
            raise RuntimeError('Something went really wrong.')

run_program(data[:])
run_program(data[:], 5)