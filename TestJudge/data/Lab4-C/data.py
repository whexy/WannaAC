#!/usr/bin/python3

from random import *

chars_list = list('1234567890xLHIr')

T = randint(1, 20)
print(T)

for t in range(T):
    N = randint(20, 100000)
    l = []
    while not l:
        l = [choice(chars_list) for i in range(N)]
        while l[-1] == 'r':
            del l[-1]
        if len(l) > 1:
            for i in range(len(l)-1):
                if l[i] == 'r':
                    l[i+1] = choice(list('1234567890'))
    N = len(l)
    s = ''.join(l)
    print(N)
    print(s)
