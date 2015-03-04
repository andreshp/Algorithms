#!/usr/bin/python

######################################################################################
# Autor: Andrés Herrera Poyatos
# Date: February, 2015
# General Heap implementation 
######################################################################################


import sys
import time

#-------------------------------------- HEAP --------------------------------------#

# Swap two components of an array
def swap(array, i, j):
    copy = array[i]
    array[i] = array[j]
    array[j] = copy

# Max/Min Heap Class.
# A heap is a representation of a complete binary tree as an array.
# The array has the Breadth-First Order of the nodes. Consecuently,
# the following equitities are true:
#    leftChild(index) = 2*index+1
#    rightChild(index) = 2*index+2
#    parent(index) = (index-1) // 2
#
# A MinHeap is a heap where there is a total order relation and verifies the following property:
#    "heap[i] >= heap[parent(i)] for all i in range(1, size())"
# analogously:
#    "Each children is greater or equal than its parent."
# 
# Consecuently, heap[0] is the minimum of the elements of the heap.
# 
# A MaxHeap is like a MinHeap but with:
#    "heap[i] <= heap[parent(i)] for all i in range(1, size())"
#  
# Consecuently, heap[0] is the maximum of the elements of the heap.
#
# This implementation let the user to chooses between MaxHeap or MinHeap.
# I call it Min/Max Heap.
#
# A Min/Max Heap supports the following operations:
#    - Get the minimum/maximum in O(1) (return heap[0])
#    - Insert an element in O(log n)
#    - Delete an element in O(log n)
class Heap(object):
    
    # Init method
    def __init__(self, type_heap = "min"):
        self.heap = []
        self.min = True if type_heap == "min" else False

    # Check if the Heap is empty
    def empty(self):
        return (not self.heap)

    # Return the min/max of the Heap.
    # Precondition: The Heap must be not empty.
    def front(self):
        return self.heap[0] 

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

    # Delete the front of the Heap.
    # Precondition: The Heap must be not empty. 
    def pop(self):
        swap(self.heap, 0, len(self.heap)-1)
        self.heap.pop()
        self._repairDown(0)

    # Change the value of an element and repair the Min-Max Heap Structure.
    def changeElement(self, index, value):
        self.heap[index] = value
        self._repairHeap(index)

    # Execute HeapSort to the elements of the heap.
    def heapSort(self):
        sorted_array = []
        while(not self.empty()):
            sorted_array.append(self.front())
            self.pop()
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
    
    # Check that it is a Min-Max Heap.
    # The invariant is checked.
    def _checkHeap(self):
        is_heap = True; fail = -1 
        for i in range(1, len(self.heap)):
            if (self.min and self.heap[i] < self.heap[(i-1) // 2]) or (not self.min and self.heap[i] > self.heap[(i-1) // 2]):
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
            if (self.min and self.heap[index] < self.heap[parent]) or (not self.min and self.heap[index] > self.heap[parent]):
                swap(self.heap, index, parent)
            else: break
            index = parent
            parent = (index-1) // 2

    # Go down in the Heap repairing its invariant
    def _repairDown(self, index):
        child = 2 * index + 1
        while child < len(self.heap):
            if child + 1 < len(self.heap) and ((self.min and self.heap[child] > self.heap[child+1]) or (not self.min and self.heap[child] < self.heap[child+1])):
                child += 1
            if (self.min and self.heap[index] > self.heap[child]) or (not self.min and self.heap[index] < self.heap[child]):
                swap(self.heap, child, index)
            else: break
            index = child
            child = 2 * index +1

#-------------------------------------- General Heap --------------------------------------#

# General Heap class
# 
# A heap generalized. Given a quantile indicator (between 0 and 1) it supports the
# following operations:
#
# - Get the quantile-element in O(1) 
# - Insert an element in O(log n)
# - Delete the quantile-element in O(log n)
class GeneralHeap(object):

    # Init method
    def __init__(self, quantil):
        self.maxheap = Heap("max")
        self.minheap = Heap("min")
        self.quantil = quantil

    # Check if the Heap is empty
    def empty(self):
        return self.maxheap.empty()

    # Return the quantil asked of the Heap.
    # Precondition: The Heap must be not empty.
    def front(self):
        return self.maxheap.front()

    # Size of the Heap
    def size(self):
        return self.maxheap.size() + self.minheap.size()

    # Insert Method
    def insert(self, element):
        if self.maxheap.empty() or element < self.maxheap.front():
            self.maxheap.insert(element)
        else:
            self.minheap.insert(element)

        self.__repair()

    # Delete the front of the Heap.
    # Precondition: The Heap must be not empty. 
    def pop(self):
        self.maxheap.pop()
        self.__repair()

    def __repair(self):
        num_elements = self.size()
        if num_elements*self.quantil + 1 <= self.maxheap.size():
            self.minheap.insert(self.maxheap.front())
            self.maxheap.pop()
        elif num_elements*(1-self.quantil) < self.minheap.size():
            self.maxheap.insert(self.minheap.front())
            self.minheap.pop()


#----------------------------------- MAIN ----------------------------------#

# See if arguments are correct
if len(sys.argv) < 2:
    print("Sintax: python3 MedianMaintenance.py <txt with the arrray>")
    sys.exit()

# Read the array
numbers = open(sys.argv[1], "r")
A = [int(line) for line in numbers]

# Execute the algortigm and count the time wasted
start_time = time.time()
sol = 0
heap = GeneralHeap(0.5)
for a in A:
    heap.insert(a)
    sol = (sol + heap.front()) % 10000
    print(heap.front())
print("--- %f seconds ---" % (time.time() - start_time))
print("Solution:", sol)
