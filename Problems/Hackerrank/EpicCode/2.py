#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-20
# Last Modified by:   andreshp
# Last Modified time: 2015-06-20
# File Name: 2.py
###################################################################

import math
import sys
import time

#---------------------------- FUNCTIONS ----------------------------#

#------------------------------ MAIN -------------------------------#

N = int(input())
S = list(input())
d = {}
sol = N
for x in S:
    if x in d:
        d[x] += 1
    else:
        d[x] = 1
for key in d.keys():
    sol += d[key]*(d[key]-1)//2
print(sol)

