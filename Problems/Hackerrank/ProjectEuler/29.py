#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
#######################################################################

import math

N = int(input())
sol = 0
log_N = math.log(N)
for i in range(0, N-1):
    log = int(log_N / math.log(N-i))
    print(N-i, log, 1 + (N-2) // log + (N-2) % log)
    sol += 1 + (N-2) // log + (N-2) % log 

print(sol)