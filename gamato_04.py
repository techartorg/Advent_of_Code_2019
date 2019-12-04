"""
### Day 4: Secure Container ###

--- Part One ---

You arrive at the Venus fuel depot only to discover it's protected by a password.
The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease;
    they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits
are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?

"""
from collections import Counter


def possible_passwords(min_num: int, max_num: int) -> list:
    pwds = [0, 0]

    for num in range(min_num, max_num):
        digits = [int(x) for x in str(num)]
        no_decrease = sorted(digits) == digits
        has_adjacent = any(2 <= x for x in Counter(digits).values())
        has_double = 2 in Counter(digits).values()  # For part two
        if no_decrease and has_adjacent:
            pwds[0] += 1
        if no_decrease and has_double:
            pwds[1] += 1

    return pwds


if __name__ == "__main__":
    part_one, part_two = possible_passwords(254032, 789860)

    print("Part One:", part_one, "Part Two:", part_two)

