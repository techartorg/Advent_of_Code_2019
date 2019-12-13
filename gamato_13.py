"""
### Day 13: Care Package ###

As you ponder the solitude of space and the ever-increasing three-hour roundtrip for messages between you and
Earth, you notice that the Space Mail Indicator Light is blinking.
To help keep you sane, the Elves have sent you a care package.

It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all the way on the other end of the ship.
Surely, it won't be hard to build your own - the care package even comes with schematics.

The arcade cabinet runs Intcode software like the game the Elves sent (your puzzle input).
It has a primitive screen capable of drawing square tiles on a grid. The software draws tiles to the screen with
output instructions: every three output instructions specify the x position (distance from the left), y position
(distance from the top), and tile id. The tile id is interpreted as follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a horizontal paddle tile (1 tile from the left
and 2 tiles from the top) and a ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?

--- Part Two ---

The game didn't run because you didn't put in any quarters. Unfortunately, you did not bring any quarters.
Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.

The arcade cabinet has a joystick that can move left and right. The software reads the position of the joystick
with input instructions:

    If the joystick is in the neutral position, provide 0.
    If the joystick is tilted to the left, provide -1.
    If the joystick is tilted to the right, provide 1.

The arcade cabinet also has a segment display capable of showing a single number that represents the player's
current score. When three output instructions specify X=-1, Y=0, the third output instruction is not a tile;
the value instead specifies the new score to show in the segment display. For example, a sequence of output
values like -1,0,12345 would show 12345 as the player's current score.

Beat the game by breaking all the blocks. What is your score after the last block is broken?
"""


def run_intcode(input_data, ball=[0, 0], pad=[0, 0], free_play=False):
    op_counts = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]
    program = [int(x) for x in input_data] + [0] * 10000
    i, relative_base = 0, 0

    if free_play:
        program[0] = 2

    output = []
    blocks = 0
    score = 0

    while program[i] != 99:
        modes = [int(x) for x in f"{program[i]:0>5}"[:3]][::-1]
        instruction = int(f"{program[i]:0>5}"[3:])
        op_count = op_counts[instruction]
        base = [relative_base if modes[x] == 2 else 0 for x in range(op_count)]
        operands = [program[i+x+1] if modes[x] == 1 else program[base[x] + program[i+x+1]] for x in range(op_count)]

        if instruction == 1:
            program[base[2] + program[i + 3]] = operands[0] + operands[1]
        elif instruction == 2:
            program[base[2] + program[i + 3]] = operands[0] * operands[1]
        elif instruction == 3:
            if ball[0] < pad[0]:
                joy = -1
            elif ball[0] > pad[0]:
                joy = 1
            else:
                joy = 0
            program[base[0] + program[i + 1]] = joy
        elif instruction == 4:
            output.append(operands[0])
            if len(output) == 3:
                if not free_play:
                    if output[2] == 2:
                        blocks += 1
                    if output[2] == 3:
                        pad = [output[0], output[1]]
                    if output[2] == 4:
                        ball = [output[0], output[1]]
                else:
                    if output[0] == -1 and output[1] == 0:
                        score = output[2]
                    elif output[2] == 3:
                        pad = [output[0], output[1]]
                    elif output[2] == 4:
                        ball = [output[0], output[1]]
                output = []  # reset output
        elif instruction == 5:
            i = (operands[1] - 3) if operands[0] != 0 else i
        elif instruction == 6:
            i = (operands[1] - 3) if operands[0] == 0 else i
        elif instruction == 7:
            program[base[2] + program[i + 3]] = int(operands[0] < operands[1])
        elif instruction == 8:
            program[base[2] + program[i + 3]] = int(operands[0] == operands[1])
        elif instruction == 9:
            relative_base += operands[0]
        i += op_count + 1
    return blocks, ball, pad, score


if __name__ == "__main__":
    data = [int(x) for x in open("input13.txt", 'r').read().split(',')]

    block_num = sum(x == 2 for x in data[637:1680])  # The lazy way, HA!
    blocks, ball_pos, pad_pos, _ = run_intcode(data)
    print("Part One:", block_num, "=>", blocks)  # Just to validate the lazy way :)
    print("Part Two:", run_intcode(data, ball=ball_pos, pad=pad_pos, free_play=True)[3])
