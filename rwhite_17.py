from rwhite_intcode import Intcode, WAITING_FOR_INPUT

data = [int(i) for i in open('day_17.input').read().split(',')]

c = Intcode(data[:])
screen = ''.join(chr(v) for v in c.run_until_input()).split('\n')
screen = [l for l in screen if l]
height, width = (len(screen), len(screen[0]))
intersections = []
grid = {}
for h in range(height):
    for w in range(width):
        grid[w + -h*1j] = screen[h][w]
        try:
            if screen[h][w] == screen[h+1][w] == screen[h-1][w] == screen[h][w+1] == screen[h][w-1] == '#':
                intersections.append((h, w))
        except IndexError:
            continue

print(sum([h*w for h, w in intersections]))

start = next(k for k, v in grid.items() if v in '^<>v')
def get_neighbors(pos):
    return {v : grid.get(pos+v, '') for v in (1, -1, 1j, -1j)}

directions = {
    '^': 1j,
    '>': 1,
    '<': -1,
    'v': -1j,
}

steps = []
current_dir = directions[grid[start]]
pos = start
step_count = 0
d = ''
while True:
    if (n := get_neighbors(pos))[current_dir] == '#':
        step_count += 1
        pos += current_dir
    else:
        if d:
            steps.append(f'{d},{step_count}')
        if n[current_dir*-1j] == '#':
            d = 'R'
            current_dir *= -1j
        elif n[current_dir*1j] == '#':
            d = 'L'
            current_dir *= 1j
        else:
            break
        step_count = 0
# print('\n'.join(screen))
# print(len(steps), ','.join(steps))
# R,8,R,10,R,10,R,4,R,8,R,10,R,12,R,8,R,10,R,10,R,12,R,4,L,12,L,12,R,8,R,10,R,10,R,4,R,8,R,10,R,12,R,12,R,4,L,12,L,12,R,8,R,10,R,10,R,4,R,8,R,10,R,12,R,12,R,4,L,12,L,12
# A,B,A,C,A,B,C,A,B,C
# A: R,8,R,10,R,10
# B: R,4,R,8,R,10,R,12
# C: R,12,R,4,L,12,L,12
main = 'A,B,A,C,A,B,C,A,B,C'
ma = 'R,8,R,10,R,10'
mb = 'R,4,R,8,R,10,R,12'
mc = 'R,12,R,4,L,12,L,12'
move_data = data[:]
assert move_data[0] == 1 and c.memory[0] == 1
move_data[0] = 2
c = Intcode(move_data[:])
print(''.join(chr(v) for v in c.run_until_input(10)))
for v in main:
    c.send(ord(v))
print(''.join(chr(v) for v in c.run_until_input(10)))
for v in ma:
    c.send(ord(v))
print(''.join(chr(v) for v in c.run_until_input(10)))
for v in mb:
    c.send(ord(v))
print(''.join(chr(v) for v in c.run_until_input(10)))
for v in mc:
    c.send(ord(v))
print(''.join(chr(v) for v in c.run_until_input(10)))
print(c.send(ord('n'))) # I don't need the video feed
out = c.run_until_input(10) # Final output however is one last shot of the video feed, and then the amount of dust
# print(''.join(chr(v) for v in out)) # This would print out the last video feed screen
print(out[-1])
# print(c.send(ord('\n')))

# print(c.run_until_input())
