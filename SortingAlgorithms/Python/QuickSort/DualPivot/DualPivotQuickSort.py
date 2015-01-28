#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Sorting Algorithm: Dual Pivot QuickSort
#######################################################################

# This program read an integer array from a file a execute the Dual Pivot Quicksort 
# algorithm on it. Afterwards, the sorted array is printed. This algorithm with some
# modifications is the one used in Java Library. It performs O(nlogn) with repeated
# elements, recursion steps are done in smaller arrays and it performs the 80%
# of comparisons than classical Hoare-Quicksort.
# 
# Other 3-Partition algorithms have been developped to work better with repeted elements
# but they don't work with dual pivot scheme, doing in general even more comparisons
# than Hoare-QuickSort algorithm. 
# 
# More info in http://iaroslavski.narod.ru/quicksort/DualPivotQuicksort.pdf

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program

# Swap two elements in the array
def swap(array, i, j):
    aux = array[i]; array[i] = array[j]; array[j] = aux

# Function that do a partition of the subarray [begin,end[.
# It returns both pivots final indexes.
def partition(array, begin, end):
    end -= 1; 
    if array[begin] > array[end]:
        swap(array, begin, end)
    pivot1 = array[begin]; pivot2 = array[end]
    
    i = begin+1; j = end-1; k = begin+1
    while k <= j:
        if array[k] < pivot1:
            swap(array, i, k); i += 1
        else:
            if array[k] >= pivot2:
                while array[j] > pivot2 and k < j:
                    j -= 1
                swap(array, k, j); j -= 1
                if array[k] < pivot1:   
                    swap(array, i, k); i += 1
        k += 1

    i -= 1; j += 1; swap(array, begin, i); swap(array, j, end)

    return i, j


# Function that sorts the array [begin, end[ in O(n log n) as average time.
# It is the DualPivotQuickSort implementation. A partition with two pivots is performed
# and the 3 subarrays are sorted.
def dualPivotQuickSort(array, begin, end):
    [pivot1, pivot2] = partition(array, begin, end)

    if pivot1 - begin > 1:
        dualPivotQuickSort(array, begin, pivot1)
    if pivot2 - pivot1 - 1 > 1:
        dualPivotQuickSort(array, pivot1+1, pivot2)
    if end - pivot2 - 1 > 1:
        dualPivotQuickSort(array, pivot2+1, end)


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

# Execute dualPivotQuickSort and count the time wasted
start_time = time.time()
dualPivotQuickSort(array, 0, len(array))
print("--- %f seconds ---" % (time.time() - start_time) )

# Print the sorted array:
if len(sys.argv) == 2:
    for element in array:
        print(element, " ", end="")
    print()
numbers.close()
