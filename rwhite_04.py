from string import digits
from typing import Iterable
possible_passwords: Iterable[str] = (str(v) for v in range(138241, 674034))
possible_passwords = [v for v in possible_passwords
                        if ''.join(sorted(v)) == v # Make sure the numbers are in ascending order
                        and any(len(set(v[i:i+2])) == 1 for i in range(len(v)-1))] # Make sure we've got at least one number pair
filtered_passwords = [v for v in possible_passwords if any(v.count(d) == 2 for d in digits)] # Make sure we've got only one pair
print(len(possible_passwords))
print(len(filtered_passwords))
