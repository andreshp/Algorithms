#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Sorting Algorithm: MergeSort
#######################################################################

# This program read an integer array from a file a execute the MergeSort 
# algorithm on it. Afterwards, the sorted array is printed.

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program

# Function that merge both subarrays ([begin,middle[, [middle,end[)
def merge(array, begin, middle, end):
    sorted_array = [ ]; j = middle; i = begin
    
    while i < middle:
        if j < end:
            if array[i] <= array[j]:
                sorted_array.append(array[i])
                i += 1
            else:
                sorted_array.append(array[j])
                j += 1
        else:
            sorted_array.append(array[i])
            i += 1

    for i in range(j, end):
        sorted_array.append(array[i])

    for i in range(0, end-begin):
        array[i+begin] = sorted_array[i]
    

# Function that sorts the array [begin, end[ in O(n log n).
# It is the classical MergeSort implementation. Array is splitted
# recursively applying merge to both parts of the array.
def mergeSort(array, begin, end):
    middle = (begin + end) // 2

    if middle - begin > 1:
        mergeSort(array, begin, middle)
    if end - middle > 1:
        mergeSort(array, middle, end)
    if (begin < middle and middle < end):
        merge(array, begin, middle, end)


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

# Execute mergeSort and count the time wasted
start_time = time.time()
mergeSort(array, 0, len(array))
print("--- %f seconds ---" % (time.time() - start_time) )

# Print the sorted array:
if len(sys.argv) == 2:
    for element in array:
        print(element, " ", end="")
    print()
numbers.close()
