from rwhite_intcode import Intcode

data = [int(i) for i in open('day_21.input').read().split(",")]
ic = Intcode(data[:])
ic.run_until_input()
# Jump if there is a gap in the first 3 blocks, but you can land on the fourth
d = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J""".split('\n')
for v in d:
    ic.send_ascii(v)
out = ic.send_ascii('WALK')
if out[-1] != 10:
    print(out[-1])
else:
    print(''.join(chr(c) for c in out))
ic = Intcode(data[:])
ic.run_until_input()
# With the extra instructions, we can look ahead one more and see if that's a hole and only jump if we can immediately jump again to a safe spot.
d.extend("""NOT E T
NOT T T
OR H T
AND T J""".split('\n'))
for v in d:
    ic.send_ascii(v)
out = ic.send_ascii('RUN')
if out[-1] != 10:
    print(out[-1])
else:
    print(''.join(chr(c) for c in out))