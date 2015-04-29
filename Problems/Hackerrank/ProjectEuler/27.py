#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, May, 2015
# Project Euler - 27
#######################################################################

import math

def isPrime(n):
    if n < 2 or (n > 2 and n % 2 == 0):
        return False
    sqrt = int(math.sqrt(n)); i = 3
    while i <= sqrt:
        if n % i == 0:
            return False
        i+=2
    return True

N = int(input())

a_max = -1
b_max = 41
max_n = 42
b = 1
while b <= N:
    for a in range(-b+1, N+1):
        n = 0
        while isPrime(n*(n + a) + b):
            n += 1
        if n > max_n:
            a_max = a; b_max = b; max_n = n
    b+=2
print(a_max, b_max)