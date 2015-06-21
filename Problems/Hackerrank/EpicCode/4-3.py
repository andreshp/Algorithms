#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-21
# Last Modified by:   andreshp
# Last Modified time: 2015-06-21
# File Name: 4-3.py
###################################################################

import math
import sys
import time

#-------------------- KADANE ALGORITHM --------------------#

# Kadane's algorithm consists of a scan through the array values, computing at each position the maximum 
# (positive sum) subarray ending at that position. This subarray is either empty (in which case its sum is zero) 
# or consists of one more element than the maximum subarray ending at the previous position. 
# Thus, the problem can be solved with the following code, expressed here in Python:

def max_subarray(A):
    max_ending_here = max_so_far = 0
    for x in A:
        max_ending_here = max(0, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

# The runtime complexity of Kadane's algorithm is O(n).

#------------------------------ MAIN -------------------------------#

N = int(input())
A = [int(x) for x in input().split()]
sol = 0

for i in range(0, N-1):
    F = [A[i]*A[-1]]
    for k in range(1,(N-i-2)//2+1):
        F.append(A[i+k]*A[-k-1])
    sol = max(max_subarray(F),sol)

for j in range(1, N):
    F = [A[j]*A[0]]
    for k in range(1,(j-1)//2+1):
        F.append(A[j-k]*A[k])
    sol = max(max_subarray(F),sol)

print(sol)