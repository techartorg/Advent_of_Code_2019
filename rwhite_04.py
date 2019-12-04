from string import digits
password_range = range(138241, 674034)
possible_passwords = []
for val in password_range:
    pword = str(val)
    if ''.join(sorted(pword)) == pword:
        if any(pword[i] == pword[i+1] for i in range(len(pword)-1)):
        # if any(pword.count(d) > 1 for d in digits):
            possible_passwords.append(pword)

print(len(possible_passwords))
filtered_passwords = []
for possible in possible_passwords:
    if any(possible.count(d) == 2 for d in digits):
        filtered_passwords.append(possible)
print(len(filtered_passwords))
