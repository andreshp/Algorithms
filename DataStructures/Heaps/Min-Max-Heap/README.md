# Max/Min Heap

## Definition

### Min Heap

A **Min Heap** is a heap where there is a total order relation and verifies the following property:

> heap[i] >= heap[parent(i)] for all i in range(1, size())

analogously:

> Each children is greater or equal than its parent
 
Consecuently, heap[0] is the minimum of the elements of the heap.
 
### Max Heap

A MaxHeap is like a MinHeap but with:

> heap[i] <= heap[parent(i)] for all i in range(1, size())
  
Consecuently, heap[0] is the maximum of the elements of the heap.

### Operations

A Min/Max Heap supports the following operations:
    
- Get the minimum/maximum in O(1) (return heap[0])
- Insert an element in O(log n)
- Delete an element in O(log n)


## Implementation

This implementation let the user to choose between MaxHeap or MinHeap. I call it Min/Max Heap.

