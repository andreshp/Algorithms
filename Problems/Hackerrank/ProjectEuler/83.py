#!/usr/bin/python

######################################################################
# Author: Andrés Herrera Poyatos
#######################################################################

#------------- MINHEAP IMPLEMENTATION FOR DIJKSTRA--------------#

# Swap two components of an array
def swap(array, i, j):
    copy = array[i]
    array[i] = array[j]
    array[j] = copy
    array[i].index = i
    array[j].index = j

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
        element.index = len(self.heap)
        self.heap.append(element)
        self._repairUp(len(self.heap)-1)

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

#----------------- GRAPH IMPLEMENTATION ------------------#

# Node Class. Allows changing the way a node is interpreted.
class Node(object):

    # Contructor
    def __init__(self, key):
        self.key = key
        self.distance = -1
        self.index = -1
    # Overloading comparisons operators
    def __lt__(self, other):
        return (self.distance < other.distance)
    def __le__(self, other):
        return(self.distance <= other.distance)
    def __gt__(self, other):
        return(self.distance > other.distance)
    def __ge__(self, other):
        return(self.distance >= other.distance)
    # Hash function
    def __hash__(self):
        return self.key.__hash__()

#----------------- DIJKSTRA IMPLEMENTATION ------------------#

# Dijkstra algorithm
def dijkstra(matrix):

    # Find the node with key node.
    last = len(matrix)*len(matrix)-1
    visited = {0}; heap = MinHeap()
    current_nodes = {}

    # right
    neighbour = Node(1); neighbour.distance = matrix[0][1] + matrix[0][0]
    heap.insert(neighbour)
    current_nodes[1] = neighbour
    # down
    neighbour = Node(len(matrix)); neighbour.distance = matrix[1][0] + matrix[0][0]
    heap.insert(neighbour)
    current_nodes[len(matrix)] = neighbour

    # Extract the node for which we can claim we have the shortest path:
    next_node = heap.min(); heap.deleteMin()
    del current_nodes[next_node.key]; visited.add(next_node.key)

    # Apply the Dijkstra iteration until every node is visited
    while last not in visited:

        # Insert neighbours to the heap (if they aren't) or change their distance
        # if we have found a shorter path from node using next_node shortest path.

        # right
        key = next_node.key+1
        if key % len(matrix) != 0 and key not in visited:
            if key in current_nodes:
                current_nodes[key].distance = min(current_nodes[key].distance, next_node.distance+matrix[key // len(matrix)][key % len(matrix)])
                heap._repairUp(current_nodes[key].index)
            else:
                neighbour = Node(key); neighbour.distance = next_node.distance + matrix[key // len(matrix)][key % len(matrix)]
                heap.insert(neighbour); current_nodes[key] = neighbour
        # left
        key = next_node.key-1
        if next_node.key % len(matrix) != 0 and key not in visited:
            if key in current_nodes:
                current_nodes[key].distance = min(current_nodes[key].distance, next_node.distance+matrix[key // len(matrix)][key % len(matrix)])
                heap._repairUp(current_nodes[key].index)
            else:
                neighbour = Node(key); neighbour.distance = next_node.distance + matrix[key // len(matrix)][key % len(matrix)]
                heap.insert(neighbour); current_nodes[key] = neighbour
        # down
        key = next_node.key+len(matrix)
        if key // len(matrix) != len(matrix) and key not in visited:
            if key in current_nodes:
                current_nodes[key].distance = min(current_nodes[key].distance, next_node.distance+matrix[key // len(matrix)][key % len(matrix)])
                heap._repairUp(current_nodes[key].index)
            else:
                neighbour = Node(key); neighbour.distance = next_node.distance + matrix[key // len(matrix)][key % len(matrix)]
                heap.insert(neighbour); current_nodes[key] = neighbour
        # up
        key = next_node.key-len(matrix)
        if key > 0 and key not in visited:
            if key in current_nodes:
                current_nodes[key].distance = min(current_nodes[key].distance, next_node.distance+matrix[key // len(matrix)][key % len(matrix)])
                heap._repairUp(current_nodes[key].index)
            else:
                neighbour = Node(key); neighbour.distance = next_node.distance + matrix[key // len(matrix)][key % len(matrix)]
                heap.insert(neighbour); current_nodes[key] = neighbour

        # Extract the node for which we can claim we have the shortest path:
        next_node = heap.min(); heap.deleteMin()
        del current_nodes[next_node.key]; visited.add(next_node.key)

    return next_node.distance 

######################## MAIN ##########################

N = 80
matrix = [[]]*N
for i in range(0,N):
    matrix[i] = [int(x) for x in input().split(',')]
distance = dijkstra(matrix)
print(distance)