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
from itertools import permutations
from pathlib import Path


def find_noun_and_verb( data: list, output: int ) -> int:
	"""
	Iterates over 9900 possible permutations of values for data[ 1 ] and data[ 2 ] to find the combination
	of noun and verb that, when run in the program, produce the value supplied for the parameter 'output'.
	
	Arguments:
		 data {list} -- 
		 output {int} -- The potential program output for which noun and verb are being searched.
	
	Returns:
		 int -- noun * 100 + verb. -1 if the program is unsolvable.
	"""

	for a, b in permutations( range( 100 ), 2 ):
		data = copy( initial_data )
		data[ 1 ] = a
		data[ 2 ] = b

		for i in range(0, len( data ), 4 ):
			with suppress( ValueError ):
				opcode, p1, p2, p3 = data[ i : i + 4 ]

				if opcode == 99 and data[ 0 ] == output:
					return ( 100 * data[ 1 ] ) + data[ 2 ]

				data[ p3 ] = data[ p1 ] + data[ p2 ] if opcode == 1 else data[ p1 ] * data[ p2 ]

	return -1


if __name__ == '__main__':
	with Path( '02_input.txt' ).open( ) as f:
		initial_data = [ int( x ) for x in f.read( ).split( ',' ) ]

	OUTPUT = 19690720
	noun_verb = find_noun_and_verb( initial_data, OUTPUT )
	if noun_verb > -1:
		print( f'The noun and verb that produce {OUTPUT} are {noun_verb}.' )
	else:
		print( f'There is no combination of noun and verb that produce the output {OUTPUT}.')
	