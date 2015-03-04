# Median Maintenance Problem

## Statement

The text file `Median.txt` (in TestCases directory) contains a list of the integers from 1 to 10000 in unsorted order. You should treat this as a stream of numbers, arriving one by one. Letting xi denote the ith number of the file, the kth median mk is defined as the median of the numbers x1,…,xk. (So, if k is odd, then mk is ((k+1)/2)th smallest number among x1,…,xk; if k is even, then mk is the (k/2)th smallest number among x1,…,xk.)

Find the sum of these 10000 medians, modulo 10000 (i.e., only the last 4 digits). That is, you should compute (m1+m2+m3+⋯+m10000)mod10000. 

## Solution

The median of a given array with numbers can be found in O(nlogn) time sorting it or O(n) with a linear selection algorithm. In any case, if we repeat the procces once per mk then we would get a O(n^2) algorithm, which is not good enough.

It seems that we need to use a data structure that let us getting the median and inserting elements in as much as O(log n) time. There are two options:

### Balanced Binary Search Trees

Using a Balanced Binary Search Tree that supports order statistic. Insertion is performed in O(log n) and getting the median in O(log n)

### Two Heaps

Using 2 heaps. Let's denote A to a MaxHeap and B to a MinHeap. Let's suppose that we have x1,…,xk in those heaps: x1,…,xk/2 in A and xk/2+1,…,xk in B. The median is max(A) or min(B) (depends on k). Thus, we have the median in O(1).

Let's try to keep this structure working for insertions. We are given the element xk+1. If xk+1 < max(A), insert it in A else insert it in B. That's logarithmic and keeps the first invariant (x <= y for all x in A, y in B). Now we need that |size(A)-size(B)| <= 1. But that's easy, if size(A) > size(B)+1, insert max(A) in B and extract it from A. Else if size(B) > size(A)+1, insert min(B) in A and extract it from B. 

We can implement an abstract version of this idea where we find a prefixed cuantile instead of the median. I call it **General Heap**. I give an implementation of this structure in [GitHub](https://github.com/andreshp/Algorithms/tree/master/DataStructures/Heaps/GeneralHeap)

It is proposed the second solution since doesn't need more than an array in memory. The first one would need the pointers and the information needed for using the Tree as Order Statistical Tree. Besides, less operations are done: there is no balancing method and the median is obtained in constant time.

## Implementation

The implementation is done with the [General Tree code](https://github.com/andreshp/Algorithms/tree/master/DataStructures/Heaps/GeneralHeap) that I have in GitHub. We only have to use it with cuantile 0.5. That's easy!
 
