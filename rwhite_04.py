from string import digits
from typing import Iterable
possible_passwords: Iterable[str] = (str(v) for v in range(138241, 674034))
possible_passwords = [v for v in possible_passwords
                        if ''.join(sorted(v)) == v
                        and any(len(set(v[i:i+2])) == 1 for i in range(len(v)-1))]
filtered_passwords = [v for v in possible_passwords if any(v.count(d) == 2 for d in digits)]
print(len(possible_passwords))
print(len(filtered_passwords))
