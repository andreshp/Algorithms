#!/usr/bin/python

######################################################################
# Autor: Andrés Herrera Poyatos
# Date: February, 2015
# Min-Heap implementation for HeapSort
#######################################################################

import sys
import time

# Check if the given array is sorted
def isSorted(array):
    is_sorted = True
    for i in range(1,len(array)):
        if array[i-1] > array[i]:
            is_sorted = False; break
    return is_sorted

# Swap two components of an array
def swap(array, i, j):
    copy = array[i]
    array[i] = array[j]
    array[j] = copy

# MinHeap Class.
# A heap is a representation of a complete binary tree as an array.
# The array has the Breadth-First Order of the nodes. Consecuently,
# the following equitities are true:
#    leftChild(index) = 2*index+1
#    rightChild(index) = 2*index+2
#    parent(index) = (index-1) // 2
#
# A MinHeap is a heap where there is a total order relation and verifies the following property:
#    "heap[i] >= heap[parent(i)] for all i in range(0, size())"
# analogously:
#    "Each children is greater or equal than its parent."
# 
# Consecuently,  heap[0] is the minimum of the elements of the heap.
# A MinHeap supports the following operations:
#    - Get the minimum in O(1) (return heap[0])
#    - Insert an element in O(log n)
#    - Delete an element in O(log n)
class MinHeap(object):
    
    # Init method
    def __init__(self):
        self.heap = []

    # Check if the Heap is empty
    def empty(self):
        return (not self.heap)

    # Return the min of the Heap.
    # Precondition: The Heap must be not empty.
    def min(self):
        return self.heap[0] # A MinHeap keeps the min in the first position.

    # Size of the Heap
    def size(self):
        return len(self.heap)

    # Insert Method
    def insert(self, element):
        self.heap.append(element)
        self._repairUp(len(self.heap)-1)

    # Insert the elements of an array
    def insertArray(self, array):
        for number in array:
            self.insert(number)

    # Delete an element from the Heap
    # Precondition: The Heap must be not empty. 
    def delete(self, index):
        swap(self.heap, index, len(self.heap)-1)
        self.heap.pop()
        self._repairDown(index)

    # Delete min from the Heap.
    # Precondition: The Heap must be not empty. 
    def deleteMin(self):
        swap(self.heap, 0, len(self.heap)-1)
        self.heap.pop()
        self._repairDown(0)

    # Change the value of an element and repair the MinHeap Structure.
    def changeElement(self, index, value):
        self.heap[index] = value
        self._repairHeap(index)

    # Execute HeapSort to the elements of the heap.
    def heapSort(self):
        sorted_array = []
        while(not self.empty()):
            sorted_array.append(self.min())
            self.deleteMin()
        return sorted_array

    # Print Heap by levels
    def printHeap(self):
        elements_level = 1
        print("Heap:")
        for i in range(0, len(self.heap)):
            if i == elements_level:
                elements_level += elements_level+1; print()
            print(self.heap[i], " ", end="")
    
        print(); print()
    
    # Check that it is a MinHeap.
    # The invariant is checked.
    def _checkHeap(self):
        is_heap = True; fail = -1 
        for i in range(1, len(self.heap)):
            if self.heap[i] < self.heap[(i-1) // 2]:
                is_heap = False; fail = i; break

        return is_heap, fail

    # Repair the Min Heap invariant:
    # Each parent key is less or equal than their children keys.
    def _repairHeap(self, index):
        self._repairUp(index)
        self._repairDown(index)

    # Go up in the Heap repairing its invariant
    def _repairUp(self, index):
        parent = (index-1) // 2
        while index > 0:
            if self.heap[index] < self.heap[parent]:
                swap(self.heap, index, parent)
            else: break
            index = parent
            parent = (index-1) // 2

    # Go down in the Heap repairing its invariant
    def _repairDown(self, index):
        child = 2 * index + 1
        while child < len(self.heap):
            if child + 1 < len(self.heap) and self.heap[child] > self.heap[child+1]:
                child += 1
            if self.heap[index] > self.heap[child]:
                swap(self.heap, child, index)
            else: break
            index = child
            child = 2 * index +1
 
######################## MAIN ##########################

# See if arguments are correct
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Sintax: HeapSort.py <options> <numbers.txt>")
    print("  - Option -n : The array isn't printed.")
    sys.exit()

# Read array
try:
    numbers = open(sys.argv[1 if len(sys.argv) == 2 else 2], "r")    
    array = []
    for line in numbers:
        array.append(int(line))
except IOError:
   print("Error: The file",  numbers_file,  "can\'t be read.")
   sys.exit()

#--- Execute HeapSort and count the time wasted ---#
start_time = time.time()
my_heap = MinHeap(); my_heap.insertArray(array)
sorted_array = my_heap.heapSort()
print("--- %f seconds ---" % (time.time() - start_time) )

# Print the sorted array:
if len(sys.argv) == 2:
    for element in sorted_array:
        print(element, " ", end="")
    print()
numbers.close()

