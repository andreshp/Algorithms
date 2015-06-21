#!/usr/bin/env python

###################################################################
# Author: Andrés Herrera Poyatos
# Email:  andreshp9@gmail.com
# Date:   2015-06-21
# Kadane Algorithm for 
###################################################################

import math
import sys
import time

#-------------------- MAXIMUM SUBARRAY PROBLEM --------------------#

# In computer science, the maximum subarray problem is the task of finding 
# the contiguous subarray within a one-dimensional array of numbers (containing 
# at least one positive number) which has the largest sum. 
# For example, for the sequence of values −2, 1, −3, 4, −1, 2, 1, −5, 4
# the contiguous subarray with the largest sum is 4, −1, 2, 1, with sum 6.

#------------------------ KADANE ALGORITHM ------------------------#

# Kadane's algorithm consists of a scan through the array values, computing at each position the maximum 
# (positive sum) subarray ending at that position. This subarray is either empty (in which case its sum is zero) 
# or consists of one more element than the maximum subarray ending at the previous position. 
# Thus, the problem can be solved with the following code, expressed here in Python:

def KadaneAlgorithm(A):
    max_ending_here = max_so_far = 0
    for x in A:
        max_ending_here = max(0, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

# The runtime complexity of Kadane's algorithm is O(n).

# If the vector does not have a positive number then the problem is trivial
# since the searched subarray is the one which consist of the greatest element
# in the array.

#------------------------------ MAIN -------------------------------#

# Example
A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("Sum for the maximum subarray problem on", A)
print(KadaneAlgorithm(A))