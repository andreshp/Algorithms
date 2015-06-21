#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-21
# Last Modified by:   andreshp
# Last Modified time: 2015-06-21
# File Name: KadaneAlgorithm.py
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

