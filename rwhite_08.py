
from typing import Set
data = open('day_08.input').read()
width = 25
height = 6

layers = [data[i:i+width*height] for i in range(0, len(data), width*height)]
layer = min(layers, key=lambda x : x.count('0'))
print(layer.count('1') * layer.count('2'))

flatten = [next(v for v in pixel if v != '2') for pixel in zip(*layers)]
print('\n'.join(''.join('#' if int(v) else ' ' for v in flatten[i:i+width]) for i in range(0, width*height, width)))