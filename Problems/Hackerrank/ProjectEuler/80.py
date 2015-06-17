#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-17
# Last Modified by:   andreshp
# Last Modified time: 2015-06-17
# File Name: 80.py
###################################################################

import math
import sys
import time
import decimal

#---------------------------- FUNCTIONS ----------------------------#


#------------------------------ MAIN -------------------------------#

N = int(input())
P = int(input())
decimal.getcontext().prec = P # Choose precision
d_sum = 0

for i in range(2, N*N+1):
    sq = int(math.sqrt(i))
    if sq*sq != i:
        number = decimal.Decimal(i).sqrt()
        d_sum += sum([int(digit) for digit in str(number)])

print(d_sum)