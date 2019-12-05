"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 240298-784956.
"""

if __name__ == '__main__':
	valid_pwd_count = 0
	for pwd in range( 240298, 784956 ): # Really should do 784957, but 784956 isn't a valid password so there's no need to verify it.
		str_pwd = str( pwd )
		set_len = len( set( str_pwd ) )

		if set_len == 1: # All duplicates. Early out.
			valid_pwd_count += 1
			continue
		elif set_len == len( str_pwd ): # No duplicates. Early out.
			continue

		double_found = False
		for i in range( len( str_pwd ) - 1 , -1, -1 ):
			if i >= 1:
				a = int( str_pwd[ i - 1 ] )
				b = int( str_pwd[ i ] )
				if a > b:
					break
				elif a == b:
					double_found = True

		else:
			if double_found:
				valid_pwd_count += 1

	print( f'The number of potential valid passwords in the range given is: {valid_pwd_count}.' )
