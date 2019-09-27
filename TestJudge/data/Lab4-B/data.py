#!/usr/bin/python3

from random import *

T = randint(1, 5)
print(T)

for t in range(T):
    N = randint(2, 1000)
    M = randint(1, 1000)
    l = list(range(N))
    shuffle(l)
    print(N, M)
    print(*l)
    for i in range(M):
        x1 = randint(0, N-2)
        y1 = randint(x1, N-2)
        x2 = randint(y1+1, N-1)
        y2 = randint(x2, N-1)
        print(l[x1], l[y1], l[x2], l[y2])
        # l[x1:y1+1], l[x2:y2+1] = l[x2:y2+1], l[x1:y1+1]
        ll = []
        ll.extend(l[0:x1])
        ll.extend(l[x2:y2+1])
        ll.extend(l[y1+1:x2])
        ll.extend(l[x1:y1+1])
        ll.extend(l[y2+1:])
        l = ll
    
