#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-20
# Last Modified by:   andreshp
# Last Modified time: 2015-06-20
# File Name: 1.py
###################################################################

import math
import sys
import time

#---------------------------- FUNCTIONS ----------------------------#

def f(A, P,X,i):
    return A[i]*(P-X*i)

#------------------------------ MAIN -------------------------------#

N, P, X = [int(x) for x in input().split()]
A = [int(x) for x in input().split()]
rating = list(map(lambda i: f(A,P,X,i), range(0,len(A))))
print(rating.index(max(rating))+1)