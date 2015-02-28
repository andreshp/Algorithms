#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Date: February, 2015
# Coursera - Stanford - Algorithms: Design and Analysis, Part 1
# Week 6 - Programming Assignment - Part 1 - 2-SUM algorithm
######################################################################################

################################# PROBLEM STATEMENT ##################################
#
# Compute the number of target values t in the interval [-10000,10000] (inclusive) 
# such that there are distinct numbers x,y in the input file that satisfy x+y=t
#
# In the asked test n = 1000000
#
###################################### SOLUTION #######################################
#
# Let's delete the duplicates with a hash table and put the numbers in a sorted list A.
# This step takes O(nlog). A hash table H is declared. This will contain the numbers
# in [-10000,10000] that are got as a sum of a,b in A with a!=b.
# 
# Now lets take two pointers left and right to the beginning and end of the array.
# Were are going to iterate left through the list while left < right.
# In each iteration we cosider x = A[left]. We have to find every y in A verifying:
#   -10000 <= x+y <=  10000  -->  -10000 - x <= y <= 10000-x
# Consecuently, we can find the indexes of -10000-x and 10000-x in A with binary search,
# name them ymin and ymax, iterate between them (i) and add x+A[i] to H.
# 
# Note that we can assume ymin >= left since if ymin<left once we have already  
# considered A[i]+A[left] for i in ymin...left (when left = i).
# 
# This step depends on the data. In [1,...,n] it is O(n^2) but in average it seems
# O(n log n).
# 

######################################## CODE ########################################

import sys
import time

# Binary Search
def binarySearch(array, begin, end, key):
    while begin < end:
        middle = (begin + end) // 2
        if array[middle] < key:
            begin = middle+1
        elif array[middle] > key:
            end = middle
        else:
            return middle
    return begin

# Solution to the problem.
# It works as explained before.
# Precondition: A has no repeted values.
def solution(A):
    # Sort A
    A.sort()

    left = 0; right = len(A)-1
    numbers = set()
    limit = 10000
    
    while left < right:
        right = binarySearch(A, left, right, limit-A[left])
        if A[left] < -limit // 2:
            ymin = binarySearch(A, left, right, -limit-A[left])
        else:
            ymin = left+1
        for i in range(ymin, right+1):
            if A[i]+A[left] <= limit and A[i]+A[left] >= -limit and A[i]+A[left] not in numbers:
                numbers.add(A[i]+A[left])
        left += 1
    
    return len(numbers)

######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2:
    print("Sintax: python3 2sum_extended.py <txt with the arrray>")
    sys.exit()

# Read the array
numbers = open(sys.argv[1], "r")
A = {int(line) for line in numbers}
A = [a for a in A]

# Execute solution and count the time wasted
start_time = time.time()
sol = solution(A)
print("--- %f seconds ---" % (time.time() - start_time) )
print("Solution:", sol)
