#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-20
# Last Modified by:   andreshp
# Last Modified time: 2015-06-20
# File Name: 4.py
###################################################################

import math
import sys
import time

#---------------------------- FUNCTIONS ----------------------------#


#------------------------------ MAIN -------------------------------#

N = int(input())
A = [int(x) for x in input().split()]
sol = 0

# Build matrix solution
M = [[]]*(N//2)
for l in range(0,len(M)):
    M[l] = [[]]*(N-2*l-1)
    for i in range(0,N-2*l-1):
        M[l][i] = [0 for j in range(i+l+1, N-l)]

# Build M[0]:
for i in range(0, N-1):
    for j in range(0,N-i-1):
        M[0][i][j] = A[i]*A[j+i+1]
        sol = max(sol, M[0][i][j])

for l in range(1,N//2+1):
    for i in range(0,N-2*l-1):
        for j in range(0, N-2*l-i-1):
            M[l][i][j] = M[l-1][i][j+2]
            M[l][i][j] += M[0][i+l][j]
            sol = max(sol, M[l][i][j])
print(sol)