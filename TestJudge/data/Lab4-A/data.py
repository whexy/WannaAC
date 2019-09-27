#!/usr/bin/python3

from random import *

T = randint(1, 200)

print(T)

for t in range(T):
    n = randint(1, 1000)
    coef = [randint(-10000, 100000) for i in range(n)]
    exp = [randint(0, 100000000) for i in range(n)]
    exp = list(set(exp))
    exp.sort()
    n = len(exp)
    print(n)
    for i in range(n):
        print(coef[i], exp[i])
    m = randint(1, 1000)
    coef = [randint(-10000, 100000) for i in range(m)]
    exp = [randint(0, 100000000) for i in range(m)]
    exp = list(set(exp))
    exp.sort()
    m = len(exp)
    print(m)
    for i in range(m):
        print(coef[i], exp[i])
    q = randint(1, 2000)
    k = [randint(0, 1000000000) for i in range(q)]
    k = list(set(k))
    k.sort()
    q = len(k)
    print(q)
    for i in range(q):
        print(k[i])




