# HeapSort

**HeapSort** is a sorting algorithm based on comparisons with efficiency O(n log n). It is based in the MinHeap Data Sructure.

##### What is a Heap
A **Heap** is a representation of a complete binary tree as an array. The array has the Breadth-First Order of the nodes. Consecuently, the following equitities are true:

- leftChild(index) = 2*index+1
- rightChild(index) = 2*index+2
- parent(index) = (index-1) // 2

##### What is a MinHeap
A **MinHeap** is a heap where there is a total order relation and verifies the following property:
    
*"heap[i] >= heap[parent(i)] for all i in range(0, size())"*

Analogously:

*"Each children is greater or equal than its parent."*

Consecuently,  heap[0] is the minimum of the elements of the heap. A MinHeap supports the following operations:

- Get the minimum in O(1) (return heap[0])
- Insert an element in O(log n)
- Delete an element in O(log n)

##### HeapSort

~~~python
    # Returns the element of the given Min Heap Sorted
    def heapSort(min_heap):
        sorted_array = []
        while(not min_heap.empty()):
            sorted_array.append(min_heap.min())
            min_heap.deleteMin()
        return sorted_array
~~~
