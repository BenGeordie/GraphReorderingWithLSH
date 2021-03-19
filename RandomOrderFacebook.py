import random
from collections import defaultdict


fb_in = open('facebook_combined.txt', 'r')
n = 0
for line in fb_in:
    n = max(n, int(line.split()[1]) + 1)
fb_in.close()
fb_in = open('facebook_combined.txt', 'r')
out = open('facebook_combined_randomly_ordered.txt', 'w')
ro = list(range(n))
random.shuffle(ro)

the_dict = defaultdict(lambda: [])

for line in fb_in:
    row = line.split()
    left = int(row[0])
    right = int(row[1])
    the_dict[ro[left]].append(ro[right])

keys = list(the_dict.keys())
keys.sort()
for key in keys:
    sorted_vals = the_dict[key]
    sorted_vals.sort()
    for val in sorted_vals:
        out.write(f'{key} {val}\n')


out.close()

