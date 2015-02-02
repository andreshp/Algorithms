#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Sorting Algorithm: Dual Pivot QuickSelect
#######################################################################

# This program read an integer array from a file a execute the Dual Pivot Quickselect
# algorithm on it to find the ith order statistic element given as an argument. 
# This algorithm uses the Dual Pivot scheme for Quicksort introduced in the Java Library.
# It performs with eficiency O(n) with repeated elements in average. Tt performs the 80%
# of comparisons than classical Hoare-Partition algorithm.
# 
# This algorithm it is not such a improvement over Classical QuickSelect as happens with QuickSort
# Since the 3 partition helps also to sort the array indirectly and reducing the size of the 3 recurrences.
# Here the help is much less appreciable.
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


# Function that selects the order-th element of array [begin, end[ according to
# the sorting relation of the elements. It is call the ith-order statistic element.
# The algorithms runs with O(n) as average time.
# It is a Dual Pivot QuickSelect implementation. 
# A partition it is performed and the search is done in the corresponding subarray.
def dualPivotQuickSelect(array, begin, end, order):
    if end - begin == 1:
        return array[begin]
    else:
        pivot1, pivot2 = partition(array, begin, end)
    
        if pivot1 > order:
            return dualPivotQuickSelect(array, begin, pivot1, order)
        elif pivot2 > order:
            if pivot1 == order:
                return array[pivot1]
            else:
                return dualPivotQuickSelect(array, pivot1+1, pivot2, order)
        elif pivot2 == order:
            return array[pivot2]
        else:
            return dualPivotQuickSelect(array, pivot2+1, end, order)


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

# Execute dualPivotQuickSelect and count the time wasted
start_time = time.time()
a = dualPivotQuickSelect(array, 0, len(array), order)
print("--- %f seconds ---" % (time.time() - start_time) )
print(order, "- ith order statistic: ", a)

numbers.close()