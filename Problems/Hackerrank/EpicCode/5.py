#!/usr/bin/env python

###################################################################
# Author: andreshp
# Email:  andreshp9@gmail.com
# Date:   2015-06-20
# Last Modified by:   andreshp
# Last Modified time: 2015-06-21
# File Name: 5.py
###################################################################

from bisect import *

#---------------------------- FUNCTIONS ----------------------------#

# Recursive function
# If there are more than 1 element sorts intervals[start:end].
# Find the intervals from intervals[middle:end] nested in a interval of intervals[start:middle]
# Call recursively to both parts
def _nestedIntervals(intervals, start, end, nested):
    if start+1 < end:
        # Sort and find middle point
        intervals[start:end] = sorted(intervals[start:end], key = lambda x: (x[0], -x[1]))
        middle = (start + end) // 2

        # Sort second part according to second value
        intervals[middle:end] = sorted(intervals[middle:end],key = lambda x: x[1])
        B2 = list(map(lambda x: x[1], intervals[middle:end]))
        B2.sort()

        #print(intervals, start, middle, end, B2)
        # For each element in first part add intervals in second part contained
        for i in range(start, middle):
            nested[intervals[i]] += bisect_right(B2, intervals[i][1]) # binary search to position most to the right

        #print(nested)
        _nestedIntervals(intervals,start,middle,nested)
        _nestedIntervals(intervals,middle,end,nested)

# Compute for each interval the number of intervals nested in him.
def nestedIntervals(intervals):
    nested = {interval : 0 for interval in intervals}
    _nestedIntervals(intervals, 0, len(intervals), nested)
    return nested

#------------------------------ MAIN -------------------------------#

# Read the pairs with not repeated elements:
N = int(input())
pairs = set()
for i in range(0,N):
    pairs.add(input())
pairs = list(map(lambda x: tuple(map(int, x.split())), list(pairs)))

sol = 0
nested = nestedIntervals(pairs)
for key in nested:
    if nested[key] == 0:
        sol += 1

print(sol)