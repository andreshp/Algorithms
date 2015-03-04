# Heap Structures

A heap is a representation of a complete binary tree as an array.

The array has the Breadth-First Order of the nodes. Consecuently,
the following equitities are true:

~~~python
   leftChild(index) = 2*index+1
   rightChild(index) = 2*index+2
   parent(index) = (index-1) // 2
~~~

The heap structure can be used to get fast insertions and specific search operations in O(log n) and O(1) respectively. Some data structures based in this idea are given:

- **Min-Max-Heap** : Heap implementation where the programmer can chooses between a Max Heap or a Min Heap.
- **GeneralHeap** : Heap that allows, given a cuantile indicator, to obtain in constant time the element representative of that cuantile. The cuantile 0 and 1 work as a Min or Max Heap respectively.