from types import SimpleNamespace
from collections import deque
from typing import List, Tuple

from rwhite_intcode import Intcode

data = [int(i) for i in open('day_23.input').read().split(',')]
network: List[Tuple[Intcode, deque]] = [(Intcode(data[:]), deque()) for i in range(50)]

NAT = SimpleNamespace(x=0, y=0)
NAT_SENT = deque([object(), object()], maxlen=2)

# Assign network addresses.
for idx, (ic, q) in enumerate(network):
    ic.run_until_input()
    ic.send(idx)

sent_nat = False
while NAT_SENT[-1] != NAT_SENT[-2]:
    for ic, q in network:
        outbound: List[int] = []
        if q:
            # Process incoming packets in received order.
            while q:
                outbound.extend(ic.send_multiple(*q.popleft()))
                outbound.extend(ic.run_until_input(-1))
        else:
            # Otherwise we send -1 until we're reading to receive inputs again.
            outbound.extend(ic.run_until_input(-1))

        # Now we process the outbound queue
        for add, x, y in (outbound[i:i+3] for i in range(0, len(outbound), 3)):
            # If the target address is the NAT, update its values and continue processing.
            if add == 255:
                if not sent_nat:
                    print(y) # Part 01 output
                    sent_nat = True
                NAT.x = x
                NAT.y = y
                continue
            # Otherwise add x and y to the target's queue
            network[add][1].append((x, y))

    # If all the machines are idle, have the NAT kick box 0
    if all(not q for _, q in network):
        network[0][1].append((NAT.x, NAT.y))
        NAT_SENT.append(NAT.y)

print(NAT_SENT[0]) # Part 02 output