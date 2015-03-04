# General Heap

## Definition

A heap generalized. Given a quantile indicator c (between 0 and 1) it supports the following operations:

- Get the quantile-element in O(1) 
- Insert an element in O(log n)
- Delete the quantile-element in O(log n)

## Implementation

The implementation uses a Max Heap and a Min Heap that mantain the following invariant:

> The Max Heap keeps E[c*num_elements]+1 smaller elements and the MinHeap mantains the rest of elements. 

Consequently, the maximum of the Max Heap is the cuantile asked.

To keep the structure, given an element, it is inserted in the Max Heap if it is smaller or equal than its front or in the Min Heap otherwise. Then, the size of both heaps are adapted to verifiy the invariant. 

