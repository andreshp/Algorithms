#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Universidad de Granada, January, 2015
# Sorting Algorithm: TimSort
#######################################################################

# This program read an integer array from a file a execute the TimSort 
# algorithm on it. Afterwards, the sorted array is printed.

import sys  # For arguments (syc.argv) and exit (syc.exit())
import time # To time the program

# Function that merge both subarrays ([begin,middle[, [middle,end[)
def merge(array, begin, middle, end):
    subarray = array[begin:middle]; j = middle; i = 0; k = begin
    count = 1; chosen = -1
    while i < len(subarray) and j < end:
        if subarray[i] <= array[j]:
            array[k:k+count] = subarray[i:i+count]; i += count; k += count
            if chosen == 0:
                count = min(end-k, len(subarray)-i, end-j, (int)(1.1*count))
            else:
                count = 1; chosen = 0
        else:
            array[k:k+count] = array[j:j+count]; j += count; k += count
            if chosen == 1:
                count = min(end-k, len(subarray)-i, end-j, (int)(1.1*count))
            else: 
                count = 1; chosen = 1

    if j >= end:
        array[k:end] = subarray[i:len(subarray)]
    for i in range(begin+1, end):
        insert(array, begin, i)

# Function which gets the next run for TimSort.
# A run is a sublist of array starting in begin verifying
# array[i] <= array[i+1] for all i in range(begin, sublist_size).
# If the algorithm just find a non-ascendent sublist it gets reversed.
def getRun(array, begin, end):
    if array[begin] <= array[begin+1]:
        i = begin + 2
        while i < end and array[i-1] <= array[i]:
            i += 1
    else:
        i = begin + 2
        while i < end and array[i-1] > array[i]:
            i += 1
        array[begin:i] = array[begin:i][::-1]

    if i - begin < 16:
        while(i < end and i - begin < 16):
            insert(array, begin, i); i += 1

    return i-begin

# Inserts the element of index given in the subarray array[0:index].
# It is supposed than that subarray is sorted.
def insert(array, begin, index):
    if index >= len(array):
        print((begin,index))
    i = index-1; element = array[index]
    while(i >= begin and array[i] > element):
        array[i+1] = array[i]; i -= 1
    array[i+1] = element

def mergeRuns(array, runs, begin):
    merge(array, runs[-2][0], runs[-1][0], begin)
    runs.pop();
    runs[-1] = (runs[-1][0], begin - runs[-1][0])

# Function that sorts the array [begin, end[ in O(n log n).
# It is the classical MergeSort implementation. Array is splitted
# recursively applying merge to both parts of the array.
def timSort(array, begin, end):
    runs = [ ]
    while begin + 1 < end:
        runs.append((begin, getRun(array, begin, end)))
        begin += runs[-1][1]
        while(len(runs) >= 2 and 2*runs[-1][1] > runs[-2][1]):
            mergeRuns(array, runs, begin)

    while(len(runs) >= 2):
        mergeRuns(array, runs, begin)
    
    for i in range(1, end):
        insert(array, 0, i)

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

# Execute timSort and count the time wasted
start_time = time.time()
timSort(array, 0, len(array))
print("--- %f seconds ---" % (time.time() - start_time) )

# Print the sorted array:
if len(sys.argv) == 2:
    for element in array:
        print(element, " ", end="")
    print()
numbers.close()
