from collections import deque
from itertools import count

data = open('day_22.input').read().split('\n')

def process_deck(cards):
    deck = deque(cards)
    for line in data:
        increment = 0
        if line.startswith('deal into new stack'):
            deck.reverse()
        elif line.startswith('deal with increment'):
            increment = int(line.split()[-1])
            for v in deck.copy():
                deck[0] = v
                deck.rotate(-increment)
        elif line.startswith('cut'):
            increment = int(line.split()[-1])
            deck.rotate(-increment)
    return deck

# Can actually replace this with my shuffle_card function from part 2, which should be faster as it just reduces to maths
print(process_deck(range(10007)).index(2019))

# So part 2 is going to be super math heavy.
# Not going to lie, had to get some hints from others in the directions to look.
# But basically we can reduce this down to some linear equations, and then the whole thing produces an LCG pseudorandom sequence
# with a repeating period equal to the number of cards in the deck.

# Source https://tailcall.net/blog/cracking-randomness-lcgs/

def get_mod_mul_inc(c0, c1, c2, num_cards):
    mul = (c2 - c1) * pow(c1 - c0, -1, num_cards) % num_cards
    inc = (c1 - c0 * mul) % num_cards
    return num_cards, mul, inc

def super_shuffle(mul, inc, mod, card_index, shuffle_by):
    # https://www.nayuki.io/page/fast-skipping-in-a-linear-congruential-generator
    # This is where the LCG part comes into play, basically we've already created and LCG,
    # we just need to skip ahead by some number of shuffles, which is what this function does.
    return ((pow(mul, shuffle_by, (mul - 1) * mod) - 1) // (mul -1) * inc + pow(mul, shuffle_by, mod) * card_index) % mod

def shuffle_card(instructions, num_cards, card_index):
    # Gets the new index for a card after running through the shuffle instructions
    # each instruction can be reduced into either some addition/subtraction + modulus
    # or multiplication + modulus operations.

    for line in instructions:
        if line.startswith('deal into new stack'):
            card_index = (num_cards - card_index - 1) % num_cards
        elif line.startswith('deal with increment'):
            increment = int(line.split()[-1])
            card_index = (card_index * increment) % num_cards
        elif line.startswith('cut'):
            increment = int(line.split()[-1])
            card_index = (card_index - increment) % num_cards
    return card_index

DECK_SIZE = 119315717514047
SHUFFLES = 101741582076661
CARD_INDEX = 2020
card_index = CARD_INDEX
# So we need at least 3 values for a card's state after shuffling to derive the multiplier and increment value needed to
# derive all future values for that index. Because of the pseudorandom nature, any index will do, but might as well stick with
# the puzzle's constant.
mod, mul, inc = get_mod_mul_inc(*[(card_index := shuffle_card(data, DECK_SIZE, card_index)) for i in range(3)], DECK_SIZE)
print(shuffle_card(data, 10007, 2019))
print(super_shuffle(mul, inc, mod, CARD_INDEX, DECK_SIZE - SHUFFLES - 1))