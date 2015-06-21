#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-20
# Last Modified by:   andreshp
# Last Modified time: 2015-06-20
# File Name: 3.py
###################################################################

import math
import sys
import time

#------------------------------ MAIN -------------------------------#

N, K = [int(x) for x in input().split()]
B = [int(x) for x in input().split()]
G = [int(x) for x in input().split()]
G.sort()
B.sort()
sol = 0

j = 0; i = 0
while i < len(B) and j < len(G):
    if abs(B[i] - G[j]) <= K:
        sol += 1
        i+=1; j+=1
    elif B[i] > G[j] + K:
        j+=1
    elif B[i] < G[j] - K:
        i+=1
print(sol)