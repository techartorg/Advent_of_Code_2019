"""
"Good, the new computer seems to be working correctly! Keep it nearby during this mission - you'll probably use it again. Real Intcode computers support many more features than your new one, but we'll let you know what they are as you need them."

"However, your current priority should be to complete your gravity assist around the Moon. For this mission to succeed, we should settle on some terminology for the parts you've already built."

Intcode programs are given as a list of integers; these values are used as the initial state for the computer's memory. When you run an Intcode program, make sure to start by initializing memory to the program's values. A position in memory is called an address (for example, the first value in memory is at "address 0").

Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values used immediately after an opcode, if any, are called the instruction's parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and 4 are the parameters. The instruction 99 contains only an opcode and has no parameters.

The address of the current instruction is called the instruction pointer; it starts at 0. After an instruction finishes, the instruction pointer increases by the number of values in the instruction; until you add more instructions to the computer, this is always 4 (1 opcode + 3 parameters) for the add and multiply instructions. (The halt instruction would increase the instruction pointer by 1, but it halts the program instead.)

"With terminology out of the way, we're ready to proceed. To complete the gravity assist, you need to determine what pair of inputs produces the output 19690720."

The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before. In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the verb. Each of the two input values will be between 0 and 99, inclusive.

Once the program has halted, its output is available at address 0, also just like before. Each time you try a pair of inputs, make sure you first reset the computer's memory to the values in the program (your puzzle input) - in other words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)
"""

from contextlib import suppress
from copy import copy
from pathlib import Path


if __name__ == '__main__':
	with Path( '02_input.txt' ).open() as f:
		str_arr = f.read()

	initial_addresses = str_arr.split(',')
	initial_addresses = [ int( x ) for x in initial_addresses ]
		
	for x in range(100):
		addresses_x = copy(initial_addresses)
		addresses_x[1] = x
		for y in range(100):
			addresses = copy(addresses_x)
			addresses[2] = y

			for i in range(0, len(addresses), 4 ):				
				opcode = addresses[ i ]
				if opcode == 99:
					if addresses[0] == 19690720:
						print( (100 * addresses[ 1 ]) + addresses[ 2 ])
						quit()

				with suppress( IndexError ):
					parameter_1 = addresses[ i + 1 ]
					parameter_2 = addresses[ i + 2 ]
					parameter_3 = addresses[ i + 3 ]

					if opcode == 1:
						addresses[ parameter_3 ] = addresses[ parameter_1 ] + addresses[ parameter_2 ]
					elif opcode == 2:
						addresses[ parameter_3 ] = addresses[ parameter_1 ] * addresses[ parameter_2 ]
			