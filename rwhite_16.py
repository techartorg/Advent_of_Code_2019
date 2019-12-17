from itertools import cycle, repeat, chain, islice
data = list(map(int, '12345678'))
data = list(map(int, '80871224585914546619083218645595'))
data = list(map(int, open('day_16.input').read()))

def build_pattern(index):
    pattern = chain.from_iterable([repeat(0, index), repeat(1, index), repeat(0, index), repeat(-1, index)])
    for idx, v in enumerate(cycle(pattern)):
        if idx == 0:
            continue
        yield v

# Slower first way, just brute forces it
# for _ in range(100):
#     nd = [int(str(sum([d*v for d, v in zip(data, build_pattern(i))]))[-1]) for i in range(1, len(data)+1)]
#     data = nd
# print(''.join(map(str, data))[:8])


# Smarter way where we build up some summations of slices
def transform(sequence, offset=0):
    # So when the offset if over half, then each value is just the sum of all the remaing items.
    # because the first half of things will be multiplied by zero, and the next half by 1
    # for some reason, its quicker to compute the sum once, and then subtract each value from it as we go
    # instead of rolling through backwards building up the summation with addition. Not sure why?
    output = [0] * len(sequence)
    if offset > len(sequence) // 2:
        # print(sequence[-10:])
        # for idx in range(-1, -len(sequence)-1, -1):
        #     output[idx] = (sequence[idx] + output[idx+1]) % 10
        total = sum(sequence[offset:])
        for n in range(offset, len(sequence)):
            output[n] = total % 10
            total -= sequence[n]
        return output

    for idx in range(offset, len(sequence)):
        step = idx + 1
        mult = 1
        for jdx in range(idx, len(sequence), step * 2):
            output[idx] += sum(sequence[jdx:jdx + step]) * mult
            mult *= -1

        output[idx] = abs(output[idx]) % 10
    return output

data = list(map(int, open('day_16.input').read()))

msg = data.copy()
for _ in range(100):
    msg = transform(msg)
print(''.join(str(c) for c in  msg)[:8])


msg = data.copy() * 10_000
offset = int(''.join(str(c) for c in data[:7]))
for _ in range(100):
    msg = transform(msg, offset)
print(''.join(str(c) for c in msg[offset:offset+8]))
