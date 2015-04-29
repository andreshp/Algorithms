#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Project Euler - 9
#######################################################################

import math

#--------- EXPLANATION ---------#

# a+b+c = N => a+c = N-b (1)
# a^2 + b^2 = c^2 => (N-b)(c-a) = (c+a)(c-a) = c^2 - a^2 = b^2
# => c-a = b^2 / (N-b)   (2)
# Usando (1) y (2) se tiene que a y c están determinados por b.
# Basta recorrer todos los posibles b e ir calculando el máximo
# de forma progresiva.

#--------- CODE ---------#

T = int(input())

for i in range(0, T):
    N = int(input())
    maximum_abc = 0
    for b in range(1,N // 3):
        pow_2 = b**2
        if pow_2 % (N-b) == 0:
            a_1 = (N-b  - pow_2 // (N-b))
            if a_1 > 0 and a_1 % 2 == 0:
                a = a_1 // 2
                c = N - a - b
                possible_sol =  - a * b * c
                if possible_sol < maximum_abc:
                    maximum_abc = possible_sol
    print(-maximum_abc if maximum_abc < 0 else -1)