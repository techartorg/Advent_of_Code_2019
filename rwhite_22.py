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
print(process_deck(range(10007)).index(2019))