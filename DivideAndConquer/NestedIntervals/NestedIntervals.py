#!/usr/bin/python

######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Number of nested Intervals Algorithm
#######################################################################

# Given an array of intervals, compute for each interval the number of other intervals
# which are nested in the current one.

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program
import bisect

#--------------------------- SOLUTION ----------------------------#

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


######################## MAIN ##########################

# See if arguments are correct.
if len(sys.argv) < 2:
    print("Error: Needs the array.txt as argument")
    sys.exit()

# Read array.
data = open(sys.argv[1], "r")    
intervals = [ ]
for line in data:
    intervals.append([ int(x) for x in line.split() ])

# Execute closestPair and count the time wasted.
start_time = time.time()
nested = nestedIntervals(intervals)
print("--- %f seconds ---" % (time.time() - start_time) )

data.close()
