
import heapq
from collections import defaultdict
from typing import Dict, Tuple, Set, Any, List


def find_minimum_steps(data: List[str]):
    key_positions = {}
    bot_cnt = 0 # Part 2 adds some more robots.
    for x in range(len(data)):
        for y in range(len(data[x])):
            if data[x][y].islower():
                key_positions[data[x][y]] = (x, y)
            elif data[x][y] == '@':
                key_positions[str(bot_cnt)] = (x, y)
                bot_cnt += 1

    num_keys = len(key_positions) - bot_cnt

    def bfs(position: Tuple[int, int]) -> Dict[str, Tuple[int, Set[str]]]:
        # We're doing a breadth first search for this position, where we find the number of steps, and keys needed to
        # reach every other key.
        queue: List[Tuple[int, int, int, Set[str]]] = [(*position, 0, set())]
        seen: Set[Tuple[int, int]] = set()
        key_info: Dict[str, Tuple[int, Set[str]]] = dict()
        while queue:
            y, x, steps, keys_needed = queue.pop(0)
            if (y, x) in seen:
                continue
            seen.add((y, x))
            symbol = data[y][x]
            if symbol.islower() and position != (y, x):
                key_info[symbol] = (steps, keys_needed)

            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_symbol = data[dy+y][dx+x]
                if new_symbol != '#':
                    kn = keys_needed.copy() # Need to copy this here other wise the collection gets funky inside the loop
                    if new_symbol.isupper(): # If we've got a door, then we need to collect the cooresponding key
                        kn.add(new_symbol.lower())
                    queue.append((dy+y, dx+x, steps+1, kn))
        return key_info

    key_data: Dict[str, Dict[str, Tuple[int, Set[str]]]] = defaultdict(dict)
    for key_name in key_positions:
        for other_key, key_info in bfs(key_positions[key_name]).items():
            key_data[key_name][other_key] = key_info

    # Using our knowledge about how to get from each key we do a search for each bot
    # where check each other key, and if we've collected all of the keys needed to reach that new key
    # we update the distance, set the bots location to that new key, and add that key to our collection.
    # This new info gets added to the search_queue, which is sorted based on the minimum number of steps, and we keep
    # looking until we've collected all the keys.
    search_queue: List[Tuple[int, Tuple[List[str], Set[str]]]] = [(0, ([str(bot_idx) for bot_idx in range(bot_cnt)], set()))]
    seen: Set[Tuple[tuple, frozenset]] = set()
    while search_queue:
        # heapq keeps the sorting of our search_queue fast enough to make this approach viable.
        # heaps are always sorted such that popping gets you the minimum value item in the heap.
        dist, (locations, collected_keys) = heapq.heappop(search_queue)
        node = tuple(locations), frozenset(collected_keys)
        if len(collected_keys) == num_keys:
            return dist

        if node in seen:
            continue
        seen.add(node)

        for bot_idx, loc in enumerate(locations):
            for key_name, (steps, needed_keys) in key_data[loc].items():
                if not (needed_keys-collected_keys) and key_name not in collected_keys:
                    # We've got all the keys needed to get his next key, and we've not collected it yet, so add this guy to search_queue
                    # using heappush ensures our next loop through will still grab the minimum item.
                    targets = locations[:]
                    targets[bot_idx] = key_name
                    collection = collected_keys.copy()
                    collection.add(key_name)
                    heapq.heappush(search_queue, ((dist+steps), (targets, collection)))


print('Part 01:', find_minimum_steps(open('day_18.input').read().split('\n')))
print('Part 02:', find_minimum_steps(open('day_18_02.input').read().split('\n')))