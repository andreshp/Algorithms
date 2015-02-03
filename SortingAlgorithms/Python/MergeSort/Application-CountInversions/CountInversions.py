#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, 2º DGMII
# Algorithms: Design and Analysis, Part 1 at Coursera
# Week 1, Programming Assignment 1, CountInversions.py
#######################################################################

# This program read an integer array from a file a execute the Counting Inversions
# algorithm based on mergesort for counting the number of inversions of the array.
# A inversion is a pair (i,j) with i < j verifying array[i] > array[j].
# As a collateral effect the array will get sorted.
# The algorithm is explained at the Coursera's course 
# Algorithms: Design and Analysis, Part 1 at Coursera, Week 1

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program

# Function that merge both subarrays ([begin,middle[, [middle,end[)
# and counts the number of inversions in this case. Time O(end-begin)
def mergeCount(array, begin, middle, end):
    sorted_array = [ ]
    sol = 0; j = middle; i = begin
    
    while i < middle:
        if j < end:
            if array[i] <= array[j]:
                sorted_array.append(array[i])
                i += 1
            else:
                sorted_array.append(array[j])
                sol += (middle - i)
                j += 1
        else:
            sorted_array.append(array[i])
            i += 1

    for i in range(j, end):
        sorted_array.append(array[i])

    for i in range(0, end-begin):
        array[i+begin] = sorted_array[i]
    
    return sol

# Function that counts the number of inversions of the array [begin, end[.
# A inversion is a pair (i,j) with i < j verifying array[i] > array[j].
# The algorithm will also sort the array because it needs to use 
# mergesort and count de inversions in the merge function.
def countInversions(array, begin, end):
    middle = (begin + end) // 2
    sol = 0

    if middle - begin > 1:
        sol += countInversions(array, begin, middle)
    if end - middle > 1:
        sol += countInversions(array, middle, end)
    if (begin < middle and middle < end):
        sol += mergeCount(array, begin, middle, end)

    return sol


######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) < 2:
    print("Error: Needs the array.txt as argument")
    sys.exit()

# Read array
numbers = open(sys.argv[1], "r")    
array = [ ]
for line in numbers:
    array.append(int(line))

# Execute countInversions and count the time wasted
start_time = time.time()
print(countInversions(array, 0, len(array)))
print("--- %f seconds ---" % (time.time() - start_time) )

numbers.close()
