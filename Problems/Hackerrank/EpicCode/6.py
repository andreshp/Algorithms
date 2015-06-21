#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-21
# Last Modified by:   andreshp
# Last Modified time: 2015-06-21
# File Name: 6.py
###################################################################

import math
import sys
import time

#---------------------------- FUNCTIONS ----------------------------#

def query1(array, x, y):
    count = 0
    for i in range(0, y-x+1):
        count = (count + (i+1)*(i+2)) % 1000000007
        array[x+i] = (array[x+i] + count) % 1000000007

    for i in range(y+1, len(array)):
        array[i] = (array[i] + count) % 1000000007

def query2(array,x,y):
    if x == 0:
        return array[y]
    else:
        sol = array[y] - array[x-1]
        if sol < 0:
            sol = 1000000007 + sol
        return sol

#------------------------------ MAIN -------------------------------#

N, Q = [int(x) for x in input().split()]
array = [0 for i in range(0,N)]
for i in range(0,Q):
    t, x, y = [int(x) for x in input().split()]
    if t == 1:
        query1(array,x-1,y-1)
    else:
        print(query2(array,x-1,y-1))