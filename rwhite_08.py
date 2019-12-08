
from typing import Set
data = open('day_08.input').read()
width = 25
height = 6

layers = [data[i:i+width*height] for i in range(0, len(data), width*height)]
layer = min(layers, key=lambda x : x.count('0'))
print(layer.count('1') * layer.count('2'))

flattened_image = ['2'] * width * height
seen: Set[int] = set()
for layer in layers:
    for idx, val in enumerate(layer):
        if idx in seen:
            continue
        if val != '2':
            flattened_image[idx] = val
            seen.add(idx)

out = '\n'.join(''.join(flattened_image[i:i+width]) for i in range(0, width*height, width))
out = out.replace('0', ' ').replace('1', '#')
print(out)