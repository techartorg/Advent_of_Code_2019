from collections import deque, defaultdict
from typing import Dict, List

data = deque([v.split(')') for v in open('day_06.input').read().split('\n')])

orbital_tree: Dict[str, List[str]] = defaultdict(list)
orbital_tree['COM'] = [] # Need to prime the tree with the base node
while data:
    parent, child = data.pop()
    if parent not in orbital_tree:
        data.appendleft([parent, child])
        continue

    orbital_tree[child].append(parent)
    orbital_tree[child].extend(orbital_tree[parent])

print(sum(len(v) for v in orbital_tree.values()))
print(len(set(orbital_tree['SAN']).symmetric_difference(orbital_tree['YOU'])))
