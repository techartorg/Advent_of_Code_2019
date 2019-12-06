from collections import deque, defaultdict
from typing import Dict, List

data = deque(open('day_06.input').read().split('\n'))

orbital_tree: Dict[str, List[str]] = defaultdict(list)
orbital_tree['COM'] = [] # Need to prime the tree with the base node
while data:
    parent, child = data[-1].split(')')
    if parent not in orbital_tree:
        data.rotate(1)
        continue

    orbital_tree[child].append(parent)
    orbital_tree[child].extend(orbital_tree[parent])
    data.pop()

print(sum(len(v) for v in orbital_tree.values()))
print(len(set(orbital_tree['SAN']).symmetric_difference(orbital_tree['YOU'])))
