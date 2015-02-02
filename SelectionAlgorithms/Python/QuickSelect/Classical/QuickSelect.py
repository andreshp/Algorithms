#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Sorting Algorithm: QuickSelect
#######################################################################

# This program read an integer array from a file a execute the QuickSelect 
# algorithm on it to find the ith order statistic element given as an argument. 
# Several variants of QuickSelect are given such as Lomuto or Hoare partition algorithm
# or some pivot selection methods. Choose the one you like but the best
# one is the implemented by defect.
# 
# This algorithm is based on QuickSort. With a similar analisys than the one done 
# for QuickSort you can see it is lineal in average but it has a quadratic worst case.

import sys                   # For arguments (syc.argv) and exit (syc.exit())
import time                  # To time the program
from random import randrange # Random integer generator

# Swap two elements in the array
def swap(array, i, j):
    aux = array[i]; array[i] = array[j]; array[j] = aux

# Select a random pivot for the subarray [begin,end[ and put it in the
# position begin. It's value is returned. 
def selectRandomPivot(array, begin, end):
    swap(array, begin, randrange(begin, end))
    return array[begin]

# Select a pivot for the subarray [begin,end[ and put it in the
# position begin. The pivot is selected as the median of 3 elements.
# It's value is returned.
def selectPivotMedian(array, begin, end):
    end -= 1; middle = (begin + end) // 2

    if array[begin] <= array[end]:
        if array[begin] >= array[middle]:
            index = begin
        else:
            index = middle if array[middle] <= array[end] else end
    else:
        if array[begin] <= array[middle]:
            index = begin
        else:
            index = middle if array[middle] >= array[end] else end

    swap(array, index, begin)
    return array[begin]

# Function that do a partition of the subarray [begin,end[.
# It uses the Lomuto algorithm. The expected total number
# of swaps is n/2 - 1/2. It perfoms poorly when there are
# repeted elements in the array since it does not divide it
# properly.
def partitionLomuto(array, begin, end):
    pivot = selectPivotMedian(array, begin, end)
    j = begin + 1 # j points to the first element bigger than pivot
    
    for i in range(begin+1, end):
        if array[i] < pivot:
            swap(array, j, i)
            j += 1

    swap(array, j-1, begin)
    return j-1

# Function that do a partition of the subarray [begin,end[.
# It uses the Hoare algorithm. The expected total number
# of swaps is n/6 - 1/3. It's better than the previous
# partition scheme and, furthermore, it does good partitions
# with repeted elements.
# A further comparison in:
# http://cs.stackexchange.com/questions/11458/quicksort-partitioning-hoare-vs-lomuto
def partitionHoare(array, begin, end):
    pivot = selectPivotMedian(array, begin, end)
    i = begin
    j = end - 1
    while True:
        while i < j and array[j] >= pivot:
            j -= 1

        while i < j  and array[i] <= pivot:
            i += 1

        if i < j:
            swap(array, i, j)
        else:
            swap(array, begin, j)
            return j
            

# Function that selects the order-th element of array [begin, end[ according to
# the sorting relation of the elements. It is call the ith-order statistic element.
# The algorithms runs with O(n) as average time.
# It is the classical QuickSelect implementation. 
# A partition it is performed and the search is done in the corresponding subarray.
def quickSelect(array, begin, end, order):
    if end - begin == 1:
        return array[begin]
    elif end - begin > 1:
        pivot_index = partitionHoare(array, begin, end)
        if pivot_index > order:
            return quickSelect(array, begin, pivot_index, order)
        elif pivot_index < order:
            return quickSelect(array, pivot_index+1, end, order)
        else:
            return array[pivot_index]


######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) != 3:
    print("Error: Needs the array.txt and the order of the element asked as arguments.")
    sys.exit()

# Read array
numbers = open(sys.argv[1])    
array = [ ]
for line in numbers:
    array.append(int(line))

# Get order and check it is correct
order = int(sys.argv[2])
if order < 0 or order >= len(array):
    print("Error: Order must be between 0 and the length of the array - 1.")
    sys.exit()

# Execute quickSelect and count the time wasted
start_time = time.time()
a = quickSelect(array, 0, len(array), order)
print("--- %f seconds ---" % (time.time() - start_time) )
print(order, "- ith order statistic: ", a)

numbers.close()
