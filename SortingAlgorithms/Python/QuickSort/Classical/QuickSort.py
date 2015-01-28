#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Sorting Algorithm: QuickSort
#######################################################################

# This program read an integer array from a file a execute the Quicksort 
# algorithm on it. Afterwards, the sorted array is printed. Several variants
# of Quicksort are given such as Lomuto or Hoare partition algorithm
# or some pivot selection methods. Choose the one you like but the best
# one is the implemented by defect.

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program
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
            

# Function that sorts the array [begin, end[ in O(n log n) as average time.
# It is the classical QuickSort implementation. A partition it is performed
# and subarrays are sorted.
def quickSort(array, begin, end):
    pivot_index = partitionHoare(array, begin, end)

    if pivot_index - begin > 1:
        quickSort(array, begin, pivot_index)
    if end - pivot_index - 1 > 1:
        quickSort(array, pivot_index+1, end)


######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) == 1 or len(sys.argv) > 3:
    print("Error: Needs the array.txt as an argument. The option -n don't print the sorted array.")
    sys.exit()

# Read array
numbers = open(sys.argv[1 if len(sys.argv) == 2 else 2], "r")    
array = [ ]
for line in numbers:
    array.append(int(line))

# Execute quickSort and count the time wasted
start_time = time.time()
quickSort(array, 0, len(array))
print("--- %f seconds ---" % (time.time() - start_time) )

# Print the sorted array:
if len(sys.argv) == 2:
    for element in array:
        print(element, " ", end="")
    print()
numbers.close()
